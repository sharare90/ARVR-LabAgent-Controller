import os, sys
sys.path.append(os.path.abspath(__file__))
from multiprocessing import Queue

import face_recognition
import speech_recognition as sr
from voice.functions import say_text_by_id, say_text
from unity_controller import functions as unity_controller


class Controller(object):
    def __init__(self):
        self.queue = Queue()
        self.known_faces, self.ids = self.load_known_faces()

        # say_text_by_id(0)

    def load_known_faces(self):
        return [], []

    def get_notification(self):
        return self.queue.get()

    def push(self, data):
        self.queue.put(data)

    def process_camera_notification(self, notification):
        print(notification)
        unity_controller.look_toward(notification['face_location'])
        matches = face_recognition.compare_faces(self.known_faces, notification['face_encoding'])
        if True in matches:
            first_match_index = matches.index(True)
            person_id = self.ids[first_match_index]

            # try:
            #     say_text(f'Hello {person_id}. How are you?')
            #     unity_controller.wave()
            # except:
            #     pass
        else:
            # we have seen a new face. Store it!
            unity_controller.show_image(notification['face_image'])
            say_text_by_id(1)

            with self.microphone as source:
                audio = self.recognizer.listen(source, phrase_time_limit=5)
            try:
                # recognize speech using Google Speech Recognition
                value = self.recognizer.recognize_google(audio)
                values = value.split()
                name = values[-1]

                # just pick a name
                # name = ''

                unity_controller.wave()
                say_text(f'Nice to meet you {name}')
                self.known_faces.append(notification['face_encoding'])
                self.ids.append(name)

            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))



        # import matplotlib.pyplot as plt
        # plt.imshow(notification['face_image'])
        # plt.show()

    def run(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        print("A moment of silence, please...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(self.recognizer.energy_threshold))
        while True:
            notification = self.get_notification()
            if notification:
                if notification['type'] == 'camera':
                    self.process_camera_notification(notification)
