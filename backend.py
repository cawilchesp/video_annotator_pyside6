from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSettings

import sys
import cv2


style_colors = {
    'azul_gris': '59,66,83',
    'azul_negro': '46,52,65',
    'azul': '128,160,194',
    'amarillo': '237,204,135',
    'rojo': '193,96,105',
    'verde': '162,191,138',
    'blanco': '229,233,240',
    'gris': '178,178,178',
    'negro': '0,0,0'
}


def open_video(source_file: str):
    cap = cv2.VideoCapture(source_file)
    if not cap.isOpened():
        print('Error opening video stream or file')
        return 0

    video_properties = {
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': float(cap.get(cv2.CAP_PROP_FPS))
    }

    return video_properties


def frame_extraction(source_file: str, frames_folder: str, labeled_folder: str, resized_folder: str):
    cap = cv2.VideoCapture(source_file)
    if not cap.isOpened():
        print('Error opening video stream or file')
        return 0

    frame_progressBar = QtWidgets.QProgressDialog('Extrayendo frames...',
                            'Cancelar', 0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    frame_progressBar.setWindowModality(Qt.WindowModality.WindowModal)
    
    frame_number = 0
    while(cap.isOpened()):
        frame_progressBar.setValue(frame_number)
        ret, frame = cap.read()
        if not ret or frame_progressBar.wasCanceled():
            break
        
        frame_text = f'{frame_number}'.zfill(6)
        frame_image = f'{frames_folder}/image_{frame_text}.png'
        cv2.imwrite(frame_image, frame)

        label_file = open(f'{labeled_folder}/image_{frame_text}.txt', 'x')
        label_file.close()
        
        resized_image = f'{resized_folder}/image_{frame_text}.png'
        resized_frame = cv2.resize(frame, [416, 416], interpolation= cv2.INTER_LINEAR)
        cv2.imwrite(resized_image, resized_frame)
        
        frame_number += 1

