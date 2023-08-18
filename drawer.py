import cv2
import numpy as np
import math
from draw_object import DrawObject

class Drawer:
    def __init__(self, listener):
        self.delay = 5
        self.listener = listener
        self.objects = []

    def get_move_blob(self, blob):
        blob.is_move_blob = False
        closest_dist = 3000
        closest_obj = None

        for obj in self.objects:
            if obj.collide(blob):
                dist = math.dist((obj.x, obj.y), (blob.current_position.x, blob.current_position.y))
                if dist < closest_dist:
                    blob.is_move_blob = True
                    closest_dist = dist
                    closest_obj = obj

        if closest_obj is not None:
            closest_obj.collided_blobs.append(blob)

    def draw(self):
        while True:
            img = np.zeros((600, 600, 3), dtype="uint8")
            img[:] = (255, 255, 255)

            for blob in self.listener.blobs:
                if blob.is_move_blob is None:
                    self.get_move_blob(blob)

                blob.draw_info(img, (255, 0, 0))

            for blob in self.listener.deleted_blobs:
                obj = blob.get_dollar_object()
                self.listener.deleted_blobs.pop(0)

                if blob.is_move_blob:
                    for obj in self.objects:
                        for collided_blob in obj.collided_blobs:
                            if collided_blob is blob:
                                obj.collided_blobs.remove(blob)
                                len(obj.collided_blobs)
                else:
                    if obj is not None:
                        self.objects.append(obj)

            for obj in self.objects:
                obj.draw(img)
                obj.transform_object()

            cv2.imshow('Frame', img)
            if cv2.waitKey(self.delay) & 0xFF == ord('q'):
                break
