import os
import cv2

UNITY_PROJECT_ROOT = 'C:\\Users\\sh479140\\LabAgent_Mixamo'
path = os.path.join(UNITY_PROJECT_ROOT, 'Assets\\Resources\\test.txt')

def try_function(g):
    def f(*args, **kwargs):
        try:
            g(*args, **kwargs)
        except:
            pass
    return f

@try_function
def wait_until_file_is_free():
    while True:
        with open(path) as f:
            if f.readline() == 'Done\n':
                break

@try_function
def wave():
    wait_until_file_is_free()
    print('wave')

    with open(path, 'w') as unity_file:
        unity_file.write('Wave')

@try_function
def show_image(image):
    wait_until_file_is_free()
    print('show image')
    image_address = os.path.join(UNITY_PROJECT_ROOT, 'Assets\\Resources\\Images\\image.jpg')
    cv2.imwrite(image_address, image)
    with open(path, 'w') as unity_file:
        unity_file.write('Show Image')

@try_function
def look_toward(location):
    wait_until_file_is_free()
    print('look toward')
    # top, right, bottom, left
    with open(path, 'w') as unity_file:
        center_x = (location[1] + location[3]) // 2
        center_y = (location[0] + location[2]) // 2
        unity_file.write(f'Look Toward: {center_x}, {center_y}')
    print(location)


