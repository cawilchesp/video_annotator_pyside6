"""
Frontend

This file contains main UI class and methods to control components operations.
"""

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPixmap, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QSettings, QRegularExpression

import sys
import pathlib
# import psycopg2
import cv2

import material3_components as mt3
import backend
import project

# -------------
# Base de Datos
# -------------
# connection = psycopg2.connect(user='postgres',
#                               password='ecf406Carolina',
#                               host='localhost',
#                               port='5432',
#                               database='video_annotator')
# cursor = connection.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS videos (
#                 id serial PRIMARY KEY,
#                 nombre VARCHAR(128) UNIQUE NOT NULL,
#                 is_calibrated BOOLEAN NOT NULL,
#                 matrix VARCHAR(128) NOT NULL
#                 )""")
# connection.commit()


class App(QWidget):
    def __init__(self):
        """ UI main application """
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings = QSettings(f'{sys.path[0]}/settings.ini', QSettings.Format.IniFormat)
        self.recent_videos = self.settings.value('recent_videos')
        self.language_value = int(self.settings.value('language'))
        self.theme_value = eval(self.settings.value('theme'))

        self.idioma_dict = {0: ('ESP', 'SPA'), 1: ('ING', 'ENG')}
        self.regExp1 = QRegularExpressionValidator(QRegularExpression('[0-9]{1,10}'), self)

        # ---------
        # Variables
        # ---------
        self.frames_folder = ''
        self.labeled_folder = ''
        self.resized_folder = ''
        self.video_width = 0
        self.video_height = 0
        self.total_frames = 0
        self.video_fps = 0
        self.video_timer = 100
        self.play_state = False

        self.project_info = None
        self.active_class = ''
        self.active_color = ''

        # ----------------
        # Generación de UI
        # ----------------
        width = 1300
        height = 700
        screen_x = int(self.screen().availableGeometry().width() / 2 - (width / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (height / 2))

        if self.language_value == 0:
            self.setWindowTitle('Anotador de Video')
        elif self.language_value == 1:
            self.setWindowTitle('Video Annotator')
        self.setGeometry(screen_x, screen_y, width, height)
        self.setMinimumSize(width, height)
        self.setObjectName('main')
        if self.theme_value:
            self.setStyleSheet(f'QWidget#main {{ background-color: #E5E9F0; color: #000000 }}'
                f'QComboBox QListView {{ border: 1px solid #000000; border-radius: 4;'
                f'background-color: #B2B2B2; color: #000000 }}')
        else:
            self.setStyleSheet(f'QWidget#main {{ background-color: #3B4253; color: #E5E9F0 }}'
                f'QComboBox QListView {{ border: 1px solid #E5E9F0; border-radius: 4;'
                f'background-color: #2E3441; color: #E5E9F0 }}')
        
        # -----------
        # Card Título
        # -----------
        self.titulo_card = mt3.Card(self, 'titulo_card',
            (8, 8, width-16, 48), ('',''), self.theme_value, self.language_value)


        # Espacio para título de la aplicación, logo, etc.

        
        self.idioma_menu = mt3.Menu(self.titulo_card, 'idioma_menu',
            (8, 8, 72), 2, 2, self.idioma_dict, self.theme_value, self.language_value)
        self.idioma_menu.setCurrentIndex(self.language_value)
        self.idioma_menu.currentIndexChanged.connect(self.on_idioma_menu_currentIndexChanged)
        
        self.tema_switch = mt3.Switch(self.titulo_card, 'tema_switch',
            (8, 8, 48), ('', ''), ('light_mode.png','dark_mode.png'), 
            self.theme_value, self.theme_value, self.language_value)
        self.tema_switch.clicked.connect(self.on_tema_switch_clicked)

        self.database_button = mt3.IconButton(self.titulo_card, 'database_button',
            (8, 8), 'database.png', self.theme_value)
        # self.database_button.clicked.connect(self.on_database_button_clicked)

        self.manual_button = mt3.IconButton(self.titulo_card, 'manual_button',
            (8, 8), 'help.png', self.theme_value)
        self.manual_button.clicked.connect(self.on_manual_button_clicked)

        self.about_button = mt3.IconButton(self.titulo_card, 'about_button',
            (8, 8), 'mail_L.png', self.theme_value)
        self.about_button.clicked.connect(self.on_about_button_clicked)

        self.aboutQt_button = mt3.IconButton(self.titulo_card, 'aboutQt_button',
            (8, 8), 'about_qt.png', self.theme_value)
        self.aboutQt_button.clicked.connect(self.on_aboutQt_button_clicked)

        # -------------
        # Card Proyecto
        # -------------
        self.proyecto_card = mt3.Card(self, 'proyecto_card',
            (8, 64, 180, 128), ('Proyecto', 'Project'), 
            self.theme_value, self.language_value)

        y_1 = 48
        self.recientes_menu = mt3.Menu(self.proyecto_card, 'recientes_menu',
            (8, y_1, 164), 10, 10, {}, self.theme_value, self.language_value)
        # for key, value in self.recent_videos.items():
        #     self.recientes_menu.addItem(key)
        # self.recientes_menu.setCurrentIndex(-1)

        y_1 += 40
        self.nuevo_button = mt3.IconButton(self.proyecto_card, 'nuevo_button',
            (140, y_1), 'new.png', self.theme_value)
        self.nuevo_button.clicked.connect(self.on_nuevo_button_clicked)
        
        # ----------------
        # Card Información
        # ----------------
        self.info_card = mt3.Card(self, 'info_card',
            (8, 200, 180, 210), ('Información', 'Information'), 
            self.theme_value, self.language_value)

        y_2 = 48
        self.nombre_value = mt3.ValueLabel(self.info_card, 'nombre_value',
            (8, y_2, 164), self.theme_value)

        y_2 += 30
        self.video_icon = mt3.IconLabel(self.info_card, 'video_icon',
            (8, y_2), 'movie', self.theme_value)

        self.video_value = mt3.ValueLabel(self.info_card, 'video_value',
            (40, y_2, 132), self.theme_value)
        
        y_2 += 30
        self.size_value = mt3.ValueLabel(self.info_card, 'size_value',
            (40, y_2, 132), self.theme_value)
        
        y_2 += 30
        self.frames_value = mt3.ValueLabel(self.info_card, 'frames_value',
            (40, y_2, 132), self.theme_value)

        # -----------
        # Card Clases
        # -----------
        self.clases_card = mt3.Card(self, 'clases_card',
            (8, 418, 180, 88), ('Clases', 'Classes'), 
            self.theme_value, self.language_value)

        y_3 = 48
        self.clases_menu = mt3.Menu(self.clases_card, 'clases_menu',
            (8, y_3, 124), 10, 10, {}, self.theme_value, self.language_value)
        self.clases_menu.currentIndexChanged.connect(self.on_clases_menu_currentIndexChanged)
        
        self.color_label = mt3.ColorLabel(self.clases_card, 'color_label',
            (140, y_3), '0,0,0')
        
        # -----------
        # Card Formas
        # -----------
        self.formas_card = mt3.Card(self, 'formas_card',
            (8, 514, 180, 128), ('Formas', 'Shapes'), 
            self.theme_value, self.language_value)
        
        y_4 = 48
        self.rectangulo_button = mt3.IconButton(self.formas_card, 'rectangulo_button',
            (25, y_4), 'rectangle.png', self.theme_value)
        self.rectangulo_button.clicked.connect(self.on_rectangulo_button_clicked)

        self.elipse_button = mt3.IconButton(self.formas_card, 'elipse_button',
            (80, y_4), 'elipse.png', self.theme_value)
        
        self.poligono_button = mt3.IconButton(self.formas_card, 'poligono_button',
            (135, y_4), 'poligono.png', self.theme_value)
        
        y_4 += 40
        self.linea_button = mt3.IconButton(self.formas_card, 'linea_button',
            (25, y_4), 'linea.png', self.theme_value)
        
        self.punto_button = mt3.IconButton(self.formas_card, 'punto_button',
            (80, y_4), 'punto.png', self.theme_value)
        
        self.cuboide_button = mt3.IconButton(self.formas_card, 'cuboide_button',
            (135, y_4), 'cuboid.png', self.theme_value)

        # ----------
        # Card Video
        # ----------
        self.video_card = mt3.Card(self, 'video_card',
            (196, 64, 1300, 68), ('', ''), self.theme_value, self.language_value)
        
        x_2 = 8
        self.slow_button = mt3.IconButton(self.video_card, 'slow_button',
            (x_2, 22), 'slow_play.png', self.theme_value)
        self.slow_button.clicked.connect(self.on_slow_button_clicked)

        x_2 += 40
        self.backFrame_button = mt3.IconButton(self.video_card, 'backFrame_button',
            (x_2, 22), 'back_frame.png', self.theme_value)
        self.backFrame_button.clicked.connect(self.on_backFrame_button_clicked)

        x_2 += 40
        self.backPlay_button = mt3.IconButton(self.video_card, 'backPlay_button',
            (x_2, 22), 'back_play.png', self.theme_value)
        self.backPlay_button.clicked.connect(self.on_backPlay_button_clicked)

        x_2 += 40
        self.pause_button = mt3.IconButton(self.video_card, 'pause_button',
            (x_2, 22), 'pause.png', self.theme_value)
        self.pause_button.clicked.connect(self.on_pause_button_clicked)

        x_2 += 40
        self.play_button = mt3.IconButton(self.video_card, 'play_button',
            (x_2, 22), 'play.png', self.theme_value)
        self.play_button.clicked.connect(self.on_play_button_clicked)

        x_2 += 40
        self.frontFrame_button = mt3.IconButton(self.video_card, 'frontFrame_button',
            (x_2, 22), 'front_frame.png', self.theme_value)
        self.frontFrame_button.clicked.connect(self.on_frontFrame_button_clicked)

        x_2 += 40
        self.fastPlay_button = mt3.IconButton(self.video_card, 'fastPlay_button',
            (x_2, 22), 'fast_play.png', self.theme_value)
        self.fastPlay_button.clicked.connect(self.on_fastPlay_button_clicked)

        x_2 += 40
        self.video_slider = mt3.Slider(self.video_card, 'video_slider',
            (x_2, 22, 890), self.theme_value)
        self.video_slider.sliderMoved.connect(self.on_video_slider_sliderMoved)
        self.video_slider.sliderReleased.connect(self.on_video_slider_sliderReleased)
        
        x_2 += 900
        self.frame_text = mt3.TextField(self.video_card,
            (x_2, 8, 100), ('Cuadro', 'Frame'), self.theme_value, self.language_value)
        self.frame_text.text_field.setValidator(self.regExp1)
        # self.frame_text.returnPressed.connect(self.on_frame_text_returnPressed)

        # -----------
        # Card Imagen
        # -----------
        self.imagen_card = mt3.Card(self, 'imagen_card',
            (196, 140, 800, 600), ('Imágenes', 'Images'), 
            self.theme_value, self.language_value)

        self.imagen_label = QtWidgets.QLabel(self.imagen_card)
        self.imagen_label.setGeometry(10, 10, 1280, 720)
        self.imagen_label.setFrameStyle(QtWidgets.QFrame.Shape.Box)

        # -------------
        # Card Opciones
        # -------------
        self.opciones_card = mt3.Card(self, 'opciones_card',
            (1520, 70, 180, 130), ('Opciones', 'Options'), 
            self.theme_value, self.language_value)
        
        y_5 = 48
        self.guardar_button = mt3.IconButton(self.opciones_card, 'guardar_button',
            (25, y_5), 'save.png', self.theme_value)
        
        self.deshacer_button = mt3.IconButton(self.opciones_card, 'deshacer_button',
            (80, y_5), 'undo.png', self.theme_value)
        
        self.roi_button = mt3.IconButton(self.opciones_card, 'roi_button',
            (135, y_5), 'roi.png', self.theme_value)
        
        y_5 += 40
        self.aumentar_button = mt3.IconButton(self.opciones_card, 'aumentar_button',
            (50, y_5), 'zoom_in.png', self.theme_value)

        self.tamanoNormal_button = mt3.IconButton(self.opciones_card, 'tamanoNormal_button',
            (110, y_5), 'zoom_out.png', self.theme_value)

        # ----------------
        # Card Anotaciones
        # ----------------
        self.anotaciones_card = mt3.Card(self, 'anotaciones_card',
            (1520, 200, 180, 820), ('Anotaciones', 'Annotations'), 
            self.theme_value, self.language_value)
        

    # ----------------
    # Funciones Título
    # ----------------
    def on_idioma_menu_currentIndexChanged(self, index: int) -> None:
        """ Language menu control to change components text language
        
        Parameters
        ----------
        index: int
            Index of language menu control
        
        Returns
        -------
        None
        """
        self.idioma_menu.language_text(index)
        
        self.proyecto_card.language_text(index)

        self.info_card.language_text(index)
        self.clases_card.language_text(index)
        self.formas_card.language_text(index)
        self.opciones_card.language_text(index)

        self.frame_text.language_text(index)
        self.anotaciones_card.language_text(index)

        self.settings.setValue('language', str(index))
        self.language_value = int(self.settings.value('language'))


    def on_tema_switch_clicked(self, state: bool) -> None:
        """ Theme switch control to change components stylesheet
        
        Parameters
        ----------
        state: bool
            State of theme switch control
        
        Returns
        -------
        None
        """
        if state: self.setStyleSheet('background-color: #E5E9F0; color: #000000')
        else: self.setStyleSheet('background-color: #3B4253; color: #E5E9F0')

        self.titulo_card.apply_styleSheet(state)
        self.idioma_menu.apply_styleSheet(state)
        self.tema_switch.set_state(state)
        self.tema_switch.apply_styleSheet(state)
        self.manual_button.apply_styleSheet(state)
        self.about_button.apply_styleSheet(state)
        self.aboutQt_button.apply_styleSheet(state)
        
        self.proyecto_card.apply_styleSheet(state)
        self.nuevo_button.apply_styleSheet(state)
        self.recientes_menu.apply_styleSheet(state)

        self.info_card.apply_styleSheet(state)
        self.nombre_value.apply_styleSheet(state)
        self.video_icon.apply_styleSheet(state)
        self.video_icon.set_icon('movie', state)
        self.video_value.apply_styleSheet(state)
        self.size_value.apply_styleSheet(state)
        self.frames_value.apply_styleSheet(state)

        self.clases_card.apply_styleSheet(state)
        self.clases_menu.apply_styleSheet(state)
        
        self.formas_card.apply_styleSheet(state)
        self.rectangulo_button.apply_styleSheet(state)
        self.elipse_button.apply_styleSheet(state)
        self.poligono_button.apply_styleSheet(state)
        self.linea_button.apply_styleSheet(state)
        self.punto_button.apply_styleSheet(state)
        self.cuboide_button.apply_styleSheet(state)
        
        self.opciones_card.apply_styleSheet(state)
        self.guardar_button.apply_styleSheet(state)
        self.deshacer_button.apply_styleSheet(state)
        self.aumentar_button.apply_styleSheet(state)
        self.tamanoNormal_button.apply_styleSheet(state)
        self.roi_button.apply_styleSheet(state)

        self.video_card.apply_styleSheet(state)
        self.slow_button.apply_styleSheet(state)
        self.backFrame_button.apply_styleSheet(state)
        self.backPlay_button.apply_styleSheet(state)
        self.pause_button.apply_styleSheet(state)
        self.play_button.apply_styleSheet(state)
        self.frontFrame_button.apply_styleSheet(state)
        self.fastPlay_button.apply_styleSheet(state)
        self.video_slider.apply_styleSheet(state)
        self.frame_text.apply_styleSheet(state)

        self.imagen_card.apply_styleSheet(state)

        self.anotaciones_card.apply_styleSheet(state)

        self.settings.setValue('theme', f'{state}')
        self.theme_value = eval(self.settings.value('theme'))


    def on_manual_button_clicked(self) -> None:
        """ Manual button to open manual window """

        return 0


    def on_about_button_clicked(self) -> None:
        """ About app button to open about app window dialog """
        self.about = backend.AboutApp()
        self.about.exec()


    def on_aboutQt_button_clicked(self) -> None:
        """ About Qt button to open about Qt window dialog """
        backend.about_qt_dialog(self, self.language_value)


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """ Resize event to control size and position of app components """
        width = self.geometry().width()
        height = self.geometry().height()

        self.titulo_card.resize(width - 16, 48)
        self.titulo_card.title.resize(width - 304, 32)
        self.idioma_menu.move(width - 312, 8)
        self.tema_switch.move(width - 232, 8)
        self.database_button.move(width - 176, 8)
        self.manual_button.move(width - 136, 8)
        self.about_button.move(width - 96, 8)
        self.aboutQt_button.move(width - 56, 8)

        self.video_card.setGeometry(196, 64, width - 392, 68)
        self.video_card.title.resize(0, 32)
        self.video_slider.setGeometry(288, 22, self.video_card.geometry().width() - 404, 32)
        self.frame_text.setGeometry(self.video_card.geometry().width() - 108, 8, 100, 52)
        
        self.imagen_card.setGeometry(196, 140, width - 392, height - 148)
        self.imagen_label.setGeometry(8,8, self.imagen_card.geometry().width()-16, self.imagen_card.geometry().height()-16)
        
        self.opciones_card.setGeometry(width - 188, 64, 180, 128)
        self.anotaciones_card.setGeometry(width - 188, 200, 180, height - 208)
        
        return super().resizeEvent(a0)

    # ------------------
    # Funciones Proyecto
    # ------------------
    def on_nuevo_button_clicked(self) -> None:
        """ Configure new project """
        self.new_window = project.NewProject()
        self.new_window.exec()

        self.project_info = self.new_window.project_data

        if self.project_info:
            # Información del proyecto
            project_name = self.project_info['project_name']
            video_file = self.project_info['video_file']
            results_folder = self.project_info['results_folder']
            classes = self.project_info['classes']

            # Creación de la carpeta del proyecto
            project_folder = pathlib.Path(f'{results_folder}/{project_name}')
            if not project_folder.exists():
                project_folder.mkdir()

                self.clases_menu.clear()
                for key, value in classes.items():
                    self.clases_menu.addItem(key)
                self.clases_menu.setCurrentIndex(0)

                frames_folder = pathlib.Path(f'{results_folder}/{project_name}/frames')
                frames_folder.mkdir()
                self.frames_folder = frames_folder

                labeled_folder = pathlib.Path(f'{results_folder}/{project_name}/labels')
                labeled_folder.mkdir()

                resized_folder = pathlib.Path(f'{results_folder}/{project_name}/resized')
                resized_folder.mkdir()

                # Extracción de información del video
                video_properties = backend.open_video(video_file)
                self.video_width = video_properties["width"]
                self.video_height = video_properties["height"]
                self.total_frames = video_properties['frame_count']
                self.video_fps = video_properties['fps']

                # Presentación de Información
                self.nombre_value.setText(f'{project_name}')
                self.video_value.setText(f'{pathlib.Path(video_file).name}')
                self.size_value.setText(f'{self.video_width} X {self.video_height}')
                self.frames_value.setText(f'{self.total_frames} frames')

                self.video_slider.setMaximum(self.total_frames)

                # Extracción de frames del video
                backend.frame_extraction(video_file, frames_folder, labeled_folder, resized_folder)
                
                # Presentación del frame 0
                cv_img = cv2.imread(f'{frames_folder}/image_000000.png')
                qt_img = backend.convert_cv_qt(cv_img)
                self.imagen_label.setPixmap(qt_img)
                self.frame_text.text_field.setText('0')
            else:
                if self.language_value == 0:
                    QtWidgets.QMessageBox.critical(self, 'Error en la creación', 'La carpeta ya existe')
                elif self.language_value == 1:
                    QtWidgets.QMessageBox.critical(self, 'Creation Error', 'Folder already exists')


    # ----------------
    # Funciones Clases
    # ----------------
    def on_clases_menu_currentIndexChanged(self, index: int):
        classes = self.project_info['classes']
        self.active_class = self.clases_menu.currentText()
        self.active_color = classes[self.clases_menu.currentText()]
        self.color_label.set_color(self.active_color)


    # ----------------
    # Funciones Formas
    # ----------------
    def on_rectangulo_button_clicked(self):
        # Activa la herramienta rectángulo
        return 0
    

    # ------------------
    # Funciones Opciones
    # ------------------



    # ---------------
    # Funciones Video
    # ---------------
    def on_slow_button_clicked(self):
        if (self.video_timer + 10 < 1000):
            self.video_timer += 10


    def on_backFrame_button_clicked(self):
        # Save current frame
        # if labels: guardar

        frame_num = int(self.frame_text.text()) - 1
        if (frame_num >= 0):
            self.frame_text.setText(f'{frame_num}')
            frame_text = self.frame_text.text().zfill(6)
            cv_img = cv2.imread(f'{self.frames_folder}/image_{frame_text}.png')
            qt_img = backend.convert_cv_qt(cv_img)
            self.imagen_label.setPixmap(qt_img)
            self.video_slider.setSliderPosition(int(frame_text))


    def on_backPlay_button_clicked(self):
        self.play_state = True
        while(self.play_state):
            frame_num = int(self.frame_text.text()) - 1
            if (frame_num >= 0):
                self.frame_text.setText(f'{frame_num}')
                frame_text = self.frame_text.text().zfill(6)
                cv_img = cv2.imread(f'{self.frames_folder}/image_{frame_text}.png')
                qt_img = backend.convert_cv_qt(cv_img)
                self.imagen_label.setPixmap(qt_img)
                self.video_slider.setSliderPosition(int(frame_text))
                cv2.waitKey(self.video_timer)
            else:
                self.play_state = False

    
    def on_pause_button_clicked(self):
        self.play_state = False

    
    def on_play_button_clicked(self):
        self.play_state = True
        while(self.play_state):
            frame_num = int(self.frame_text.text()) + 1
            if (frame_num < self.total_frames):
                self.frame_text.setText(f'{frame_num}')
                frame_text = self.frame_text.text().zfill(6)
                cv_img = cv2.imread(f'{self.frames_folder}/image_{frame_text}.png')
                qt_img = backend.convert_cv_qt(cv_img)
                self.imagen_label.setPixmap(qt_img)
                self.video_slider.setSliderPosition(int(frame_text))
                cv2.waitKey(self.video_timer)
            else:
                self.play_state = False
            

    def on_frontFrame_button_clicked(self):
        # Save current frame
        # if labels: guardar

        frame_num = int(self.frame_text.text()) + 1
        if (frame_num < self.total_frames):
            self.frame_text.setText(f'{frame_num}')
            frame_text = self.frame_text.text().zfill(6)
            cv_img = cv2.imread(f'{self.frames_folder}/image_{frame_text}.png')
            qt_img = backend.convert_cv_qt(cv_img)
            self.imagen_label.setPixmap(qt_img)
            self.video_slider.setSliderPosition(int(frame_text))

    
    def on_fastPlay_button_clicked(self):
        if (self.video_timer - 10 > 0):
            self.video_timer -= 10


    def on_video_slider_sliderMoved(self):
        self.frame_text.setText(str(self.video_slider.value()))


    def on_video_slider_sliderReleased(self):
        frame_text = self.frame_text.text().zfill(6)
        cv_img = cv2.imread(f'{self.frames_folder}/image_{frame_text}.png')
        qt_img = backend.convert_cv_qt(cv_img)
        self.imagen_label.setPixmap(qt_img)


    def on_frame_text_returnPressed(self):
        frame_text = self.frame_text.text().zfill(6)
        cv_img = cv2.imread(f'{self.frames_folder}/image_{frame_text}.png')
        qt_img = backend.convert_cv_qt(cv_img)
        self.imagen_label.setPixmap(qt_img)
        self.video_slider.setSliderPosition(int(frame_text))
    

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec())
