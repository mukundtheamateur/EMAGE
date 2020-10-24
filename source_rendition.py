from statistics import mode
import matplotlib.pyplot as plt

import cv2
from keras.models import load_model
import numpy as np

import os


from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input


# parameters for loading data and images
def emotionrec():
    detection_model_path = 'haarcascade_frontalface_alt2.xml'
    emotion_model_path = 'fer2013_mini_XCEPTION.102-0.66.hdf5'
    emotion_labels = get_labels('fer2013')

    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)

    # loading models
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)

    # getting input model shapes for inference
    emotion_target_size = emotion_classifier.input_shape[1:3]

    # starting lists for calculating modes
    emotion_window = []

    # starting video streaming
    cv2.namedWindow('Emotion Detection by EmoGing')
    video_capture = cv2.VideoCapture(0)

    slices = [0, 0, 0, 0, 0]
    file = open('emotion.txt','a') 
    file. truncate(0)
    for x in range(0, 20):
        
        bgr_image = video_capture.read()[1]
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = detect_faces(face_detection, gray_image)

        for face_coordinates in faces:

            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_window.append(emotion_text)

            if len(emotion_window) > frame_window:
                emotion_window.pop(0)
            try:
                emotion_mode = mode(emotion_window)
            except:
                continue

            colors = ['red', 'blue', 'yellow', 'cyan', 'green']
            emotions = ['angry', 'sad', 'happy', 'surprise', 'neutral']
            if emotion_text == 'angry':
                color = emotion_probability * np.asarray((255, 0, 0))
                slices[0]+=1
                #print("angry")
                file.write("angry\n")
            elif emotion_text == 'sad':
                color = emotion_probability * np.asarray((0, 0, 255))
                slices[1]+=1
                #print("sad")
                file.write("sad\n")
            elif emotion_text == 'happy':
                color = emotion_probability * np.asarray((255, 255, 0))
                slices[2]+=1
                #print("happy")
                file.write("happy\n")
            elif emotion_text == 'surprise':
                color = emotion_probability * np.asarray((0, 255, 255))
                slices[3]+=1
                #print("surprise")
                file.write("surprise\n")
            else:
                color = emotion_probability * np.asarray((0, 255, 0))
                slices[4]+=1
                file.write("sad\n")

            color = color.astype(int)
            color = color.tolist()
            

            draw_bounding_box(face_coordinates, rgb_image, color)
            draw_text(face_coordinates, rgb_image, emotion_mode,
                      color, 0, -45, 1, 1)

        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('(Press Q to quit)', bgr_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            maxx = slices.index(max(slices))
            exploded=[0,0,0,0,0]
            exploded[maxx] = 0.06
            plt.pie(slices, labels=emotions, colors=colors, startangle=90, shadow=True, explode=exploded, autopct='%1.2f%%')
            plt.legend(loc="upper right")
            plt.legend()
            lines = [line.rstrip('\n') for line in open('log.txt')]
            plt.title(lines[0] + " - " + lines[1])
            cv2.destroyAllWindows()
            #plt.show()
            plt.savefig("result.png")
            strname = lines[0] +"_"+ lines[1] + ".png"
            plt.savefig(strname)
            video_capture.release() 
            im = cv2.imread('result.png')
            cv2.imshow('Result',im)
            cv2.waitKey(0)        
            # plt.savefig(strname)
            break

    file.close()
    print("----------------------------------------")

    emotion = open("emotion.txt",'r')

    d = dict()

    for line in emotion:
        line = line.strip()
        # print(line)

        line = line.lower()

        words = line.split(" ")
        #print(words)

        for word in words:
            if word in d:
                d[word] = d[word]+1
            else:
                d[word] = 1
    for key in list(d.keys()):
        keymax = max(d, key=d.get)
    print(keymax)

    emotions = keymax
    filey = open('emotions.txt','a') 
    filey. truncate(0)

    filey.write(emotions)
    filey.close()

    filey = open('emotions.txt','r')

    return filey.read()