import cv2
from draw_object import DrawObject


class Rectangle(DrawObject):
    def __init__(self, blob):
        DrawObject.__init__(self, blob)

    def draw(self, img):
        points = self.rotate()
        cv2.drawContours(img, [points], 0, (255, 255, 0), -1, cv2.LINE_AA)
        # cv2.rectangle(img, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 255, 0), -1)

    def collide(self, blob):
        return (self.x < blob.current_position.x < self.x + self.width
                and self.y < blob.current_position.y < self.y + self.height)
