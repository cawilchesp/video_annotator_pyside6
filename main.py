"""
Main

This file contains main UI class and methods to control components operations.
"""

from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap

import sys
import yaml
import pathlib

import cv2

from main_ui import UI
from dialogs.about_app import AboutApp
import backend
import project

# For debugging
from icecream import ic


class MainWindow(QMainWindow):
    def __init__(self):
        """ UI main application """
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

        # self.frames_folder = ''
        # self.labeled_folder = ''
        # self.resized_folder = ''

        self.cap = None
        self.video_width = None
        self.video_height = None
        self.video_total_frames = None
        self.video_fps = None
        self.aspect_ratio = 1.0

        self.timer_play = None
        self.timer_reverse = None

        self.time_step = 0
        self.frame_number = 0

        # self.project_info = None
        # self.active_class = ''
        # self.active_color = ''

        # ---
        # GUI
        # ---
        self.ui = UI(self)
        theme = 'light' if self.theme_style else 'dark'
        theme_qss_file = f"themes/{self.theme_color}_{theme}_theme.qss"
        with open(theme_qss_file, "r") as theme_qss:
            self.setStyleSheet(theme_qss.read())

        



        # # -----------
        # # Card Clases
        # # -----------
        # self.clases_card = mt3.Card(self, 'clases_card',
        #     (8, 418, 180, 88), ('Clases', 'Classes'), 
        #     self.theme_value, self.language_value)

        # y_3 = 48
        # self.clases_menu = mt3.Menu(self.clases_card, 'clases_menu',
        #     (8, y_3, 124), 10, 10, {}, self.theme_value, self.language_value)
        # self.clases_menu.currentIndexChanged.connect(self.on_clases_menu_currentIndexChanged)
        
        # self.color_label = mt3.ColorLabel(self.clases_card, 'color_label',
        #     (140, y_3), '0,0,0')
        
        # # -----------
        # # Card Formas
        # # -----------
        # self.formas_card = mt3.Card(self, 'formas_card',
        #     (8, 514, 180, 128), ('Formas', 'Shapes'), 
        #     self.theme_value, self.language_value)
        
        # y_4 = 48
        # self.rectangulo_button = mt3.IconButton(self.formas_card, 'rectangulo_button',
        #     (25, y_4), 'rectangle.png', self.theme_value)
        # self.rectangulo_button.clicked.connect(self.on_rectangulo_button_clicked)

        # self.elipse_button = mt3.IconButton(self.formas_card, 'elipse_button',
        #     (80, y_4), 'elipse.png', self.theme_value)
        
        # self.poligono_button = mt3.IconButton(self.formas_card, 'poligono_button',
        #     (135, y_4), 'poligono.png', self.theme_value)
        
        # y_4 += 40
        # self.linea_button = mt3.IconButton(self.formas_card, 'linea_button',
        #     (25, y_4), 'linea.png', self.theme_value)
        
        # self.punto_button = mt3.IconButton(self.formas_card, 'punto_button',
        #     (80, y_4), 'punto.png', self.theme_value)
        
        # self.cuboide_button = mt3.IconButton(self.formas_card, 'cuboide_button',
        #     (135, y_4), 'cuboid.png', self.theme_value)

        
        # # -------------
        # # Card Opciones
        # # -------------
        # self.opciones_card = mt3.Card(self, 'opciones_card',
        #     (1520, 70, 180, 130), ('Opciones', 'Options'), 
        #     self.theme_value, self.language_value)
        
        # y_5 = 48
        # self.guardar_button = mt3.IconButton(self.opciones_card, 'guardar_button',
        #     (25, y_5), 'save.png', self.theme_value)
        
        # self.deshacer_button = mt3.IconButton(self.opciones_card, 'deshacer_button',
        #     (80, y_5), 'undo.png', self.theme_value)
        
        # self.roi_button = mt3.IconButton(self.opciones_card, 'roi_button',
        #     (135, y_5), 'roi.png', self.theme_value)
        
        # y_5 += 40
        # self.aumentar_button = mt3.IconButton(self.opciones_card, 'aumentar_button',
        #     (50, y_5), 'zoom_in.png', self.theme_value)

        # self.tamanoNormal_button = mt3.IconButton(self.opciones_card, 'tamanoNormal_button',
        #     (110, y_5), 'zoom_out.png', self.theme_value)

        # # ----------------
        # # Card Anotaciones
        # # ----------------
        # self.anotaciones_card = mt3.Card(self, 'anotaciones_card',
        #     (1520, 200, 180, 820), ('Anotaciones', 'Annotations'), 
        #     self.theme_value, self.language_value)
        

    # -----------------
    # Options Functions
    # -----------------
    def on_language_changed(self, index: int) -> None:
        """ Language menu control to change components text language
        
        Parameters
        ----------
        index: int
            Index of language menu control
        
        Returns
        -------
        None
        """
        for key in self.ui.gui_widgets.keys():
            if hasattr(self.ui.gui_widgets[key], 'set_language'):
                self.ui.gui_widgets[key].set_language(index)
        
        self.language_value = index
        self.config['LANGUAGE'] = index
        with open(self.settings_file, 'w') as file:
            yaml.dump(self.config, file)


    def on_theme_clicked(self) -> None:
        """ Dark theme segmented control to change components stylesheet
        
        """
        state = not self.theme_style
        theme = 'light' if state else 'dark'
        theme_qss_file = f"themes/{self.theme_color}_{theme}_theme.qss"
        with open(theme_qss_file, "r") as theme_qss:
            self.setStyleSheet(theme_qss.read())
        self.ui.gui_widgets['theme_button'].set_state(state, self.theme_color)

        # Save settings
        self.theme_style = state
        self.config['THEME_STYLE'] = state
        with open(self.settings_file, 'w') as file:
            yaml.dump(self.config, file)


    def on_about_button_clicked(self) -> None:
        """ About app button to open about app window dialog """
        self.about_app = AboutApp()
        self.about_app.exec()


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """ Resize event to control size and position of app components """
        width = self.geometry().width()
        height = self.geometry().height()

        self.ui.gui_widgets['options_divider'].move(8, height - 49)
        self.ui.gui_widgets['language_menu'].move(8, height - 40)
        self.ui.gui_widgets['theme_button'].move(88, height - 40)
        self.ui.gui_widgets['about_button'].move(128, height - 40)

        self.ui.gui_widgets['video_toolbar_card'].resize(width - 204, 68)
        self.ui.gui_widgets['video_slider'].resize(self.ui.gui_widgets['video_toolbar_card'].width() - 324, 32)
        self.ui.gui_widgets['frame_value_textfield'].move(self.ui.gui_widgets['video_toolbar_card'].width() - 108, 8)

        self.ui.gui_widgets['video_output_card'].resize(width - 204, height - 92)

        frame_width = (self.ui.gui_widgets['video_output_card'].height() - 56) * self.aspect_ratio
        frame_height = self.ui.gui_widgets['video_output_card'].height() - 56
        if frame_width > self.ui.gui_widgets['video_output_card'].width() - 16:
            frame_width = self.ui.gui_widgets['video_output_card'].width() - 16
            frame_height = frame_width / self.aspect_ratio
        self.ui.gui_widgets['video_label'].resize(frame_width, frame_height)
        
    #     self.opciones_card.setGeometry(width - 188, 64, 180, 128)
    #     self.anotaciones_card.setGeometry(width - 188, 200, 180, height - 208)
        
        return super().resizeEvent(a0)

    # ------------------
    # Funciones Proyecto
    # ------------------
    def on_project_new_button_clicked(self) -> None:
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



    # -------------
    # Video Toolbar
    # -------------
    def on_backFrame_button_clicked(self) -> None:
        if self.timer_play.isActive(): self.timer_play.stop()
        if self.timer_reverse.isActive(): self.timer_reverse.stop()
        self.play_backward()


    def on_reverse_button_clicked(self) -> None:
        if self.timer_play.isActive(): self.timer_play.stop()
        self.timer_reverse.start(self.time_step)


    def on_pause_button_clicked(self) -> None:
        self.timer_play.stop() if self.timer_play.isActive() else self.timer_reverse.stop()


    def on_play_button_clicked(self) -> None:
        if self.timer_reverse.isActive(): self.timer_reverse.stop()
        self.timer_play.start(self.time_step)


    def on_frontFrame_button_clicked(self) -> None:
        if self.timer_play.isActive(): self.timer_play.stop()
        if self.timer_reverse.isActive(): self.timer_reverse.stop()
        self.play_forward()


    def on_video_slider_sliderMoved(self) -> None:
        self.frame_number = self.ui.gui_widgets['video_slider'].value()
        self.ui.gui_widgets['frame_value_textfield'].text_field.setText(f"{self.frame_number}")
        

    def on_video_slider_sliderReleased(self) -> None:
        self.draw_frame()


    def on_frame_value_textfield_returnPressed(self) -> None:
        self.frame_number = int(self.ui.gui_widgets['frame_value_textfield'].text_field.text())
        self.ui.gui_widgets['video_slider'].setSliderPosition(self.frame_number)
        self.draw_frame()


    # ---------
    # Functions
    # ---------
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        return QPixmap.fromImage(convert_to_qt_format)


    def draw_frame(self):
        return None
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
        # _, image = self.cap.read()
        # annotated_image = image.copy()
        
        # class_filter = [ value[1] for value in self.class_options.values() if value[0] ]
        
        # # Run YOLOv8 inference
        # results = self.yolov8_model(
        #     source=image,
        #     imgsz=640,
        #     conf=0.5,
        #     device=0,
        #     agnostic_nms=True,
        #     classes=class_filter,
        #     retina_masks=True,
        #     verbose=False
        # )[0]

        # detections = sv.Detections.from_ultralytics(results)

        # tracks = self.byte_tracker.update_with_detections(detections)

        # for track in tracks:
        #     if track[4] not in self.track_deque:
        #         self.track_deque[track[4]] = deque(maxlen=64)

        # # Draw labels
        # labels = [f"{results.names[class_id]} - {tracker_id}" for _, _, _, class_id, tracker_id in tracks]

        # # Draw boxes
        # annotated_image = box_annotations(annotated_image, tracks, labels)

        # # Draw masks
        # if detections.mask is not None:
        #     annotated_image = mask_annotations(annotated_image, detections)
        
        # # Draw tracks
        # annotated_image = track_annotations(annotated_image, tracks, self.track_deque, 'centroid')

        # qt_image = self.convert_cv_qt(annotated_image)
        # self.ui.gui_widgets['video_label'].setPixmap(qt_image)


    def play_forward(self):
        if (self.frame_number <= self.video_total_frames):
            self.frame_number += 1
            self.draw_frame()

            self.ui.gui_widgets['video_slider'].setValue(self.frame_number)
            self.ui.gui_widgets['frame_value_textfield'].text_field.setText(f"{self.frame_number}")


    def play_backward(self):
        if (self.frame_number > 0):
            self.frame_number -= 1
            self.draw_frame()

            self.ui.gui_widgets['video_slider'].setValue(self.frame_number)
            self.ui.gui_widgets['frame_value_textfield'].text_field.setText(f"{self.frame_number}")
    

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
