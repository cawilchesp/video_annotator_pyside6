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

from PySide6 import QtWidgets
from PySide6.QtCore import QSettings, QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator

import sys
import pathlib



class NewProject(QtWidgets.QDialog):
    def __init__(self):
        """ UI Project dialog class """
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings = QSettings(f'{sys.path[0]}/settings.ini', QSettings.Format.IniFormat)
        self.video_folder = self.settings.value('video_folder')
        self.results_folder = self.settings.value('results_folder')
        self.language_value = int(self.settings.value('language'))
        self.theme_value = eval(self.settings.value('theme'))

        self.regExp1 = QRegularExpressionValidator(QRegularExpression('[0-9A-Za-z_]{1,30}'), self)

        # ---------
        # Variables
        # ---------
        self.project_data = None
        self.classes_values = {}
        self.color_value = ''

        # ----------------
        # Generación de UI
        # ----------------
        width = 380
        height = 424
        screen_x = int(self.screen().availableGeometry().width() / 2 - (width / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (height / 2))

        if self.language_value == 0:
            self.setWindowTitle('Nuevo Proyecto')
        elif self.language_value == 1:
            self.setWindowTitle('New Project')
        self.setGeometry(screen_x, screen_y, width, height)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height + 200)
        self.setModal(True)
        self.setObjectName('object_dialog')
        if self.theme_value:
            self.setStyleSheet(f'QWidget#object_dialog {{ background-color: #E5E9F0;'
                f'color: #000000 }}')
        else:
            self.setStyleSheet(f'QWidget#object_dialog {{ background-color: #3B4253;'
                f'color: #E5E9F0 }}')


        self.project_card = mt3.Card(self, 'project_card',
            (8, 8, width-16, height-16), ('Información del Proyecto', 'Project Information'), 
            self.theme_value, self.language_value)
        
        y, w = 48, width - 32
        self.name_text = mt3.TextField(self.project_card,
            (8, y, w), ('Nombre del Proyecto', 'Project Name'), self.theme_value, self.language_value)
        self.name_text.text_field.setValidator(self.regExp1)

        y += 68
        self.video_text = mt3.TextField(self.project_card,
            (8, y, w-40), ('Archivo de Video', 'Video File'), self.theme_value, self.language_value)

        self.video_button = mt3.IconButton(self.project_card, 'video_button',
            (w-24, y+14), 'video_library.png', self.theme_value)
        self.video_button.clicked.connect(self.on_video_button_clicked)

        y += 68
        self.save_text = mt3.TextField(self.project_card,
            (8, y, w-40), ('Carpeta de Resultados', 'Results Folder'), self.theme_value, self.language_value)

        self.save_button = mt3.IconButton(self.project_card, 'save_button',
            (w-24, y+14), 'results_folder.png', self.theme_value)
        self.save_button.clicked.connect(self.on_save_button_clicked)

        y += 68
        self.class_text = mt3.TextField(self.project_card,
            (8, y, 160), ('Clases', 'Classes'), self.theme_value, self.language_value)

        self.color_button = mt3.ColorButton(self.project_card, 'color_button',
            (176, y+14), '0,0,0', self.theme_value)
        self.color_button.clicked.connect(self.on_color_button_clicked)

        self.add_button = mt3.IconButton(self.project_card, 'add_button',
            (216, y+14), 'new.png', self.theme_value)
        self.add_button.clicked.connect(self.on_add_button_clicked)

        self.number_value = mt3.ValueLabel(self.project_card, 'number_value',
            (256, y+14, 98), self.theme_value)
        self.number_value.setText('0')
        self.number_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        y += 68
        self.class_value = mt3.ValueLabel(self.project_card, 'class_value',
            (8, y, w), self.theme_value)
        self.class_value.setAlignment(Qt.AlignmentFlag.AlignTop)

        y += 48
        self.aceptar_button = mt3.TextButton(self.project_card, 'aceptar_button',
            (w-200, y, 100), ('Aceptar', 'Ok'), 'done.png', self.theme_value, self.language_value)
        self.aceptar_button.clicked.connect(self.on_aceptar_button_clicked)

        self.cancelar_button = mt3.TextButton(self.project_card, 'cancelar_button',
            (w-92, y, 100), ('Cancelar', 'Cancel'), 'close.png', self.theme_value, self.language_value)
        self.cancelar_button.clicked.connect(self.on_cancelar_button_clicked)


    # ---------
    # Funciones
    # ---------
    def on_video_button_clicked(self) -> None:
        """ Video file selection dialog to annotate """
        if self.language_value == 0:
            open_message = 'Seleccione el archivo de video'
            open_filter = 'Archivos de Video (*.avi *.mp4 *.mpg *.m4v *.mkv)'
        elif self.language_value == 1:
            open_message = 'Choose video file'
            open_filter = 'Video Files (*.avi *.mp4 *.mpg *.m4v *.mkv)'

        selected_file = QtWidgets.QFileDialog.getOpenFileName(self, open_message, self.video_folder, open_filter)

        if selected_file[0]:
            file_path = pathlib.Path(selected_file[0])
            video_path = str(file_path.parent)
            self.video_text.text_field.setText(f'{selected_file[0]}')
            self.settings.setValue('video_folder', video_path)
            self.video_folder = self.settings.value('video_folder')
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error en la selección', 'No se seleccionó un archivo de video')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Selection error', "Video file wasn't chosen")


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

    def on_color_button_clicked(self) -> None:
        """ Color dialog button """
        selected_color = QtWidgets.QColorDialog.getColor()
        self.color_value = f'{selected_color.red()}, {selected_color.green()}, {selected_color.blue()}'
        self.color_button.apply_styleSheet(self.theme_value, self.color_value)


    def on_add_button_clicked(self) -> None:
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


    def on_aceptar_button_clicked(self) -> None:
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


    def on_cancelar_button_clicked(self) -> None:
        """ Close dialog window without saving """
        self.close()