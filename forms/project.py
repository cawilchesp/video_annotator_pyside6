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

from PySide6.QtWidgets import QDialog, QFileDialog, QColorDialog, QTableWidgetItem
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

import yaml
from pathlib import Path

from forms.project_ui import ProjectUI
from dialogs.info_message import InfoMessageApp

# For debugging
from icecream import ic


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
        self.project_folder = self.config['PROJECT_FOLDER']

        # ---------
        # Variables
        # ---------
        self.project_data = None
        self.classes_values = {}
        self.color_value = ''

        self.class_count = 0

        self.form_fill_state = {
            'project_name_textfield': False,
            'video_name_textfield': False,
            'project_folder_textfield': False,
            'frame_extraction_textfield': False
        }

        # ----------------
        # Generación de UI
        # ----------------
        self.ui = ProjectUI(self)
        theme = 'light' if self.theme_style else 'dark'
        theme_qss_file = f"themes/{self.theme_color}_{theme}_theme.qss"
        with open(theme_qss_file, "r") as theme_qss:
            self.setStyleSheet(theme_qss.read())


    # ---------
    # Funciones
    # ---------
    def on_textEdited(self):
        self.enable_ok_button()


    def on_video_button_clicked(self) -> None:
        """ Video file selection dialog to annotate """
        video_dialog = {
            'caption': { 0: 'Seleccione el archivo de video',
                         1: 'Select video file' },
            'filter': { 0: 'Archivos de Video (*.avi *.mp4 *.mpg *.m4v *.mkv)',
                        1: 'Video Files (*.avi *.mp4 *.mpg *.m4v *.mkv)' }
        }
        selected_file = QFileDialog.getOpenFileName(parent = self,
            dir = self.source_folder,
            caption = video_dialog['caption'][self.language_value],
            filter = video_dialog['filter'][self.language_value]
        )[0]

        if selected_file:
            self.source_folder = str(Path(selected_file).parent)
            self.config['SOURCE_FOLDER'] = self.source_folder
            with open(self.settings_file, 'w') as file:
                yaml.dump(self.config, file)
            self.ui.project_widgets['video_name_textfield'].text_field.setText(selected_file)
        else:
            self.info_app = InfoMessageApp({'size': (300, 100), 'type': 'error',
                'messages': ("No se seleccionó un archivo de video",
                             "Video file wasn't selected") })
            self.info_app.exec()
            

    def on_save_button_clicked(self) -> None:
        """ Folder selection dialog where annotations are saved """
        folder_dialog = { 0: 'Seleccione la carpeta del proyecto',
                          1: 'Select project folder' }
        selected_folder = QFileDialog.getExistingDirectory(parent = self,
            caption = folder_dialog[self.language_value],
            dir = self.project_folder )
        
        if selected_folder:
            self.project_folder = str(Path(selected_folder))
            self.config['PROJECT_FOLDER'] = self.project_folder
            with open(self.settings_file, 'w') as file:
                yaml.dump(self.config, file)
            self.ui.project_widgets['project_folder_textfield'].text_field.setText(selected_folder)
        else:
            self.info_app = InfoMessageApp({'size': (300, 100), 'type': 'error',
                'messages': ("No se seleccionó la carpeta del proyecto",
                             "Project folder wasn't selected") })
            self.info_app.exec()


    def on_class_color_button_clicked(self) -> None:
        """ Color dialog button """
        self.color_value = QColorDialog.getColor().name()
        self.ui.project_widgets['class_color_label'].set_color_label(self.color_value)


    def on_class_add_button_clicked(self) -> None:
        """ Adding new class and corresponding color """
        class_name = self.ui.project_widgets['class_textfield'].text_field.text()
        if class_name != '' and class_name not in self.classes_values:
            if self.color_value != '':
                self.classes_values[self.ui.project_widgets['class_textfield'].text_field.text()] = self.color_value
            else:
                self.classes_values[self.ui.project_widgets['class_textfield'].text_field.text()] = '#000000'

            self.class_count += 1
            if self.class_count > 1:
                window_width = self.geometry().width()
                window_height = self.geometry().height()
                self.resize(window_width, window_height + 40)
                self.ui.project_widgets['project_card'].resize(window_width - 16, window_height - 16 + 40)
                self.ui.project_widgets['cancel_button'].move(window_width - 232, window_height - 56 + 40)
                self.ui.project_widgets['ok_button'].move(window_width - 124, window_height - 56 + 40)
                self.ui.project_widgets['new_class_table'].resize(self.ui.project_widgets['new_class_table'].width(), self.ui.project_widgets['new_class_table'].height() + 40)
            
            self.ui.project_widgets['new_class_table'].setRowCount(self.class_count)
            self.ui.project_widgets['new_class_table'].setRowHeight(self.class_count - 1, 40)
            class_item = QTableWidgetItem(class_name)
            class_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            class_item.setBackground(QColor(0, 0, 0, 0))
            self.ui.project_widgets['new_class_table'].setItem(self.class_count - 1, 0, class_item)
            self.ui.project_widgets['new_class_table'].setItem(self.class_count - 1, 1, QTableWidgetItem(''))
            self.ui.project_widgets['new_class_table'].item(self.class_count - 1, 1).setBackground(QColor(self.color_value))
            
            self.ui.project_widgets['class_textfield'].text_field.setText('')
        
        self.enable_ok_button()
            

    def on_ok_button_clicked(self) -> None:
        """ Checking and saving form values """
        self.project_data = {
            'project_name': self.ui.project_widgets['project_name_textfield'].text_field.text(),
            'video_file': self.ui.project_widgets['video_name_textfield'].text_field.text(),
            'project_folder': self.ui.project_widgets['project_folder_textfield'].text_field.text(),
            'frame_extraction': int(self.ui.project_widgets['frame_extraction_textfield'].text_field.text()),
            'classes': self.classes_values
        }
        self.close()


    def on_cancel_button_clicked(self) -> None:
        """ Close dialog window without saving """
        self.close()


    def enable_ok_button(self) -> bool:
        """ Enable OK button if all form spaces are filled """
        for key in self.form_fill_state.keys():
            if self.ui.project_widgets[key].text_field.text() == '':
                self.form_fill_state[key] = False
            else: 
                self.form_fill_state[key] = True

        if False in self.form_fill_state.values():
            return self.ui.project_widgets['ok_button'].setEnabled(False)
        elif len(self.classes_values) > 0:
            return self.ui.project_widgets['ok_button'].setEnabled(True)