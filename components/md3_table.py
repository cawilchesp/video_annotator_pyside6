"""
PySide6 Table component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QTableWidget
from PySide6.QtCore import Qt

# -----
# Table
# -----
class MD3Table(QTableWidget):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Table

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
        super(MD3Table, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        w = attributes['width'] if 'width' in attributes else 32
        self.setGeometry(x, y, w, 32)

        self.setColumnCount(attributes['columns'])
        self.setRowCount(attributes['rows'])
        if not attributes['header']:
            self.horizontalHeader().hide()
            self.verticalHeader().hide()
        self.setRowHeight(0, 40)
        if not attributes['scrollbar']:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        