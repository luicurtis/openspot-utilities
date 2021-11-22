import cv2 as open_cv
import numpy as np

from colors import COLOR_WHITE
from drawing_utils import draw_contours


class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = open_cv.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []

        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)
        open_cv.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
        while True:
            font                   = open_cv.FONT_HERSHEY_SIMPLEX
            topLeftCornerOfText    = (10,125)
            fontScale              = 2
            fontColor              = (0,0,255)
            lineType               = 5

            open_cv.putText(self.image,'Press \'q\' to quit once you\'ve drawn the boxes', 
                topLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            open_cv.imshow(self.caption, self.image)

            key = open_cv.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                # TODO: Make this function work
                self.image = self.image.copy()

            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        open_cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params):

        if event == open_cv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            open_cv.circle(self.image, (x,y), radius=10, color=(0, 0, 255), thickness=-1)
            self.click_count += 1

            if self.click_count >= 4:
                self.__handle_done()

            elif self.click_count > 1:
                self.__handle_click_progress()

        open_cv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        open_cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 10)

    def __handle_done(self):
        open_cv.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color,
                     10)
        open_cv.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color,
                     10)

        self.click_count = 0

        coordinates = np.array(self.coordinates)
        # height, width = self.image.shape[:2]

        # TODO: Add functinality to  determine the bottom left, etc most point
        #       to not require to go in order of clicking (top left, top right, etc...)
        # maybe: https://stackoverflow.com/questions/67822179/find-polygon-top-left-top-right-bottom-right-and-bottom-left-points

        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        draw_contours(self.image, coordinates, str(self.ids), COLOR_WHITE)

        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1
