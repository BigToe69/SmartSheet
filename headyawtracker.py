import cv2
import numpy as np
import mediapipe as mp
import time
import pyautogui
import math

screen_width, screen_height = pyautogui.size()

settings = {"turn_time": 1.0, "turn_begin_threshold_degrees": 10.0}

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/face_landmarker.task"
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=1,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True
)

landmarker = FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

def GetFaceData():
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )
    result = landmarker.detect(mp_image)
    if not result.face_blendshapes:
        return None
    matrix = np.array(
        result.facial_transformation_matrixes[0]
    )
    blendshapes = result.face_blendshapes
    blend = {i.category_name : i.score for i in range(blendshapes)} 

    return matrix, blend

turning = False
turning_start_time = 0
turn = False
turning_progress = 0
def Track():
    global turning_start_time
    global turning
    global turn
    global turning_progress
    turn = False
    data = GetFaceData()
    if data is None:
        return
    matrix = data[0]
    blend = data[1]
    print(blend['mouthLeft'])

    R = matrix[:3, :3]

    yaw = -math.degrees(math.atan2(R[0,2], R[2,2]))

    if yaw > settings["turn_begin_threshold_degrees"]:
        if not turning: turning_start_time = time.time()
        turning = True
        turning_progress = (time.time() - turning_start_time) / settings["turn_time"]
        if time.time() > turning_start_time + settings["turn_time"]:
            turn = "right"
            turning_start_time = time.time() + 100
    elif yaw < -settings["turn_begin_threshold_degrees"]:
        if not turning: turning_start_time = time.time()
        turning = True
        turning_progress = (time.time() - turning_start_time) / settings["turn_time"]
        if time.time() > turning_start_time + settings["turn_time"]:
            turn = "left"
            turning_start_time = time.time() + 100
    else:
        turning = False
        turning_progress = turning_progress + (0-turning_progress)*0.5
    
        
