from PySide6.QtWidgets import QWidget

from components.md3_button import MD3Button
from components.md3_card import MD3Card
from components.md3_chip import MD3Chip
from components.md3_datepicker import MD3DatePicker
from components.md3_divider import MD3Divider
from components.md3_imagelabel import MD3ImageLabel
from components.md3_label import MD3Label
from components.md3_menu import MD3Menu
from components.md3_segmentedbutton import MD3SegmentedButton
from components.md3_themebutton import MD3ThemeButton
from components.md3_slider import MD3Slider
from components.md3_switch import MD3Switch
from components.md3_textfield import MD3TextField
from components.md3_window import MD3Window

import yaml


class UI(QWidget):
    def __init__(self, parent):
        super(UI, self).__init__(parent)

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
        self.gui_widgets = {}

        # -----------
        # Main Window
        # -----------
        (width, height) = (1300, 700)
        self.gui_widgets['main_window'] = MD3Window( {
            'parent': parent,
            'size': (width, height),
            'minimum_size': (width, height),
            'labels': ('Anotador de Video', 'Video Annotator'),
            'language': self.language_value } )

        # -------
        # Options
        # -------
        self.gui_widgets['options_divider'] = MD3Divider(parent, {
            'length': 180,
            'shape': 'horizontal' } )

        self.gui_widgets['language_menu'] = MD3Menu(parent, {
            'width': 72,
            'type': 'outlined',
            'options': {0: ('ESP', 'SPA'), 1: ('ING', 'ENG')},
            'set': self.language_value,
            'language': self.language_value,
            'index_changed': parent.on_language_changed } )

        self.gui_widgets['theme_button'] = MD3ThemeButton(parent, {
            'type': 'filled',
            'state': self.theme_style,
            'theme_color': self.theme_color,
            'clicked': parent.on_theme_clicked } )
        
        self.gui_widgets['about_button'] = MD3Button(parent, {
            'type': 'filled',
            'icon': 'mail',
            'theme_color': self.theme_color,
            'clicked': parent.on_about_button_clicked } )


        # -----------
        # Card Source
        # -----------
        self.gui_widgets['project_card'] = MD3Card(parent, {
            'position': (8, 8),
            'size': (180, 88),
            'type': 'outlined',
            'titles': ('Proyecto', 'Project'),
            'language': self.language_value } )
        
        self.gui_widgets['project_new_button'] = MD3Button(self.gui_widgets['project_card'], {
            'position': (140, 48),
            'type': 'filled',
            'icon': 'new',
            'theme_color': self.theme_color,
            'clicked': parent.on_project_new_button_clicked } )

        # ----------------
        # Card Information
        # ----------------
        self.gui_widgets['info_card'] = MD3Card(parent, {
            'position': (8, 104),
            'size': (180, 176),
            'type': 'outlined',
            'titles': ('Información', 'Information'),
            'language': self.language_value } )

        self.gui_widgets['source_icon'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (8, 48),
            'type': 'icon',
            'icon': 'cam',
            'theme_color': self.theme_color } )
        
        self.gui_widgets['filename_value'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (48, 56), 
            'width': 124,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Nombre del archivo', 'File Name'),
            'language': self.language_value } )

        self.gui_widgets['size_icon'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (8, 80),
            'type': 'icon',
            'icon': 'size',
            'theme_color': self.theme_color } )

        self.gui_widgets['size_value'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (48, 88),
            'width': 124,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Ancho X Alto', 'Width X Height'),
            'language': self.language_value } )
        
        self.gui_widgets['total_frames_icon'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (8, 112),
            'type': 'icon',
            'icon': 'number',
            'theme_color': self.theme_color } )

        self.gui_widgets['total_frames_value'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (48, 120),
            'width': 124,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('Total de Cuadros', 'Total Frames'),
            'language': self.language_value } )

        self.gui_widgets['fps_icon'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (8, 144),
            'type': 'icon',
            'icon': 'fps',
            'theme_color': self.theme_color } )

        self.gui_widgets['fps_value'] = MD3Label(self.gui_widgets['info_card'], {
            'position': (48, 152),
            'width': 124,
            'type': 'subtitle',
            'align': 'left',
            'labels': ('CPS', 'FPS'),
            'language': self.language_value } )

        # --------------
        # Card Labelling
        # --------------
        self.gui_widgets['labelling_card'] = MD3Card(parent, { 
            'position': (8, 288),
            'size': (180, 128),
            'type': 'outlined',
            'titles': ('Etiquetado', 'Labelling'),
            'language': self.language_value } )
        
        self.gui_widgets['classes_menu'] = MD3Menu(self.gui_widgets['labelling_card'], {
            'position': (8, 48),
            'width': 124,
            'type': 'outlined',
            'set': -1,
            'language': self.language_value,
            'index_changed': parent.on_language_changed } )
        
        self.gui_widgets['class_color_label'] = MD3Label(self.gui_widgets['labelling_card'], {
            'position': (140, 48),
            'type': 'color',
            'color': '#ffffff',
            'theme_color': self.theme_color } )
        
        self.gui_widgets['drag_button'] = MD3Button(self.gui_widgets['labelling_card'], {
            'position': (60, 88),
            'type': 'filled',
            'icon': 'drag',
            'theme_color': self.theme_color,
            'clicked': parent.on_drag_button_clicked } )
        
        self.gui_widgets['polygon_button'] = MD3Button(self.gui_widgets['labelling_card'], {
            'position': (100, 88),
            'type': 'filled',
            'icon': 'polygon',
            'theme_color': self.theme_color,
            'clicked': parent.on_polygon_button_clicked } )
        
        self.gui_widgets['box_button'] = MD3Button(self.gui_widgets['labelling_card'], {
            'position': (140, 88),
            'type': 'filled',
            'icon': 'square',
            'theme_color': self.theme_color,
            'clicked': parent.on_box_button_clicked } )

        # ----------------------
        # Card Labelling Options
        # ----------------------
        self.gui_widgets['options_card'] = MD3Card(parent, { 
            'position': (8, 424),
            'size': (180, 148),
            'type': 'outlined',
            'titles': ('Opciones', 'Options'),
            'language': self.language_value } )

        self.gui_widgets['minus_button'] = MD3Button(self.gui_widgets['options_card'], {
            'position': (8, 60),
            'type': 'filled',
            'icon': 'minus',
            'theme_color': self.theme_color,
            'clicked': parent.on_minus_button_clicked } )

        self.gui_widgets['zoom_value_textfield'] = MD3TextField(self.gui_widgets['options_card'], {
            'position': (48, 48),
            'width': 84,
            'type': 'outlined',
            'labels': ('Zoom', 'Zoom'),
            'input': 'integer',
            'language': self.language_value,
            'return_pressed': parent.on_zoom_value_textfield_returnPressed } )

        self.gui_widgets['plus_button'] = MD3Button(self.gui_widgets['options_card'], {
            'position': (140, 60),
            'type': 'filled',
            'icon': 'new',
            'theme_color': self.theme_color,
            'clicked': parent.on_plus_button_clicked } )
        
        self.gui_widgets['undo_button'] = MD3Button(self.gui_widgets['options_card'], {
            'position': (100, 108),
            'type': 'filled',
            'icon': 'undo',
            'theme_color': self.theme_color,
            'clicked': parent.on_undo_button_clicked } )

        self.gui_widgets['redo_button'] = MD3Button(self.gui_widgets['options_card'], {
            'position': (140, 108),
            'type': 'filled',
            'icon': 'redo',
            'theme_color': self.theme_color,
            'clicked': parent.on_redo_button_clicked } )

        # -------------------
        # Card Auto-Labelling
        # -------------------
        self.gui_widgets['autolabelling_card'] = MD3Card(parent, {
            'size': (180, 128),
            'type': 'outlined',
            'titles': ('Autoetiquetado', 'Autolabelling'),
            'language': self.language_value } )
        
        self.gui_widgets['models_menu'] = MD3Menu(self.gui_widgets['autolabelling_card'], {
            'position': (8, 48),
            'width': 164,
            'type': 'outlined',
            'set': -1,
            'language': self.language_value,
            'index_changed': parent.on_models_changed } )
        
        self.gui_widgets['autobox_button'] = MD3Button(self.gui_widgets['autolabelling_card'], {
            'position': (100, 88),
            'type': 'filled',
            'icon': 'square_plus',
            'theme_color': self.theme_color,
            'clicked': parent.on_autobox_button_clicked } )
        
        self.gui_widgets['autopolygon_button'] = MD3Button(self.gui_widgets['autolabelling_card'], {
            'position': (140, 88),
            'type': 'filled',
            'icon': 'polygon_plus',
            'theme_color': self.theme_color,
            'clicked': parent.on_autopolygon_button_clicked } )

        # ------------------
        # Card Video Toolbar
        # ------------------
        self.gui_widgets['video_toolbar_card'] = MD3Card(parent, {
            'position': (196, 8),
            'type': 'outlined',
            'language': self.language_value } )

        self.gui_widgets['backFrame_button'] = MD3Button(self.gui_widgets['video_toolbar_card'], {
            'position': (8, 20),
            'type': 'filled',
            'icon': 'step_backward', 
            'enabled': True,
            'theme_color': self.theme_color,
            'clicked': parent.on_backFrame_button_clicked } )

        self.gui_widgets['reverse_button'] = MD3Button(self.gui_widgets['video_toolbar_card'], {
            'position': (48, 20),
            'type': 'filled',
            'icon': 'reverse', 
            'enabled': True,
            'theme_color': self.theme_color,
            'clicked': parent.on_reverse_button_clicked } )

        self.gui_widgets['pause_button'] = MD3Button(self.gui_widgets['video_toolbar_card'], {
            'position': (88, 20),
            'type': 'filled',
            'icon': 'pause', 
            'enabled': True,
            'theme_color': self.theme_color,
            'clicked': parent.on_pause_button_clicked } )

        self.gui_widgets['play_button'] = MD3Button(self.gui_widgets['video_toolbar_card'], {
            'position': (128, 20),
            'type': 'filled',
            'icon': 'play', 
            'enabled': True,
            'theme_color': self.theme_color,
            'clicked': parent.on_play_button_clicked } )

        self.gui_widgets['frontFrame_button'] = MD3Button(self.gui_widgets['video_toolbar_card'], {
            'position': (168, 20),
            'type': 'filled',
            'icon': 'step_forward', 
            'enabled': True,
            'theme_color': self.theme_color,
            'clicked': parent.on_frontFrame_button_clicked } )

        self.gui_widgets['video_slider'] = MD3Slider(self.gui_widgets['video_toolbar_card'], {
            'position': (208, 20),
            'range': (0, 1, 10),
            'value': 0,
            'enabled': False,
            'slider_moved': parent.on_video_slider_sliderMoved,
            'slider_released': parent.on_video_slider_sliderReleased } )

        self.gui_widgets['frame_value_textfield'] = MD3TextField(self.gui_widgets['video_toolbar_card'], {
            'width': 100,
            'type': 'outlined',
            'labels': ('Cuadro', 'Frame'),
            'input': 'integer',
            'language': self.language_value,
            'return_pressed': parent.on_frame_value_textfield_returnPressed } )

        # ----------------
        # Card Video Image
        # ----------------
        self.gui_widgets['video_output_card'] = MD3Card(parent, {
            'position': (196, 84),
            'type': 'outlined',
            'titles': ('Salida del Video','Video Output'),
            'language': self.language_value } )
        
        self.gui_widgets['video_label'] = MD3ImageLabel(self.gui_widgets['video_output_card'], {
            'position': (8, 48),
            'scaled_image': True } )