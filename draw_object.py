import math
import numpy as np


class DrawObject:

    def __init__(self, blob):
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.get_bounding_box(blob)
        self.collided_blobs = []
        self.distance = 0
        self.angle = 0
        self.rotation = None

    def get_bounding_box(self, blob):
        self.x = 3000
        self.y = 3000
        maxX = 0
        maxY = 0

        for pos in blob.positions:
            if pos.x < self.x:
                self.x = pos.x

            if pos.y < self.y:
                self.y = pos.y
            if pos.x > maxX:
                maxX = pos.x

            if pos.y > maxY:
                maxY = pos.y

        if blob.current_position.x < self.x:
            self.x = blob.current_position.x

        if blob.current_position.y < self.y:
            self.y = blob.current_position.y
        if blob.current_position.x > maxX:
            maxX = blob.current_position.x

        if blob.current_position.y > maxY:
            maxY = blob.current_position.y

        self.width = maxX - self.x
        self.height = maxY - self.y

    def transform_object(self):
        self.update_pos()
        self.update_scale()
        self.update_rotation()

    def update_pos(self):
        if len(self.collided_blobs) != 1:
            return
        delta = self.collided_blobs[0].move_object()

        if len(delta) == 0:
            return

        self.x += delta[0]
        self.y += delta[1]

    def draw(self, img):
        pass

    def collide(self, blob):
        pass

    def update_scale(self):
        if len(self.collided_blobs) != 2:
            return
        pos1 = self.collided_blobs[0].current_position
        pos2 = self.collided_blobs[1].current_position

        dist = int(math.dist((pos1.x, pos1.y), (pos2.x, pos2.y)) - self.distance)

        self.height += dist
        self.width += dist

        self.distance = int(math.dist((pos1.x, pos1.y), (pos2.x, pos2.y)))

    def update_rotation(self):
        if len(self.collided_blobs) != 2:
            return

        pos1 = self.collided_blobs[0].current_position
        pos2 = self.collided_blobs[1].current_position
        if self.rotation is None:
            self.rotation = math.atan2(pos1.y - pos2.y, pos1.x - pos2.x)

        self.angle += math.atan2(pos1.y - pos2.y, pos1.x - pos2.x) - self.rotation
        self.rotation = math.atan2(pos1.y - pos2.y, pos1.x - pos2.x)

    def rotate(self):
        points = np.array([(self.x, self.y), (self.x, self.y + self.height),
                           (self.x + self.width, self.y + self.height), (self.x + self.width, self.y)])

        c_x, c_y = np.mean(points, axis=0)
        rotation_matrix = np.array(
            [
                [np.cos(self.angle), -np.sin(self.angle)],
                [np.sin(self.angle), np.cos(self.angle)]
            ]
        )
        rotated_points = np.dot(points - np.array([c_x, c_y]),
                                rotation_matrix.T) + np.array([c_x, c_y])
        return rotated_points.astype(int)

