"""
PySide6 Main Window

"""

# ------
# Window
# ------
class MD3Window:
    def __init__(self, attributes):
        """ Main Window

        Parameters
        ----------
        attributes: dict
            parent:
                UI Parent object 
            size: tuple
                Window width and height
                (width, height)
            position: tuple (Optional)
                Window position, centered by default
                (x, y) -> x, y: upper left corner
            minimum_size: tuple
                minimum window size when resized
                (minimum_width, minimum_height)
            maximum_size: tuple
                maximum window size when resized
                (maximum_width, maximum_height)
            labels: tuple
                Window title labels
                (label_spanish, label_english)
            language: int
                App language
                0: Spanish, 1: English
        
        Returns
        -------
        None
        """
        self.parent = attributes['parent']
        self.attributes = attributes

        w, h = attributes['size'] if 'size' in attributes else (1300, 700)
        if 'position' in attributes:
            x, y = attributes['position']
        else:
            screen_x = int(self.parent.screen().availableGeometry().width() / 2 - (w / 2))
            screen_y = int(self.parent.screen().availableGeometry().height() / 2 - (h / 2))
            x, y = (screen_x, screen_y) 
        self.parent.setGeometry(x, y, w, h)
        if 'minimum_size' in attributes:
            w_min, h_min = attributes['minimum_size']
            self.parent.setMinimumSize(w_min, h_min)
        if 'maximum_size' in attributes:
            w_max, h_max = attributes['maximum_size']
            self.parent.setMaximumSize(w_max, h_max)
        self.set_language(attributes['language'])


    def set_language(self, language: int) -> None:
        """ Change language of title text """
        if language == 0:   self.parent.setWindowTitle(self.attributes['labels'][0])
        elif language == 1: self.parent.setWindowTitle(self.attributes['labels'][1])