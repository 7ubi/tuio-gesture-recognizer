from pythontuio import Cursor
from pythontuio import TuioListener
from blob import Blob

class Listener(TuioListener):

    def __init__(self):
        self.blobs = []
        self.deleted_blobs = []

    def add_tuio_cursor(self, cursor: Cursor):
        self.blobs.append(Blob(cursor.position[0], cursor.position[1], 600, 600, cursor.session_id))
    
    def update_tuio_cursor(self, cursor: Cursor):
        for i in range(len(self.blobs)):
            if self.blobs[i].id == cursor.session_id:
                self.blobs[i].update_position(cursor.position[0], cursor.position[1])
                break
        return super().update_tuio_cursor(cursor)
    
    def remove_tuio_cursor(self, cursor: Cursor):
        for i in range(len(self.blobs)):
            if self.blobs[i].id == cursor.session_id:
                self.deleted_blobs.append(self.blobs[i])
                self.blobs.pop(i)
                break
        return super().remove_tuio_cursor(cursor)
