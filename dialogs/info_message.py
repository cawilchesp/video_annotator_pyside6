from PySide6.QtWidgets import QDialog, QLabel, QPushButton
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QIcon
from PySide6.QtCore import Qt

import yaml


# ----------------
# About App Dialog
# ----------------
class InfoMessageApp(QDialog):
    def __init__(self, attributes: dict):
        """ About Me Dialog """
        super().__init__()

        # --------
        # Settings
        # --------
        with open('settings.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.theme_style = self.config['THEME_STYLE']
        self.theme_color = self.config['THEME_COLOR']
        self.language_value = int(self.config['LANGUAGE'])

        # ---------
        # Variables
        # ---------
        self.attributes = attributes
        self.icon_button_colors = {
            'error': [348/360, 0.86, 0.96],
            'warning': [44/360, 1.0, 0.96],
            'success': [153/360, 0.53, 0.96]
        }
        self.title_dict = {
            'error': ('Error', 'Error'),
            'warning': ('Advertencia', 'Warning'),
            'success': ('Éxito', 'Success'),
        }



        # ---
        # GUI
        # ---
        self.setWindowFlags(Qt.FramelessWindowHint)
        theme = 'light' if self.theme_style else 'dark'
        theme_qss_file = f"themes/{self.theme_color}_{theme}_theme.qss"
        with open(theme_qss_file, "r") as theme_qss:
            self.setStyleSheet(theme_qss.read())
        
        # -------------
        # Dialog Window
        # -------------
        (w, h) = self.attributes['size']
        screen_x = int(self.screen().availableGeometry().width() / 2 - (w / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (h / 2))
        x, y = (screen_x, screen_y)
        self.setGeometry(x, y, w, h)

        self.setMinimumSize(w, h)

        self.title = QLabel(self)
        self.title.setObjectName('dialog_title')
        self.title.setGeometry(0, 0, w, 48)
        self.title.setFont(QFont('Segoe UI', 20))

        self.message = QLabel(self)
        self.message.setObjectName('dialog_message')
        self.message.setGeometry(0, 48, w, h-48)
        self.title.setFont(QFont('Segoe UI', 14))

        self.close_button = QPushButton(self)
        self.close_button.setGeometry(w-40, 14, 20, 20)
        self.close_button.setIcon(self.set_icon_color())
        self.close_button.clicked.connect(self.on_close_button_clicked)

        self.setProperty(self.attributes['type'], True)

        self.set_language(self.language_value)


    def set_icon_color(self):
        hue, sat, lum = self.icon_button_colors[self.attributes['type']]
        icon_color = QColor.fromHslF(hue, sat, lum)
        icon_pixmap = QPixmap('icons/close.png')
        painter = QPainter(icon_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(icon_pixmap.rect(), icon_color)
        painter.end()

        return QIcon(icon_pixmap)


    def set_language(self, language: int) -> None:
        """ Change language of title text """
        if language == 0:
            self.title.setText(self.title_dict[self.attributes['type']][0])
            self.message.setText(self.attributes['messages'][0])
        elif language == 1:
            self.title.setText(self.title_dict[self.attributes['type']][1])
            self.message.setText(self.attributes['messages'][1])


    def on_close_button_clicked(self):
        """ Close dialog """
        self.close()

        
        








        # -----------
        # Card Dialog
        # -----------
        # self.aboutapp_widgets['aboutapp_dialog_card'] = MD3Card(parent, {
        #     'position': (8, 8),
        #     'size': (width-16, height-16),
        #     'type': 'outlined',
        #     'titles': ('Anotador de Video', 'Video Annotator'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['version_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (8, 48),
        #     'width': width - 32,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Versión: 1.0', 'Version: 1.0'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['developed_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (8, 96), 
        #     'width': width - 32,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Desarrollado por:', 'Developed by:'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['person_icon'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (8, 144),
        #     'type': 'icon',
        #     'icon': 'user',
        #     'theme_color': self.theme_color } )

        # self.aboutapp_widgets['name_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (48, 152), 
        #     'width': width - 80,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Carlos Andrés Wilches Pérez', 'Carlos Andrés Wilches Pérez'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['profession_icon'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (8, 174),
        #     'type': 'icon',
        #     'icon': 'school',
        #     'theme_color': self.theme_color } )

        # self.aboutapp_widgets['profession_1_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (48, 182), 
        #     'width': width - 80,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Ingeniero Electrónico, BSc. MSc. PhD.', 'Electronic Engineer, BSc. MSc. PhD.'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['profession_2_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (48, 206), 
        #     'width': width - 80,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Universidad Nacional de Colombia', 'Nacional University of Colombia'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['profession_3_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (48, 238), 
        #     'width': width - 80,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Maestría en Ingeniería Electrónica', 'Master in Electronic Engineering'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['profession_4_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (48, 262), 
        #     'width': width - 80,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Doctor en Ingeniería', 'Doctor in Engineering'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['profession_5_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (48, 286), 
        #     'width': width - 80,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('Pontificia Universidad Javeriana', 'Xaverian Pontifical University'),
        #     'language': self.language_value } )

        # self.aboutapp_widgets['email_icon'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (8, 310),
        #     'type': 'icon',
        #     'icon': 'mail',
        #     'theme_color': self.theme_color } )

        # self.aboutapp_widgets['email_label'] = MD3Label(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (48, 318), 
        #     'width': width - 80,
        #     'type': 'subtitle',
        #     'align': 'left',
        #     'labels': ('cawilchesp@outlook.com', 'cawilchesp@outlook.com'),
        #     'language': self.language_value } )

        # # ---------
        # # Button Ok
        # # ---------
        # self.aboutapp_widgets['ok_button'] = MD3Button(self.aboutapp_widgets['aboutapp_dialog_card'], {
        #     'position': (width - 124, height - 56),
        #     'width': 100,
        #     'type': 'standard',
        #     'labels': ('Aceptar', 'Ok'),
        #     'theme_color': self.theme_color,
        #     'language': self.language_value,
        #     'clicked': parent.on_ok_button_clicked } )


    def on_ok_button_clicked(self):
        """ Close dialog """
        self.close()