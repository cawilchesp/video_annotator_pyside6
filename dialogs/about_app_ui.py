from PySide6.QtWidgets import QDialog

from components.md3_window import MD3Window
from components.md3_card import MD3Card
from components.md3_label import MD3Label
from components.md3_button import MD3Button

import yaml


# ----------------
# About App Dialog
# ----------------
class AboutAppUI(QDialog):
    def __init__(self, parent):
        """ About Me Dialog """
        super(AboutAppUI, self).__init__(parent)

        # --------
        # Settings
        # --------
        with open('settings.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.language_value = int(self.config['LANGUAGE'])
        self.theme_style = self.config['THEME_STYLE']
        self.theme_color = self.config['THEME_COLOR']

        self.aboutapp_widgets = {}


        # -------------
        # Dialog Window
        # -------------
        (width, height) = (320, 408)
        self.aboutapp_widgets['main_window'] = MD3Window( {
            'parent': parent,
            'size': (width, height),
            'minimum_size': (width, height),
            'maximum_size': (width, height),
            'labels': ('Acerca de...','About...'),
            'language': self.language_value } )

        # -----------
        # Card Dialog
        # -----------
        self.aboutapp_widgets['aboutapp_dialog_card'] = MD3Card(parent, {
            'position': (8, 8),
            'size': (width-16, height-16),
            'type': 'outlined',
            'titles': ('Seguidor de Objetos en Video', 'Video Object Tracker'),
            'language': self.language_value } )

        self.aboutapp_widgets['version_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (8, 48),
            'width': width - 32,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Versión: 1.0', 'Version: 1.0'),
            'language': self.language_value } )

        self.aboutapp_widgets['developed_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (8, 96), 
            'width': width - 32,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Desarrollado por:', 'Developed by:'),
            'language': self.language_value } )

        self.aboutapp_widgets['person_icon'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (8, 144),
            'type': 'icon',
            'icon': 'user',
            'theme_color': self.theme_color } )

        self.aboutapp_widgets['name_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (48, 152), 
            'width': width - 80,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Carlos Andrés Wilches Pérez', 'Carlos Andrés Wilches Pérez'),
            'language': self.language_value } )

        self.aboutapp_widgets['profession_icon'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (8, 174),
            'type': 'icon',
            'icon': 'school',
            'theme_color': self.theme_color } )

        self.aboutapp_widgets['profession_1_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (48, 182), 
            'width': width - 80,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Ingeniero Electrónico, BSc. MSc. PhD.', 'Electronic Engineer, BSc. MSc. PhD.'),
            'language': self.language_value } )

        self.aboutapp_widgets['profession_2_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (48, 206), 
            'width': width - 80,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Universidad Nacional de Colombia', 'Nacional University of Colombia'),
            'language': self.language_value } )

        self.aboutapp_widgets['profession_3_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (48, 238), 
            'width': width - 80,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Maestría en Ingeniería Electrónica', 'Master in Electronic Engineering'),
            'language': self.language_value } )

        self.aboutapp_widgets['profession_4_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (48, 262), 
            'width': width - 80,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Doctor en Ingeniería', 'Doctor in Engineering'),
            'language': self.language_value } )

        self.aboutapp_widgets['profession_5_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (48, 286), 
            'width': width - 80,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Pontificia Universidad Javeriana', 'Xaverian Pontifical University'),
            'language': self.language_value } )

        self.aboutapp_widgets['email_icon'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (8, 310),
            'type': 'icon',
            'icon': 'mail',
            'theme_color': self.theme_color } )

        self.aboutapp_widgets['email_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (48, 318), 
            'width': width - 80,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('cawilchesp@outlook.com', 'cawilchesp@outlook.com'),
            'language': self.language_value } )

        # ---------
        # Button Ok
        # ---------
        self.aboutapp_widgets['ok_button'] = MD3Button(self.aboutapp_widgets['aboutapp_dialog_card'], {
            'position': (width - 124, height - 56),
            'width': 100,
            'type': 'standard',
            'labels': ('Aceptar', 'Ok'),
            'theme_color': self.theme_color,
            'language': self.language_value,
            'clicked': parent.on_ok_button_clicked } )