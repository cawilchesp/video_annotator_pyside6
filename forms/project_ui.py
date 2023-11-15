from PySide6.QtWidgets import QDialog

from components.md3_button import MD3Button
from components.md3_card import MD3Card
from components.md3_label import MD3Label
from components.md3_textfield import MD3TextField
from components.md3_window import MD3Window

import yaml


class ProjectUI(QDialog):
    def __init__(self, parent):
        super(ProjectUI, self).__init__(parent)

        # --------
        # Settings
        # --------
        with open('settings.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.language_value = int(self.config['LANGUAGE'])
        self.theme_style = self.config['THEME_STYLE']
        self.theme_color = self.config['THEME_COLOR']
        self.source_folder = self.config['SOURCE_FOLDER']
        self.project_folder = self.config['PROJECT_FOLDER']

        # ---------
        # Variables
        # ---------
        self.project_widgets = {}

        # -----------
        # Main Window
        # -----------
        (width, height) = (380, 344)
        self.project_widgets['main_window'] = MD3Window( {
            'parent': parent,
            'size': (width, height),
            'minimum_size': (width, height),
            'labels': ('Nuevo Proyecto', 'New Project'),
            'language': self.language_value } )

        # ----------------
        # Card New Project
        # ----------------
        self.project_widgets['project_card'] = MD3Card(parent, {
            'position': (8, 8),
            'size': (width-16, height-16),
            'type': 'outlined',
            'titles': ('Información del Proyecto', 'Project Information'),
            'language': self.language_value } )
        
        self.project_widgets['project_name_textfield'] = MD3TextField(self.project_widgets['project_card'], {
            'position': (8, 48),
            'width': width - 32,
            'type': 'outlined',
            'labels': ('Nombre del Proyecto', 'Project Name'),
            'language': self.language_value,
            'text_edited': parent.on_textEdited } )

        self.project_widgets['video_name_textfield'] = MD3TextField(self.project_widgets['project_card'], {
            'position': (8, 108),
            'width': width - 72,
            'type': 'outlined',
            'labels': ('Archivo de Video', 'Video File'),
            'language': self.language_value,
            'text_edited': parent.on_textEdited } )

        self.project_widgets['video_name_button'] = MD3Button(self.project_widgets['project_card'], {
            'position': (width - 56, 122),
            'type': 'filled',
            'icon': 'file_video',
            'theme_color': self.theme_color,
            'clicked': parent.on_video_button_clicked } )
        
        self.project_widgets['project_folder_textfield'] = MD3TextField(self.project_widgets['project_card'], {
            'position': (8, 168),
            'width': width - 72,
            'type': 'outlined',
            'labels': ('Carpeta del Proyecto', 'Project Folder'),
            'language': self.language_value,
            'text_edited': parent.on_textEdited } )

        self.project_widgets['project_folder_button'] = MD3Button(self.project_widgets['project_card'], {
            'position': (width - 56, 182),
            'type': 'filled',
            'icon': 'results_folder',
            'theme_color': self.theme_color,
            'clicked': parent.on_save_button_clicked } )
        
        self.project_widgets['class_textfield'] = MD3TextField(self.project_widgets['project_card'], {
            'position': (8, 228),
            'width': 160,
            'type': 'outlined',
            'labels': ('Clases', 'Classes'),
            'language': self.language_value } )
        
        self.project_widgets['class_color_button'] = MD3Button(self.project_widgets['project_card'], {
            'position': (176, 242),
            'type': 'filled',
            'icon': 'palette',
            'theme_color': self.theme_color,
            'clicked': parent.on_class_color_button_clicked } )
        
        self.project_widgets['class_color_label'] = MD3Label(self.project_widgets['project_card'], {
            'position': (216, 242),
            'type': 'color',
            'color': '#ff8888',
            'theme_color': self.theme_color } )
        
        self.project_widgets['class_add_button'] = MD3Button(self.project_widgets['project_card'], {
            'position': (256, 242),
            'type': 'filled',
            'icon': 'new',
            'theme_color': self.theme_color,
            'clicked': parent.on_class_add_button_clicked } )

        # ---------------------
        # Buttons Ok and Cancel
        # ---------------------
        self.project_widgets['cancel_button'] = MD3Button(self.project_widgets['project_card'], {
            'position': (width - 232, height - 56),
            'width': 100,
            'type': 'standard',
            'labels': ('Cancelar', 'Cancel'),
            'language': self.language_value,
            'clicked': parent.on_cancel_button_clicked } )

        self.project_widgets['ok_button'] = MD3Button(self.project_widgets['project_card'], {
            'position': (width - 124, height - 56),
            'width': 100,
            'type': 'standard',
            'enabled': False,
            'labels': ('Aceptar', 'Ok'),
            'language': self.language_value,
            'clicked': parent.on_ok_button_clicked } )
