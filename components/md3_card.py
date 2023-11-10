"""
PySide6 Card component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QLabel

# ----
# Card
# ----
class MD3Card(QFrame):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Card

        Parameters
        ----------
        attributes: dict
            position: tuple
                Card top left corner position
                (x, y)
            size: tuple
                Card size
                (width, height)
            titles: tuple
                Card titles (Optional)
                (label_spanish, label_english)
            type: str
                Card type
                'filled', 'outlined'
            language: int
                App language
                0: Spanish, 1: English
        
        Returns
        -------
        None
        """
        super(MD3Card, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        w, h = attributes['size'] if 'size' in attributes else (96, 96)
        self.setGeometry(x, y, w, h)

        self.title = QLabel(self)
        self.title.setGeometry(8, 8, 32, 32)
        self.title.setFont(QFont('Segoe UI', 14))

        self.setProperty(self.attributes['type'], True)
        self.set_language(attributes['language'])


    def set_language(self, language: int) -> None:
        """ Change language of title text """
        if 'titles' in self.attributes:
            if language == 0:   self.title.setText(self.attributes['titles'][0])
            elif language == 1: self.title.setText(self.attributes['titles'][1])
            self.title.adjustSize()