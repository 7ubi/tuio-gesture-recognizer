import cv2
import numpy as np
from dollar import Dollar
from rectangle import Rectangle
from circle import Circle


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return str(self.x) + " " + str(self.y) 


class Blob:
    def __init__(self, x, y, width, height, id):
        self.id = id
        self.positions = []
        self.width = width
        self.height = height
        self.current_position = Point(int(x * self.width), int(y * self.height))
        self.last_position = self.current_position
        self.dollar = Dollar()
        self.MIN_N_POINTS = 9
        self.is_move_blob = None

    def update_position(self, x, y):
        new_pos = Point(int(x * self.width), int(y * self.height))

        self.positions.append(self.current_position)
        self.last_position = self.current_position
        self.current_position = new_pos

    def draw_info(self, img, color):
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(len(self.positions)):
            try:
                cv2.line(img, (self.positions[i].x, self.positions[i].y),
                         (self.positions[i + 1].x, self.positions[i + 1].y), color=(0, 255, 0), thickness=1)
            except:
                cv2.line(img, (self.positions[i].x, self.positions[i].y),
                         (self.current_position.x, self.current_position.y), color=(0, 255, 0), thickness=1)
            cv2.circle(img, (self.positions[i].x, self.positions[i].y), radius=1, color=(0, 0, 255), thickness=1)

        gesture = ''
        if len(self.positions) > self.MIN_N_POINTS:
            points = []
            for pos in self.positions:
                points.append((pos.x, pos.y))
            points.append((self.current_position.x, self.current_position.y))
            gesture = self.dollar.get_gesture(points)

        cv2.putText(img, "{}: {}".format(str(self.id), gesture),
                    (self.current_position.x, self.current_position.y), font, 0.5, color, 1, cv2.LINE_AA)

    def move_object(self):
        if len(self.positions) == 0:
            return []
        delta_x = self.current_position.x - self.last_position.x
        delta_y = self.current_position.y - self.last_position.y
        self.last_position = self.current_position

        return [delta_x, delta_y]

    def get_dollar_object(self):
        gesture = ''
        if len(self.positions) > self.MIN_N_POINTS:
            points = []
            for pos in self.positions:
                points.append((pos.x, pos.y))
            points.append((self.current_position.x, self.current_position.y))
            gesture = self.dollar.get_gesture(points)

        if gesture == 'rectangle':
            return Rectangle(self)
        elif gesture == 'circle':
            return Circle(self)
        else:
            return None
