from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSettings

import sys
import cv2

import material3_components as mt3

style_colors = {
    'azul_gris': '59,66,83',
    'azul_negro': '46,52,65',
    'azul': '128,160,194',
    'amarillo': '237,204,135',
    'rojo': '193,96,105',
    'verde': '162,191,138',
    'blanco': '229,233,240',
    'gris': '178,178,178',
    'negro': '0,0,0'
}


def convert_cv_qt(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
    p = convert_to_Qt_format.scaled(1280, 720, Qt.AspectRatioMode.KeepAspectRatio)
    return QPixmap.fromImage(p)


def open_video(source_file: str):
    cap = cv2.VideoCapture(source_file)
    if not cap.isOpened():
        print('Error opening video stream or file')
        return 0

    video_properties = {
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': float(cap.get(cv2.CAP_PROP_FPS))
    }

    return video_properties


def frame_extraction(source_file: str, frames_folder: str, labeled_folder: str, resized_folder: str):
    cap = cv2.VideoCapture(source_file)
    if not cap.isOpened():
        print('Error opening video stream or file')
        return 0

    frame_progressBar = QtWidgets.QProgressDialog('Extrayendo frames...',
                            'Cancelar', 0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    frame_progressBar.setWindowModality(Qt.WindowModality.WindowModal)
    
    frame_number = 0
    while(cap.isOpened()):
        frame_progressBar.setValue(frame_number)
        ret, frame = cap.read()
        if not ret or frame_progressBar.wasCanceled():
            break
        
        frame_text = f'{frame_number}'.zfill(6)
        frame_image = f'{frames_folder}/image_{frame_text}.png'
        cv2.imwrite(frame_image, frame)

        label_file = open(f'{labeled_folder}/image_{frame_text}.txt', 'x')
        label_file.close()
        
        resized_image = f'{resized_folder}/image_{frame_text}.png'
        resized_frame = cv2.resize(frame, [416, 416], interpolation= cv2.INTER_LINEAR)
        cv2.imwrite(resized_image, resized_frame)
        
        frame_number += 1


# ----------------
# About App Dialog
# ----------------
class AboutApp(QtWidgets.QDialog):
    def __init__(self) -> None:
        """ About Me Dialog """
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings = QSettings(f'{sys.path[0]}/settings.ini', QSettings.Format.IniFormat)
        self.language_value = int(self.settings.value('language'))
        self.theme_value = eval(self.settings.value('theme'))

        # ----------------
        # Generación de UI
        # ----------------
        width = 320
        height = 408
        screen_x = int(self.screen().availableGeometry().width() / 2 - (width / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (height / 2))

        if self.language_value == 0:
            self.setWindowTitle('Acerca de...')
        elif self.language_value == 1:
            self.setWindowTitle('About...')
        self.setGeometry(screen_x, screen_y, width, height)
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setModal(True)
        self.setObjectName('object_about')
        if self.theme_value:
            self.setStyleSheet(f'QWidget#object_about {{ background-color: #E5E9F0;'
                f'color: #000000 }}')
        else:
            self.setStyleSheet(f'QWidget#object_about {{ background-color: #3B4253;'
                f'color: #E5E9F0 }}')


        self.about_card = mt3.Card(self, 'about_card',
            (8, 8, width-16, height-16), ('Anotador de Video', 'Video Annotator'), 
            self.theme_value, self.language_value)

        y, w = 48, width - 32
        mt3.FieldLabel(self.about_card, 'version_label',
            (8, y), ('Versión: 1.0', 'Version: 1.0'), self.theme_value, self.language_value)

        y += 48
        mt3.FieldLabel(self.about_card, 'desarrollado_label',
            (8, y), ('Desarrollado por:', 'Developed by:'), self.theme_value, self.language_value)

        y += 48
        mt3.IconLabel(self.about_card, 'nombre_icon',
            (8, y), 'person', self.theme_value)

        y += 6
        mt3.FieldLabel(self.about_card, 'nombre_label',
            (48, y), ('Carlos Andrés Wilches Pérez', 'Carlos Andrés Wilches Pérez'), self.theme_value, self.language_value)

        y += 30
        mt3.IconLabel(self.about_card, 'profesion_icon',
            (8, y), 'school', self.theme_value)
        
        y += 6
        mt3.FieldLabel(self.about_card, 'profesion_label',
            (48, y), ('Ingeniero Electrónico, BSc. MSc. PhD.', 'Electronic Engineer, BSc. MSc. PhD.'), self.theme_value, self.language_value)
        
        y += 24
        mt3.FieldLabel(self.about_card, 'profesion_label',
            (48, y), ('Universidad Nacional de Colombia', 'Universidad Nacional de Colombia'), self.theme_value, self.language_value)

        y += 32
        mt3.FieldLabel(self.about_card, 'profesion_label',
            (48, y), ('Maestría en Ingeniería Electrónica', 'Master in Electronic Engineering'), self.theme_value, self.language_value)

        y += 24
        mt3.FieldLabel(self.about_card, 'profesion_label',
            (48, y), ('Doctor en Ingeniería', 'Doctor in Engineering'), self.theme_value, self.language_value)

        y += 24
        mt3.FieldLabel(self.about_card, 'profesion_label',
            (48, y), ('Pontificia Universidad Javeriana', 'Pontificia Universidad Javeriana'), self.theme_value, self.language_value)

        y += 24
        mt3.IconLabel(self.about_card, 'email_icon',
            (8, y), 'mail', self.theme_value)

        y += 6
        mt3.FieldLabel(self.about_card, 'email_label',
            (48, y), ('cawilchesp@outlook.com', 'cawilchesp@outlook.com'), self.theme_value, self.language_value)

        y += 32
        self.aceptar_button = mt3.TextButton(self.about_card, 'aceptar_button',
            (w-92, y, 100), ('Aceptar', 'Ok'), 'done.png', self.theme_value, self.language_value)
        self.aceptar_button.clicked.connect(self.on_aceptar_button_clicked)

    def on_aceptar_button_clicked(self):
        self.close()

# ---------------
# About Qt Dialog
# ---------------
def about_qt_dialog(parent, language: int) -> None:
    """ About Qt Dialog """
    if language == 0:   title = 'Acerca de Qt...'
    elif language == 1: title = 'About Qt...'
    QtWidgets.QMessageBox.aboutQt(parent, title)