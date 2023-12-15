# video que me ajudou a desenvolver https://www.youtube.com/watch?v=nPzde1YG4ko
# nao consegui fazer pelo que foi passado no moodle

import cv2
import mediapipe as mp
import pyautogui 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

x1 = x2 = y1 = y2 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
font = cv2.FONT_HERSHEY_COMPLEX


def set_system_volume(volume_percentage):

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_percentage / 100, None)


while True:
    ret, frame = webcam.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=6, color=(255,255,255), thickness=4)
                    x1, y1 = x, y

                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=6, color=(255,255,255), thickness=4)
                    x2, y2 = x, y

        cv2.line(frame, (x1,y1), (x2,y2), (0,255,0), 2) 
        dist = ((x2-x1)**2+(y2-y1)**2)**(0.5) // 4 


        # ===================================== #

        # ESCOLHA SO UMA, A OUTRA DEIXE dESCOMENTADA!! #

        # ===================================== #

        # ======= TIPO DE CONTROLADOR 1 ======= #

        # cv2.putText(frame, 'Controle de volume', (20, 40), font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        # cv2.putText(frame, 'Aumentar: Valor > 30', (20, 80), font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        # cv2.putText(frame, 'Diminuir: Valor < 10', (20, 120), font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        # cv2.putText(frame, f'Valor: {dist}', (20, 160), font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        # if dist > 30:
        #     pyautogui.press("volumeup")
        # elif dist < 10:
        #     pyautogui.press("volumedown")

        # ===================================== #

        # ======= TIPO DE CONTROLADOR 2 ======= #

        max_dist = 30  
        min_dist = 10  
        volume_percentage = ((dist - min_dist) / (max_dist - min_dist)) * 100
        volume_percentage = max(0, min(volume_percentage, 100))
        set_system_volume(volume_percentage)
        cv2.putText(frame, f'Volume: {int(volume_percentage)}%', (15, 40), font, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        # ===================================== #

    cv2.imshow("webcam", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()
