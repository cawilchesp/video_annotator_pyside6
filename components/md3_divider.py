"""
PySide6 Divider component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QFrame

# -------
# Divider
# -------
class MD3Divider(QFrame):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Divider

        Parameters
        ----------
        attributes: dict
            position: tuple
                Divider top left corner position
                (x, y)
            length: int
                Divider length
            shape: str
                Divider shape
                'horizontal', 'vertical'
        
        Returns
        -------
        None
        """
        super(MD3Divider, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        if attributes['shape'] == 'horizontal':
            w = attributes['length'] if 'length' in attributes else 32
            h = 1
            self.setFrameShape(QFrame.Shape.HLine)
        elif attributes['shape'] == 'vertical':
            w = 1
            h = attributes['length'] if 'length' in attributes else 32
            self.setFrameShape(QFrame.Shape.VLine)
        self.setGeometry(x, y, w, h)

        self.setFrameShadow(QFrame.Shadow.Sunken)
