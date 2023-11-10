from PySide6.QtWidgets import QDialog

from dialogs.about_app_ui import AboutAppUI

import yaml


# ----------------
# About App Dialog
# ----------------
class AboutApp(QDialog):
    def __init__(self):
        """ About Me Dialog """
        super().__init__()

        # --------
        # Settings
        # --------
        with open('settings.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.theme_style = self.config['THEME_STYLE']
        self.theme_color = self.config['THEME_COLOR']

        # ---
        # GUI
        # ---
        self.ui = AboutAppUI(self)
        theme_file = f"themes/{self.theme_color}_light_theme.qss" if self.theme_style else f"themes/{self.theme_color}_dark_theme.qss"
        with open(theme_file, "r") as theme_qss:
            self.setStyleSheet(theme_qss.read())


    def on_ok_button_clicked(self):
        """ Close dialog """
        self.close()