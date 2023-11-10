"""
PySide6 Chip component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QToolButton
from PySide6.QtCore import Qt

from icon_color import icon_color

# ----
# Chip
# ----
class MD3Chip(QToolButton):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Chip

        Parameters
        ----------
        attributes: dict
            position: tuple
                Chip top left corner position
                (x, y)
            width: int
                Chip width
            labels: tuple
                Chip labels
                (label_spanish, label_english)
            icon: str (Optional)
                Icon name
            state: bool
                State of activation
                True: On, False: Off
            enabled: bool
                Chip enabled / disabled
            theme_color: str
                App theme color name
            language: int
                App language
                0: Spanish, 1: English
            clicked: def
                Chip 'clicked' method name
        
        Returns
        -------
        None
        """
        super(MD3Chip, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        w = attributes['width'] if 'width' in attributes else 32
        self.setGeometry(x, y, w, 32)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setCheckable(True)
        self.setEnabled(attributes['enabled']) if 'enabled' in attributes else True

        self.set_state(attributes['state'], attributes['theme_color'])
        self.set_language(attributes['language'])

        self.clicked.connect(attributes['clicked'])

        
    def set_state(self, state: bool, color_name: str) -> None:
        """ Set chip state and corresponding icon """
        self.setChecked(state)
        icon_name = self.attributes['icon'] if 'icon' in self.attributes else 'none'
        if state:
            icon_name = 'done'
            color = 'black'
        else:
            color = color_name
        colorized_icon = icon_color(color, icon_name)
        self.setIcon(colorized_icon)


    def set_language(self, language: int) -> None:
        """ Change language of label text """
        if language == 0:   self.setText(self.attributes['labels'][0])
        elif language == 1: self.setText(self.attributes['labels'][1])