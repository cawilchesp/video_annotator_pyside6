"""
PySide6 Button component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QPushButton

from icon_color import icon_color

# --------------
# Common Buttons
# --------------
class MD3ThemeButton(QPushButton):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Common Buttons

        Parameters
        ----------
        attributes: dict
            position: tuple
                Button top left corner position
                (x, y)
            type: str
                Button type
                'filled', 'tonal', 'outlined', 'standard'
            state: bool
                State of activation
                True: On, False: Off
            enabled: bool
                Button enabled / disabled
            theme_color: str
                App theme color name
            clicked: def
                Button 'clicked' method name
        
        Returns
        -------
        None
        """
        super(MD3ThemeButton, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        self.setGeometry(x, y, 32, 32)
        self.setEnabled(attributes['enabled']) if 'enabled' in attributes else True
        
        self.set_state(attributes['state'], attributes['theme_color'])
        self.setProperty(attributes['type'], True)

        self.clicked.connect(attributes['clicked'])


    def set_state(self, state: bool, color_name: str) -> None:
        """ Set chip state and corresponding icon """
        icon_name = 'light_mode' if state else 'dark_mode'

        if self.attributes['type'] in ['filled', 'tonal']:
            color = 'black'
        elif self.attributes['type'] in ['outlined', 'standard']:
            color = color_name
        colorized_icon = icon_color(color, icon_name)
        self.setIcon(colorized_icon)