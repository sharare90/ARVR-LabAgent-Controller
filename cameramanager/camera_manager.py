import os,sys
sys.path.append(os.path.abspath(__file__))

from datetime import datetime, timedelta

import cv2
import face_recognition


class CameraManager(object):
    def __init__(self, controller):
        self.controller = controller
        self.cap = cv2.VideoCapture(0)
        self.num_frame_to_process = 4
        if not self.cap.isOpened():
            print('Could not find the camera {}'.format(0))
            exit()

        self.unknown_id = 1
        self.names, self.face_encodings = self.load_face_encodings()
        self.confidence_threshold_frames = 5  # The number of frames in which the same vector for face is seen.
        self.confidence_threshold_faces = 0.01  # The distance between faces recognized by system.
        self.last_notification_time = {}

    def load_face_encodings(self):
        return [], []

    def process_face_encoding(self, face_encoding, frame, face_location):
        matches = face_recognition.compare_faces(self.face_encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            name = self.names[first_match_index]
            if name.startswith('unknown'):
                confidence = float(name[name.index('_') + 1:])
                confidence += 0.2
                if confidence > 0.9:
                    current_time = datetime.now()
                    # if first_match_index in self.last_notification_time:
                    #     last_notification_time = self.last_notification_time[first_match_index]
                    #     if current_time - last_notification_time < timedelta(minutes=1):
                    #         self.last_notification_time[first_match_index] = current_time
                    #         return

                    # self.last_notification_time[first_match_index] = current_time
                    top, right, bottom, left = face_location
                    face_image = frame[top:bottom, left:right, :]

                    self.controller.push(
                        {
                            'type': 'camera',
                            'event': 'face_seen',
                            'face_image': face_image,
                            'face_location': face_location,
                            'face_encoding': face_encoding,
                            'time': current_time
                        }
                    )
                else:
                    self.names[first_match_index] = f'unknown_{confidence}'
            # else:
            #     print(f'Greetings {name}!! How is it going')
        else:
            self.names.append('unknown_0.0')
            self.face_encodings.append(face_encoding)

    def run(self):
        counter = 0

        while True:
            counter += 1
            ret, frame = self.cap.read()
            if counter == self.num_frame_to_process:
                counter = 0
                # Capture frame-by-frame
                # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                small_frame = frame
                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                # print(face_locations)
                frame_face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                for i, face_encoding in enumerate(frame_face_encodings):
                    self.process_face_encoding(face_encoding, frame, face_locations[i])

                # Display the results
                for top, right, bottom, left in face_locations:
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    # top *= 2
                    # right *= 2
                    # bottom *= 2
                    # left *= 2
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()
