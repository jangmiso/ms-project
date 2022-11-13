#아직 수정중!

import numpy as np
import imutils
import time
import timeit
import dlib
import cv2
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
from threading import Timer
from check_cam_fps import check_fps
import make_train_data as mtd
#import light_remover as lr
#import ringing_alarm as alarm

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A+B) / (2.0*C)
    return ear

def init_open_ear():
    time.sleep(5)
    print("open init time sleep")
    ear_list = []
    th_message1 = Thread(target = init_message)
    th_message1.deamon = True
    th_message1.start()
    for i in range(7):
        ear_list.append(both_ear)
        time.sleep(1)
    global OPEN_EAR
    OPEN_EAR = sum(ear_list)/len(ear_list)
    print("open list =", ear_list, "\nOPEN_EAR =", OPEN_EAR, "\n")
    
def init_close_ear(): 
    time.sleep(2)
    th_open.join()
    time.sleep(5)
    print("close init time sleep")
    ear_list=[]
    th_message2 = Thread(target = init_message)
    th_message2.deamon = True
    th_message2.start()
    time.sleep(1)
    for i in range(7):
        ear_list.append(both_ear)
        time.sleep(1)
    CLOSE_EAR = sum(ear_list)/len(ear_list)
    global EAR_THRESH
    EAR_THRESH = (((OPEN_EAR-CLOSE_EAR)/2)+CLOSE_EAR)
    print("close list =", ear_list, "\nCLOSE_EAR =", CLOSE_EAR, "\n")
    print("The last EAR_THRESH's value :",EAR_THRESH, "\n")

def init_message() :
    print("init_message")
    #alarm.sound_alarm("init_sound.mp3")
    
#1. Variables for checking EAR
OPEN_EAR=0
EAR_THRESH=0

#2. Variables for detecting if user is asleep.
EAR_CONSEC_FRAMES=20 
COUNTER=0

#3. When the alarm rings, measure the time eyes are being closed.
closed_eyes_time=[]
TIMER_FLAG=False
ALARM_FLAG=False

#4. When the alarm is rang, count the number of times it is rang, and prevent the alarm from ringing continuously.
ALARM_COUNT=0
RUNNING_TIME=0

#5. We should count the time eyes are being opened for data labeling.
PREV_TERM=0

#6. Variables for trained data generation and calculation fps.
np.random.seed(9)
power, nomal, short = mtd.start(25)
test_data = []
result_data = []
prev_time = 0

#7. Detect face & eyes.
print("loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#8. Run the cam.
print("starting video stream thread...")
vs = VideoStream(src=0).start()
time.sleep(1.0)

#9. Threads to run the functions in which determine the EAR_THRESH.
th_open = Thread(target=init_open_ear)
th_open.deamon = True
th_open.start()
th_close = Thread(target = init_close_ear)
th_close.deamon = True
th_close.start()


while True:
    frame = vs.read()
    frame = imutils.resize(frame, width = 400)
    
    #L, gray = lr.light_removing(frame)
    
    rects = detector(gray,0)
    
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        both_ear = (leftEAR + rightEAR)*500 

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0,255,0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0,255,0), 1)
        
        if both_ear < EAR_THRESH:
            if not TIMER_FLAG:
                start_closing = timeit.default_timer()
                TIMER_FLAG=True
            COUNTER+=1

            if COUNTER >= EAR_CONSEC_FRAMES:

                mid_closing = timeit.default_timer()
                closing_time = round((mid_closing-start_closing),3)

                if closing_time >= RUNNING_TIME:
                    if RUNNING_TIME == 0:
                        CUR_TERM = timeit.default_timer()
                        OPENED_EYES_TIME = round((CUR_TERM - PREV_TERM),3)
                        PREV_TERM = CUR_TERM
                        RUNNING_TIME = 1.75

                    RUNNING_TIME += 2
                    ALARM_FLAG = True
                    ALARM_COUNT += 1

                    print("{0}st ALARM".format(ALARM_COUNT))
                    print("The time eyes is being opened before the alarm went off :", OPENED_EYES_TIME)
                    print("closing time :", closing_time)
                    test_data.append([OPENED_EYES_TIME, round(closing_time*10,3)])
                    result = mtd.run([OPENED_EYES_TIME, closing_time*10], power, nomal, short)
                    result_data.append(result)
                    t = Thread(target = alarm.select_alarm, args = (result, ))
                    t.deamon = True
                    t.start()

        else :
            COUNTER = 0
            TIMER_FLAG = False
            RUNNING_TIME = 0

            if ALARM_FLAG :
                end_closing = timeit.default_timer()
                closed_eyes_time.append(round((end_closing-start_closing),3))
                print("The time eyes were being offed :", closed_eyes_time)

            ALARM_FLAG = False

        cv2.putText(frame, "EAR : {:.2f}".format(both_ear), (300,130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,30,20), 2)

    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()