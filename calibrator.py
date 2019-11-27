import cv2


class Calibrator(object):
    def __init__(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        def handle_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.left = x - self.square_side_length // 2
                self.top = y - self.square_side_length // 2
                self.right = self.left + self.square_side_length
                self.bottom = self.top + self.square_side_length

        cv2.namedWindow("frame")
        cv2.setMouseCallback("frame", handle_click)

        self.square_side_length = 80
        self.height = len(frame)
        self.width = len(frame[0])

        self.top = (self.height - self.square_side_length) // 2
        self.left = (self.width - self.square_side_length) // 2
        self.right = self.left + self.square_side_length
        self.bottom = self.top + self.square_side_length

        self.color = (0, 0, 255)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()

            cv2.rectangle(frame, (self.left, self.top), (self.right, self.bottom), self.color, 2)

            top = (self.height - self.square_side_length) // 2
            bottom = top + self.square_side_length
            cv2.rectangle(
                frame,
                (self.square_side_length, top),
                (2 * self.square_side_length, bottom),
                (0, 255, 0),
                2
            )
            cv2.rectangle(
                frame,
                (self.width - 2 * self.square_side_length, top),
                (self.width - self.square_side_length, bottom),
                (0, 255, 0),
                2
            )
            # Display the resulting frame
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    Calibrator().run()
