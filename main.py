"""
Main

This file contains main UI class and methods to control components operations.
"""

from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QRubberBand
from PySide6.QtCore import QTimer, QRect, QSize, QPoint, Qt
from PySide6.QtGui import QPixmap, QColor

from ultralytics import YOLO
import supervision as sv

import sys
import yaml
from pathlib import Path

import cv2

from main_ui import UI
from dialogs.about_app import AboutApp
from dialogs.info_message import InfoMessageApp
from forms.project import NewProject
import backend

from tools.annotators import box_annotations

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
        self.project_folder = self.config['PROJECT_FOLDER']

        # ---------
        # Variables
        # ---------

        self.frames_folder = ''
        self.labeled_folder = ''
        self.resized_folder = ''

        self.video_width = None
        self.video_height = None
        self.video_total_frames = None
        self.video_fps = None
        self.aspect_ratio = 1.0

        self.timer_play = None
        self.timer_reverse = None

        self.time_step = 0
        self.frame_number = 0
        self.image_number = 0
        self.total_images = 0
        self.current_image = None

        self.projects_list = None
        self.project_info = None
        self.active_class = ''
        self.active_class_index = None
        self.active_color = ''

        self.rubberBand = None
        self.top_label = None
        self.left_label = None
        self.start_point = None
        self.end_point = None
        self.current_boxes = []

        self.mouse_selection_state = False
        self.box_button_state = False
        self.polygon_button_state = False
        self.drag_button_state = False

        # ---
        # GUI
        # ---
        self.ui = UI(self)
        theme = 'light' if self.theme_style else 'dark'
        theme_qss_file = f"themes/{self.theme_color}_{theme}_theme.qss"
        with open(theme_qss_file, "r") as theme_qss:
            self.setStyleSheet(theme_qss.read())

        # -------------
        # Load Projects
        # -------------
        self.projects_list = list(Path(self.project_folder).iterdir())
        for project_name in self.projects_list:
            self.ui.gui_widgets['projects_menu'].addItem(project_name.name)
        self.ui.gui_widgets['projects_menu'].setCurrentIndex(-1)

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
        """ Theme button control to change components stylesheet
        
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
        self.ui.gui_widgets['video_output_card'].resize(width - 392, height - 92)
        self.ui.gui_widgets['autolabelling_card'].move(width - 188, 84)

        frame_width = (self.ui.gui_widgets['video_output_card'].height() - 56) * self.aspect_ratio
        frame_height = self.ui.gui_widgets['video_output_card'].height() - 56
        if frame_width > self.ui.gui_widgets['video_output_card'].width() - 16:
            frame_width = self.ui.gui_widgets['video_output_card'].width() - 16
            frame_height = frame_width / self.aspect_ratio
        self.ui.gui_widgets['video_label'].resize(frame_width, frame_height)
                
        return super().resizeEvent(a0)

    # ------------------
    # Funciones Proyecto
    # ------------------
    def on_projects_changed(self) -> None:
        print(self.ui.gui_widgets['projects_menu'].currentIndex())


    def on_project_folder_button_clicked(self) -> None:
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

            # Menu
            self.projects_list = list(Path(self.project_folder).iterdir())
            for project_name in self.projects_list:
                self.ui.gui_widgets['projects_menu'].addItem(project_name.name)
            self.ui.gui_widgets['projects_menu'].setCurrentIndex(-1)
        else:
            self.info_app = InfoMessageApp({'size': (300, 100), 'type': 'error',
                'messages': ("No se seleccionó la carpeta de ubicación de los proyecto",
                             "The projects location folder wasn't selected") })
            self.info_app.exec()
    

    def on_project_new_button_clicked(self) -> None:
        """ Configure new project """
        self.new_window = NewProject()
        self.new_window.exec()

        self.project_info = self.new_window.project_data

        if self.project_info:
            # Información del proyecto
            project_name = self.project_info['project_name']
            video_file = self.project_info['video_file']
            project_folder = self.project_info['project_folder']
            classes = self.project_info['classes']
            frame_extraction = self.project_info['frame_extraction']

            # Creación de la carpeta del proyecto
            main_project_folder = Path(f'{project_folder}/{project_name}')
            if not main_project_folder.exists():
                main_project_folder.mkdir()

                # Creación de sub-carpetas
                self.frames_folder = Path(f'{project_folder}/{project_name}/frames')
                self.frames_folder.mkdir()

                self.labeled_folder = Path(f'{project_folder}/{project_name}/labels')
                self.labeled_folder.mkdir()

                self.resized_folder = Path(f'{project_folder}/{project_name}/resized')
                self.resized_folder.mkdir()

                # Extracción de frames del video
                self.total_images = backend.frame_extraction(video_file, self.frames_folder, self.labeled_folder, self.resized_folder, frame_extraction)

                # Extracción de información del video
                video_properties = backend.open_video(video_file)
                self.video_width = video_properties["width"]
                self.video_height = video_properties["height"]
                self.total_frames = video_properties['frame_count']
                self.video_fps = video_properties['fps']
                self.aspect_ratio = float(self.video_width / self.video_height)

                # Presentación de Información
                self.ui.gui_widgets['filename_value'].setText(f'{Path(video_file).name}')
                self.ui.gui_widgets['size_value'].setText(f'{self.video_width} X {self.video_height}')
                self.ui.gui_widgets['total_frames_value'].setText(f'{self.total_frames}')
                self.ui.gui_widgets['fps_value'].setText(f"{self.video_fps}")

                # Configuración de clases
                self.ui.gui_widgets['classes_menu'].clear()
                for class_name in classes.keys():
                    self.ui.gui_widgets['classes_menu'].addItem(class_name)

                # Configuración de barra de video
                self.ui.gui_widgets['video_slider'].setMaximum(self.total_images - 1)
                self.ui.gui_widgets['video_slider'].setEnabled(True)
                self.ui.gui_widgets['frame_value_textfield'].text_field.setText('0')
                self.ui.gui_widgets['zoom_value_textfield'].text_field.setText('100')

                # Timers
                self.timer_play = QTimer()
                self.timer_play.timeout.connect(self.play_forward)
                self.timer_reverse = QTimer()
                self.timer_reverse.timeout.connect(self.play_backward)

                # Presentación del frame 0
                self.draw_frame()
                frame_width = (self.ui.gui_widgets['video_output_card'].height() - 56) * self.aspect_ratio
                frame_height = self.ui.gui_widgets['video_output_card'].height() - 56
                if frame_width > self.ui.gui_widgets['video_output_card'].width() - 16:
                    frame_width = self.ui.gui_widgets['video_output_card'].width() - 16
                    frame_height = frame_width / self.aspect_ratio
                self.ui.gui_widgets['video_label'].resize(frame_width, frame_height)
            else:
                self.info_app = InfoMessageApp({'size': (300, 100), 'type': 'warning',
                    'messages': ("La carpeta ya existe",
                                "Folder already exists") })
                self.info_app.exec()

    # --------------------
    # Funciones Etiquetado
    # --------------------
    def on_classes_changed(self, index):
        classes = self.project_info['classes']
        self.active_class = self.ui.gui_widgets['classes_menu'].currentText()
        self.active_class_index = index
        self.active_color = classes[self.active_class]
        self.ui.gui_widgets['class_color_label'].set_color_label(self.active_color)


    def on_drag_button_clicked(self):
        self.drag_button_state = not self.drag_button_state
        if self.drag_button_state:
            self.ui.gui_widgets['drag_button'].setStyleSheet('border-width: 3px; border-color: hsl(348, 100%, 61%)')
            self.ui.gui_widgets['video_label'].setCursor(Qt.CursorShape.OpenHandCursor)
            self.mouse_selection_state = True
        else:
            self.ui.gui_widgets['drag_button'].setStyleSheet('border-width: 0px')
            self.ui.gui_widgets['video_label'].setCursor(Qt.CursorShape.ArrowCursor)
            self.mouse_selection_state = False
        

    def on_polygon_button_clicked(self):
        self.polygon_button_state = not self.polygon_button_state
        if self.polygon_button_state:
            self.ui.gui_widgets['polygon_button'].setStyleSheet('border-width: 3px; border-color: hsl(348, 100%, 61%)')
            self.ui.gui_widgets['video_label'].setCursor(Qt.CursorShape.CrossCursor)
            self.mouse_selection_state = True
        else:
            self.ui.gui_widgets['polygon_button'].setStyleSheet('border-width: 0px')
            self.ui.gui_widgets['video_label'].setCursor(Qt.CursorShape.ArrowCursor)
            self.mouse_selection_state = False
        

    def on_box_button_clicked(self):
        self.box_button_state = not self.box_button_state
        if self.box_button_state:
            self.ui.gui_widgets['box_button'].setStyleSheet('border-width: 3px; border-color: hsl(348, 100%, 61%)')
            self.ui.gui_widgets['video_label'].setCursor(Qt.CursorShape.CrossCursor)
            self.mouse_selection_state = True
        else:
            self.ui.gui_widgets['box_button'].setStyleSheet('border-width: 0px')
            self.ui.gui_widgets['video_label'].setCursor(Qt.CursorShape.ArrowCursor)
            self.mouse_selection_state = False
    
    # ---------------
    # Funciones Mouse
    # ---------------
    def mousePressEvent(self, event):
        if self.mouse_selection_state:
            self.top_label = self.ui.gui_widgets['video_output_card'].y() + 48
            self.left_label = self.ui.gui_widgets['video_output_card'].x() + 8

            self.start_point = QPoint(event.position().x() - self.left_label, event.position().y() - self.top_label)

            if ((0 < self.start_point.x() < self.ui.gui_widgets['video_label'].width()) and 
                (0 < self.start_point.y() < self.ui.gui_widgets['video_label'].height())):
                if not self.rubberBand:
                    self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self.ui.gui_widgets['video_label'])
                self.rubberBand.setGeometry(QRect(self.start_point, QSize()))
                self.rubberBand.show()

    def mouseMoveEvent(self, event):
        # Se debe definir no el end point sino el next point
        # Si es un box, solo son 2 puntos
        # Si es un polygon, se debe definir cuál va a ser el end point
        if self.rubberBand:
            self.end_point = QPoint(event.position().x() - self.left_label, event.position().y() - self.top_label)
            if self.end_point.x() < 0:
                self.end_point.setX(0)
            elif self.end_point.x() > self.ui.gui_widgets['video_label'].width() - 1:
                self.end_point.setX(self.ui.gui_widgets['video_label'].width() - 1)
            if self.end_point.y() < 0:
                self.end_point.setY(0)
            elif self.end_point.y() > self.ui.gui_widgets['video_label'].height() - 1:
                self.end_point.setY(self.ui.gui_widgets['video_label'].height() - 1)
            self.rubberBand.setGeometry(QRect(self.start_point, self.end_point).normalized())

    def mouseReleaseEvent(self, event):
        # Como el release se activa al soltar el mouse, depende de la herramienta
        # seleccionada, por lo tanto, se deben definir las condiciones de cuándo
        # pintar
        # Si es un box, al soltar, se tendrán ya los 2 puntos y se pintan todos
        # los cuadros
        # Si es un polygon, al soltar, se debe pensar cómo iniciar el siguiente
        # punto. Por eso, se debe pensar si usar QRubberBand para realizar el 
        # dibujo, o si se cambia a la forma anterior, donde solo se marcan los puntos
        # sin necesidad de un QRubberBand
        # Investigar si hay otros rubber bands
        

        if self.rubberBand:
            self.rubberBand.hide()

            qt_image = self.convert_cv_qt(self.current_image)
            painter = QtGui.QPainter(qt_image)
            
            bounding_box = self.image_coordinates(self.start_point, self.end_point)
            self.current_boxes.append([self.active_class_index, bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]])

            for box in self.current_boxes:
                class_index = box[0]
                left = int((box[1] - box[3]/2) * self.video_width)
                top = int((box[2] - box[4]/2) * self.video_height)
                right = int((box[1] + box[3]/2) * self.video_width)
                bottom = int((box[2] + box[4]/2) * self.video_height)

                classes = self.project_info['classes']
                classes_keys = list(classes.keys())
                color_rgb = QColor.fromString(classes[classes_keys[class_index]])
                pen = QtGui.QPen()
                pen.setWidth(1)
                pen.setColor(color_rgb)
                painter.setPen(pen)

                if self.box_button_state:
                    painter.drawRect(QRect(QPoint(left,top), QPoint(right,bottom)))

            painter.end()
            self.ui.gui_widgets['video_label'].setPixmap(qt_image)

    def image_coordinates(self, point_1: QPoint, point_2: QPoint):
        point_1_x = point_1.x() / self.ui.gui_widgets['video_label'].width()
        point_1_y = point_1.y() / self.ui.gui_widgets['video_label'].height()
        point_2_x = point_2.x() / self.ui.gui_widgets['video_label'].width()
        point_2_y = point_2.y() / self.ui.gui_widgets['video_label'].height()

        box_x_center = (point_1_x + point_2_x) / 2
        box_y_center = (point_1_y + point_2_y) / 2
        box_width = abs(point_2_x - point_1_x)
        box_height = abs(point_2_y - point_1_y)

        return (box_x_center, box_y_center, box_width, box_height)
    
    # ------------------
    # Funciones Opciones
    # ------------------
    def on_minus_button_clicked(self):
        return None

    def on_zoom_value_textfield_returnPressed(self):
        return None
    
    def on_plus_button_clicked(self):
        return None
    
    def on_undo_button_clicked(self):
        return None

    def on_redo_button_clicked(self):
        return None
        
    # ------------------------
    # Funciones Autoetiquetado
    # ------------------------

    def on_models_changed(self):
        return None

    def on_autobox_button_clicked(self):
        return None

    def on_autopolygon_button_clicked(self):
        return None

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
        self.image_number = self.ui.gui_widgets['video_slider'].value()
        self.ui.gui_widgets['frame_value_textfield'].text_field.setText(f"{self.image_number}")
        

    def on_video_slider_sliderReleased(self) -> None:
        self.draw_frame()


    def on_frame_value_textfield_returnPressed(self) -> None:
        self.image_number = int(self.ui.gui_widgets['frame_value_textfield'].text_field.text())
        if self.image_number < 0:
            self.image_number = 0
        elif self.image_number >= self.total_images:
            self.image_number = self.total_images - 1

        self.ui.gui_widgets['frame_value_textfield'].text_field.setText(f"{self.image_number}")    
        self.ui.gui_widgets['video_slider'].setSliderPosition(self.image_number)
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
        frame_text = f'{self.image_number}'.zfill(6)
        self.current_image = cv2.imread(f"{self.frames_folder}/image_{frame_text}.png")
        qt_image = self.convert_cv_qt(self.current_image)
        self.ui.gui_widgets['video_label'].setPixmap(qt_image)


    def autobox_detections(self):
        model = YOLO(f"weights/yolov8m.pt")
        annotated_image = self.current_image.copy()
        class_filter = [0,1,2,3,5,7]
        # Run YOLOv8 inference
        results = self.model(
            source=self.current_image,
            imgsz=640,
            conf=0.5,
            device=0,
            agnostic_nms=True,
            classes=class_filter,
            retina_masks=True,
            verbose=False
        )[0]

        detections = sv.Detections.from_ultralytics(results)

        # Draw labels
        labels = [f"{results.names[class_id]} - {tracker_id}" for _, _, _, class_id, tracker_id in detections]

        # Draw boxes
        annotated_image = box_annotations(annotated_image, detections, labels)

        # # Draw masks
        # if detections.mask is not None:
        #     annotated_image = mask_annotations(annotated_image, detections)
        
        # # Draw tracks
        # annotated_image = track_annotations(annotated_image, tracks, self.track_deque, 'centroid')

        # qt_image = self.convert_cv_qt(annotated_image)
        # self.ui.gui_widgets['video_label'].setPixmap(qt_image)


    def play_forward(self):
        if (self.image_number < self.total_images - 1):
            self.image_number += 1
            self.draw_frame()

            self.ui.gui_widgets['video_slider'].setValue(self.image_number)
            self.ui.gui_widgets['frame_value_textfield'].text_field.setText(f"{self.image_number}")
        else:
            if self.timer_play.isActive(): self.timer_play.stop()


    def play_backward(self):
        if (self.image_number > 0):
            self.image_number -= 1
            self.draw_frame()

            self.ui.gui_widgets['video_slider'].setValue(self.image_number)
            self.ui.gui_widgets['frame_value_textfield'].text_field.setText(f"{self.image_number}")
        else:
            if self.timer_reverse.isActive(): self.timer_reverse.stop()
    

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
