"""
New Project

This file contains class New Project Dialog.

To provide the project information, it requires:

Name:
    Name of the project
Video File:
    Select the video file to annotate
Results Folder:
    Folder path where annotations are saved
Classes:
    Name of the class
    Color of the label for specified class
"""

from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import QSettings, QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator

import yaml
from pathlib import Path

from forms.project_ui import ProjectUI
from dialogs.info_message import InfoMessageApp


class NewProject(QDialog):
    def __init__(self):
        """ UI Project dialog class """
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings_file = 'settings.yaml'
        with open(self.settings_file, 'r') as file:
            self.config = yaml.safe_load(file)

        self.language_value = int(self.config['LANGUAGE'])
        self.theme_style = self.config['THEME_STYLE']
        self.theme_color = self.config['THEME_COLOR']
        self.source_folder = self.config['SOURCE_FOLDER']
        self.results_folder = self.config['RESULTS_FOLDER']

        # ---------
        # Variables
        # ---------
        self.project_data = None
        self.classes_values = {}
        self.color_value = ''

        # ----------------
        # Generación de UI
        # ----------------
        self.ui = ProjectUI(self)
        theme = 'light' if self.theme_style else 'dark'
        theme_qss_file = f"themes/{self.theme_color}_{theme}_theme.qss"
        with open(theme_qss_file, "r") as theme_qss:
            self.setStyleSheet(theme_qss.read())



        # self.number_value = mt3.ValueLabel(self.project_card, 'number_value',
        #     (256, y+14, 98), self.theme_value)
        # self.number_value.setText('0')
        # self.number_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # y += 68
        # self.class_value = mt3.ValueLabel(self.project_card, 'class_value',
        #     (8, y, w), self.theme_value)
        # self.class_value.setAlignment(Qt.AlignmentFlag.AlignTop)



    # ---------
    # Funciones
    # ---------
    def on_textEdited(self):
        return None




    def on_video_button_clicked(self) -> None:
        """ Video file selection dialog to annotate """
        if self.language_value == 0:
            dialog_message = 'Seleccione el archivo de video'
            dialog_filter = 'Archivos de Video (*.avi *.mp4 *.mpg *.m4v *.mkv)'
        elif self.language_value == 1:
            dialog_message = 'Choose video file'
            dialog_filter = 'Video Files (*.avi *.mp4 *.mpg *.m4v *.mkv)'

        selected_file = QFileDialog.getOpenFileName(self, dialog_message, self.source_folder, dialog_filter)[0]

        if selected_file:
            self.source_folder = str(Path(selected_file).parent)
            self.config['SOURCE_FOLDER'] = self.source_folder
            with open(self.settings_file, 'w') as file:
                yaml.dump(self.config, file)
            self.ui.project_widgets['video_name_textfield'].text_field.setText(selected_file)
        else:
            self.info_app = InfoMessageApp({
                'size': (300, 100),
                'messages': ("No se seleccionó un archivo de video",
                             "Video file wasn't selected"),
                'type': 'error'
            })
            self.info_app.exec()
            

    def on_save_button_clicked(self) -> None:
        """ Folder selection dialog where annotations are saved """
        if self.language_value == 0:
            open_message = 'Seleccione la carpeta de resultados'
        elif self.language_value == 1:
            open_message = 'Choose results folder'

        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(self, open_message, self.results_folder)
        
        if selected_folder:
            file_path = pathlib.Path(selected_folder)
            self.save_text.text_field.setText(f'{selected_folder}')
            self.settings.setValue('results_folder', str(file_path))
            self.results_folder = self.settings.value('results_folder')
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error en la selección', 'No se seleccionó la carpeta de resultados')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Selection error', "Results folder wasn't chosen")

    def on_class_color_button_clicked(self) -> None:
        """ Color dialog button """
        selected_color = QtWidgets.QColorDialog.getColor()
        self.color_value = f'{selected_color.red()}, {selected_color.green()}, {selected_color.blue()}'
        self.color_button.apply_styleSheet(self.theme_value, self.color_value)


    def on_class_add_button_clicked(self) -> None:
        """ Adding new class and corresponding color """
        if self.class_text.text_field.text() != '':
            if self.color_value != '':
                self.classes_values[self.class_text.text_field.text()] = self.color_value
            else:
                self.classes_values[self.class_text.text_field.text()] = '0, 0, 0'

            self.class_value.clear()
            for key, value in self.classes_values.items():
                c = self.class_value.text()
                self.class_value.setText(f'{c}{key}: {value}\n')
            
            x_window = self.geometry().x()
            y_window = self.geometry().y()
            w_window = self.geometry().width()

            cnt = len(self.classes_values)
            self.number_value.setText(f'{cnt}')

            if cnt > 2:
                self.setGeometry(x_window, y_window, w_window, 392+(cnt*16))
                self.project_card.setGeometry(8, 8, w_window-16, 376+(cnt*16))
                
                self.class_value.setGeometry(8, 320, w_window-32, cnt*16)

                self.aceptar_button.setGeometry(w_window-232, 336+(cnt*16), 100, 32)
                self.cancelar_button.setGeometry(w_window-124, 336+(cnt*16), 100, 32)
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error en la clase', 'No se le dio nombre a la clase')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Class error', 'Class name is missing')

        self.class_text.text_field.setText('')


    def on_ok_button_clicked(self) -> None:
        """ Checking and saving form values """
        if (self.name_text.text_field.text() == '' or self.video_text.text_field.text() == '' or 
                self.save_text.text_field.text() == '' or self.class_value.text() == ''):

            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error en el Formulario', 'Hacen falta datos del proyecto')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Form Error', 'Project data is missing')
        else:
            self.project_data = {
                'project_name': self.name_text.text_field.text(),
                'video_file': self.video_text.text_field.text(),
                'results_folder': self.save_text.text_field.text(),
                'classes': self.classes_values
            }
            self.close()


    def on_cancel_button_clicked(self) -> None:
        """ Close dialog window without saving """
        self.close()