"""
PySide6 Video label component adapted to follow Material Design 3 guidelines

"""
from PySide6.QtWidgets import QLabel, QFrame

# -----------
# Image Label
# -----------
class MD3ImageLabel(QLabel):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Image Label

        Parameters
        ----------
        attributes: dict
            position: tuple
                Label position
                (x, y) -> x, y: upper left corner
            size: tuple
                Label size
                (w, h) -> w: width, h: height
            scaled_image: bool
                Fit image to label size
        
        Returns
        -------
        None
        """
        super(MD3ImageLabel, self).__init__(parent)

        self.attributes = attributes
        self.parent = parent

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        w, h = attributes['size'] if 'size' in attributes else (96, 96)
        self.setGeometry(x, y, w, h)

        self.setScaledContents(attributes['scaled_image'])
        
        self.setFrameStyle(QFrame.Shape.Box)
