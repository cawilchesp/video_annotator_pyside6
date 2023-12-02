import supervision as sv
from supervision.detection.core import Detections

import cv2
import numpy as np
from collections import deque

from icecream import ic

COLOR_LIST = sv.ColorPalette.from_hex([
    '#ff2d55',
    '#0f7f07',
    '#0095ff',
    '#ffcc00',
    '#46f0f0',
    '#ff9500',
    '#d2f53c',
    '#cf52de',
])


def box_annotations(scene: np.ndarray, detections: Detections, labels: list = None) -> np.ndarray:
    for index, detection in enumerate(detections):
        x1, y1, x2, y2 = detection[0].astype(int)
        
        color = COLOR_LIST.by_idx(detection[3]).as_bgr()
        
        cv2.rectangle(img=scene,pt1=(x1, y1),pt2=(x2, y2),color=color,thickness=1)
        
        # Label
        if labels is not None: 
            text = labels[index]

            (text_width, text_height), _ = cv2.getTextSize(
                text=text,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.3,
                thickness=1,
            )

            text_background_x1 = x1 if x1 > 0 else x2 - 6 - text_width
            text_background_y1 = y1 - 6 - text_height if y1 - 6 - text_height > 0 else y2

            text_background_x2 = text_background_x1 + 6 + text_width
            text_background_y2 = text_background_y1 + 6 + text_height
            
            text_x = text_background_x1 + 3
            text_y = text_background_y2 - 3

            cv2.rectangle(
                img=scene,
                pt1=(text_background_x1, text_background_y1),
                pt2=(text_background_x2, text_background_y2),
                color=color,
                thickness=cv2.FILLED,
            )

            cv2.putText(
                img=scene,
                text=text,
                org=(text_x, text_y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.3,
                color=(0,0,0),
                thickness=1,
                lineType=cv2.LINE_AA,
            )

    return scene


def track_annotations(scene: np.ndarray, tracks: Detections, track_deque: deque, position: str = 'centroid') -> np.ndarray:
    track_positions = {
        'top_left': lambda x1, y1, x2, y2 : tuple(map(int, (x1, y1))),
        'top_center': lambda x1, y1, x2, y2 : tuple(map(int, ((x2+x1)/2, y1))),
        'top_right': lambda x1, y1, x2, y2 : tuple(map(int, (x2, y1))),
        'center_left': lambda x1, y1, x2, y2 : tuple(map(int, (x1, (y2+y1)/2))),
        'centroid': lambda x1, y1, x2, y2 : tuple(map(int, ((x2+x1)/2, (y2+y1)/2))),
        'center_right': lambda x1, y1, x2, y2 : tuple(map(int, (x2, (y2+y1)/2))),
        'bottom_left': lambda x1, y1, x2, y2 : tuple(map(int, (x1, y2))),
        'bottom_center': lambda x1, y1, x2, y2 : tuple(map(int, ((x2+x1)/2, y2))),
        'bottom_right': lambda x1, y1, x2, y2 : tuple(map(int, (x2, y2)))
    }

    for track in tracks:
        xyxy, _, _, class_id, tracker_id = track
        x1, y1, x2, y2 = xyxy.astype(int)
        color = COLOR_LIST.by_idx(class_id).as_bgr()
        
        # Draw track line
        track_deque[tracker_id].appendleft(track_positions[position](x1, y1, x2, y2))

        for point1, point2 in zip(list(track_deque[tracker_id]), list(track_deque[tracker_id])[1:]):
            cv2.line(scene, point1, point2, color, 1, cv2.LINE_AA)
    
    return scene


def mask_annotations(scene: np.ndarray, detections: Detections) -> np.ndarray:
    for detection in detections:
        mask = detection[1]

        color = COLOR_LIST.by_idx(detection[3]).as_bgr()
        
        colored_mask = np.zeros_like(scene, dtype=np.uint8)
        colored_mask[:] = color

        scene = np.where(
            np.expand_dims(mask, axis=-1),
            np.uint8(0.5 * colored_mask + (1 - 0.5) * scene),
            scene,
        )

    return scene


def pose_annotations(scene: np.array, poses: np.array, pose_config: dict) -> None:
    """
    Draw object pose on frame
    """





    
    for keypoints in poses:
        if pose_config['HEAD']:
            color = (0, 255, 0)
            nose = (keypoints[0][0], keypoints[0][1])
            left_eye = (keypoints[1][0], keypoints[1][1])
            right_eye = (keypoints[2][0], keypoints[2][1])
            left_ear = (keypoints[3][0], keypoints[3][1])
            right_ear = (keypoints[4][0], keypoints[4][1])
            # Draw points
            cv2.circle(scene, nose, 4, color, -1)
            cv2.circle(scene, left_eye, 4, color, -1)
            cv2.circle(scene, right_eye, 4, color, -1)
            cv2.circle(scene, left_ear, 4, color, -1)
            cv2.circle(scene, right_ear, 4, color, -1)
            # Draw lines
            cv2.line(scene, nose, left_eye, color, 2, cv2.LINE_AA)
            cv2.line(scene, nose, right_eye, color, 2, cv2.LINE_AA)
            cv2.line(scene, right_eye, left_eye, color, 2, cv2.LINE_AA)
            cv2.line(scene, left_ear, left_eye, color, 2, cv2.LINE_AA)
            cv2.line(scene, right_ear, right_eye, color, 2, cv2.LINE_AA)

        if pose_config['ARMS']:
            color = (255, 0, 0)
            left_shoulder =     (keypoints[5][0], keypoints[5][1])
            right_shoulder =    (keypoints[6][0], keypoints[6][1])
            left_elbow =        (keypoints[7][0], keypoints[7][1])
            right_elbow =       (keypoints[8][0], keypoints[8][1])
            left_hand =         (keypoints[9][0], keypoints[9][1])
            right_hand =        (keypoints[10][0], keypoints[10][1])
            # Draw points
            cv2.circle(scene, left_shoulder, 4, color, -1)
            cv2.circle(scene, right_shoulder, 4, color, -1)
            cv2.circle(scene, left_elbow, 4, color, -1)
            cv2.circle(scene, right_elbow, 4, color, -1)
            cv2.circle(scene, left_hand, 4, color, -1)
            cv2.circle(scene, right_hand, 4, color, -1)
            # Draw lines
            cv2.line(scene, left_hand, left_elbow, color, 2, cv2.LINE_AA)
            cv2.line(scene, left_elbow, left_shoulder, color, 2, cv2.LINE_AA)
            cv2.line(scene, left_shoulder, right_shoulder, color, 2, cv2.LINE_AA)
            cv2.line(scene, right_shoulder, right_elbow, color, 2, cv2.LINE_AA)
            cv2.line(scene, right_elbow, right_hand, color, 2, cv2.LINE_AA)

        if pose_config['TRUNK']:
            color = (0, 0, 255)
            left_hip = (keypoints[11][0], keypoints[11][1])
            right_hip = (keypoints[12][0], keypoints[12][1])
            # Draw points
            cv2.circle(scene, left_hip, 4, color, -1)
            cv2.circle(scene, right_hip, 4, color, -1)
            # Draw lines
            cv2.line(scene, left_shoulder, left_hip, color, 2, cv2.LINE_AA)
            cv2.line(scene, left_hip, right_hip, color, 2, cv2.LINE_AA)
            cv2.line(scene, right_hip, right_shoulder, color, 2, cv2.LINE_AA)

        if pose_config['LEGS']:
            color = (0, 255, 255)
            left_knee = (keypoints[13][0], keypoints[13][1])
            right_knee = (keypoints[14][0], keypoints[14][1])
            left_foot = (keypoints[15][0], keypoints[15][1])
            right_foot = (keypoints[16][0], keypoints[16][1])
            # Draw points
            cv2.circle(scene, left_knee, 4, color, -1)
            cv2.circle(scene, right_knee, 4, color, -1)
            cv2.circle(scene, left_foot, 4, color, -1)
            cv2.circle(scene, right_foot, 4, color, -1)
            # Draw lines
            cv2.line(scene, left_hip, left_knee, color, 2, cv2.LINE_AA)
            cv2.line(scene, left_knee, left_foot, color, 2, cv2.LINE_AA)
            cv2.line(scene, right_hip, right_knee, color, 2, cv2.LINE_AA)
            cv2.line(scene, right_knee, right_foot, color, 2, cv2.LINE_AA)

    return scene