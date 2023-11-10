"""
PySide6 Icon Button component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QFrame, QToolButton
from PySide6.QtCore import Qt, QSize

from icon_color import icon_color

# ------
# Switch
# ------
class MD3Switch(QFrame):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Switch

        Parameters
        ----------
        attributes: dict
            position: tuple
                Button top left corner position
                (x, y)
            state: bool
                State of activation
                True: On, False: Off
            enabled: bool
                Switch enabled / disabled
            theme_color: str
                App theme color name
            clicked: def
                Switch 'clicked' method name
        
        Returns
        -------
        None
        """
        super(MD3Switch, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (0, 0)
        self.setGeometry(x, y, 52, 32)

        self.left_switch = QToolButton(self)
        self.left_switch.setGeometry(0, 0, 26, 32)
        self.left_switch.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.left_switch.setCheckable(True)
        self.left_switch.setEnabled(attributes['enabled']) if 'enabled' in attributes else True

        self.right_switch = QToolButton(self)
        self.right_switch.setGeometry(26, 0, 26, 32)
        self.right_switch.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.right_switch.setCheckable(True)
        self.right_switch.setEnabled(attributes['enabled']) if 'enabled' in attributes else True

        self.left_switch.setProperty('left', True)
        self.right_switch.setProperty('right', True)
        self.set_state(attributes['state'], attributes['theme_color'])

        self.left_switch.clicked.connect(attributes['clicked'])
        self.right_switch.clicked.connect(attributes['clicked'])
        

    def set_state(self, state: bool, color_name: str) -> None:
        """ Set button state and corresponding icon """
        
        self.left_switch.setChecked(state)
        self.right_switch.setChecked(state)
        icon_state = {
            True: { 'left': 'none', 'right': 'circle_checked' },
            False: { 'left': 'circle', 'right': 'none' }
        }
        icon_left_name = icon_state[state]['left']
        icon_right_name = icon_state[state]['right']
        color = 'black' if state else color_name
        colorized_left_icon = icon_color(color, icon_left_name)
        colorized_right_icon = icon_color(color, icon_right_name)
        self.left_switch.setIcon(colorized_left_icon)
        self.right_switch.setIcon(colorized_right_icon)
        self.left_switch.setIconSize(QSize(16,16))
        self.right_switch.setIconSize(QSize(16,16))