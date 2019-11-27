import os
from multiprocessing import Process

from controller.controller import Controller
from cameramanager.camera_manager import CameraManager


def start_controller(controller):
    print('controller')
    controller.run()


def start_camera_manager(controller):
    print('camera_manager')
    CameraManager(controller).run()


if __name__ == '__main__':
    # set GOOGLE_APPLICATION_CREDENTIALS=C:\\gcloud_credentials\\UCF Parking-20b5aeed5fdd.json

    controller = Controller()
    p1 = Process(target=start_controller, args=(controller, ))
    p2 = Process(target=start_camera_manager, args=(controller, ))

    p1.start()
    p2.start()
