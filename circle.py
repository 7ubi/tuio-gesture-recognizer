import cv2
import math
from draw_object import DrawObject


class Circle(DrawObject):
    def __init__(self, blob):
        DrawObject.__init__(self, blob)
        self.radius = int((self.width + self.height) / 4)

    def draw(self, img):
        self.radius = int((self.width + self.height) / 4)
        cv2.circle(img, (int(self.x + self.width / 2), int(self.y + self.height / 2)),
                   self.radius, (255, 0, 0), -1)

    def collide(self, blob):
        return math.dist((self.x + self.width / 2, self.y + self.height / 2),
                         (blob.current_position.x, blob.current_position.y)) < self.radius
