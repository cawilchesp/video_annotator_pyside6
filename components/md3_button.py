"""
PySide6 Button component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QPushButton

from icon_color import icon_color

# --------------
# Common Buttons
# --------------
class MD3Button(QPushButton):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Common Buttons

        Parameters
        ----------
        attributes: dict
            position: tuple
                Button top left corner position
                (x, y)
            width: int
                Button width
            type: str
                Button type
                'filled', 'tonal', 'outlined', 'standard'
            icon: str (Optional)
                Icon name
            labels: tuple
                Button labels
                (label_spanish, label_english)
            enabled: bool
                Button enabled / disabled
            theme_color: str
                App theme color name
            language: int
                App language
                0: Spanish, 1: English
            clicked: def
                Button 'clicked' method name
        
        Returns
        -------
        None
        """
        super(MD3Button, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        w = attributes['width'] if 'width' in attributes else 32
        self.setGeometry(x, y, w, 32)
        self.setEnabled(attributes['enabled']) if 'enabled' in attributes else True
        
        if 'icon' in self.attributes:
            self.set_icon(attributes['theme_color'], attributes['icon'])
        if 'labels' in self.attributes:
            self.set_language(attributes['language'])
        self.setProperty(attributes['type'], True)

        self.clicked.connect(attributes['clicked'])


    def set_icon(self, color_name: str, icon_name: str):
        if self.attributes['type'] in ['filled', 'tonal']:
            color = 'black'
        elif self.attributes['type'] in ['outlined', 'standard']:
            color = color_name
        colorized_icon = icon_color(color, icon_name)
        self.setIcon(colorized_icon)


    def set_language(self, language: int) -> None:
        """ Change language of title text """
        if 'labels' in self.attributes:
            if language == 0:   self.setText(self.attributes['labels'][0])
            elif language == 1: self.setText(self.attributes['labels'][1])