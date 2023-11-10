"""
PySide6 Text Field component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QFrame, QLineEdit, QLabel
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression, Qt

from icon_color import icon_color

# ----------
# Text Field
# ----------
class MD3TextField(QFrame):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Text Field

        Parameters
        ----------
        attributes: dict
            position: tuple
                Text field top left corner position
                (x, y)
            width: int
                Text field width
            type: str
                Text field type
                'filled', 'outlined'
            input: str (optional, any character allowed if not specified)
                Text field type
                    'text':      only letters and accents
                    'integer':   only integer numbers
                    'double':    allow decimal point
                    'weight':    double values from 0.00 to 999.99
                    'height_si': double values from 0.00 to 2.99
                    'height_us': number in format [ft]'[in]" (ex. 5'12")
                    'email':     text in email format
                    'ip':        numbers in ip format (0.0.0.0 - 255.255.255.255)
                    'password':  any character with visible/hidden icon
            width: int
                Text field width
            length: int
                Number of characters allowed
            labels: tuple
                Text field labels
                (label_spanish, label_english)
            enabled: bool
                Text field enabled / disabled
            theme_color: str
                App theme color name
            language: int
                App language
                0: Spanish, 1: English
            return_pressed: def
                Text field 'return pressed' method name
            text_edited: def
                Text field 'text edited' method name
            text_changed: def
                Text field 'text changed' method name
        
        Returns
        -------
        None
        """
        super(MD3TextField, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        w = attributes['width'] if 'width' in attributes else 96
        self.setGeometry(x, y, w, 52)

        self.text_field = QLineEdit(self)
        self.text_field.setGeometry(0, 8, w, 44)
        self.text_field.setClearButtonEnabled(True)

        if 'input' in attributes:
            patterns_dict = {
                'text': r"[\p{L}\s]+",
                'integer': r'[+-]?\d+',
                'double': r'[+-]?\d+\.\d+',
                'weight': r'([0-9]\d{0,2})\.(\d{1,2})',
                'height_si': r'[0-3]\.(\d{1,2})',
                'height_us': r'[0-9]\'([0-9]|10|11|12)\"',
                'email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
                'ip': r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
            }
            if attributes['input'] in patterns_dict:
                pattern = patterns_dict[attributes['input']]
                reg_exp = QRegularExpressionValidator(QRegularExpression(f'{pattern}'))
                self.text_field.setValidator(reg_exp)

            if attributes['input'] == 'password':
                self.visible_icon = icon_color(attributes['theme_color'], 'eye')
                self.hidden_icon = icon_color(attributes['theme_color'], 'eye_off')
                                
                self.text_field.setEchoMode(QLineEdit.EchoMode.Password)
                self.toggle_password = self.text_field.addAction(self.visible_icon, QLineEdit.ActionPosition.TrailingPosition)
                self.toggle_password.triggered.connect(self.password_action)
                self.toggle_password_state = False

        if 'length' in attributes:
            self.text_field.setMaxLength(attributes['length'])

        self.label_field = QLabel(self)
        self.label_field.move(8, 0)
        self.label_field.setMargin(4)
        self.label_field.setFont(QFont('Segoe UI', 9))
        self.label_field.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.setEnabled(attributes['enabled']) if 'enabled' in attributes else True

        self.setProperty(attributes['type'], True)
        self.set_language(attributes['language'])

        if 'return_pressed' in attributes:
            self.text_field.returnPressed.connect(attributes['return_pressed'])
        if 'text_edited' in attributes:
            self.text_field.textEdited.connect(attributes['text_edited'])
        if 'text_changed' in attributes:
            self.text_field.textChanged.connect(attributes['text_changed'])
          

    def password_action(self) -> None:
        if not self.toggle_password_state:
            self.text_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_state = True
            self.toggle_password.setIcon(self.hidden_icon)
        else:
            self.text_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_state = False
            self.toggle_password.setIcon(self.visible_icon)


    def set_language(self, language: int) -> None:
        """ Change language of label text """
        if language == 0:   self.label_field.setText(self.attributes['labels'][0])
        elif language == 1: self.label_field.setText(self.attributes['labels'][1])
        self.label_field.adjustSize()
        self.label_field.resize(self.label_field.width(), 20)