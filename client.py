from pythontuio import TuioClient
from threading import Thread
from drawer import Drawer
from listener import Listener


client = TuioClient(("localhost", 3333))
listener = Listener()
drawer = Drawer(listener)
tuio_thread = Thread(target=client.start)
draw_thread = Thread(target=drawer.draw)
client.add_listener(listener)

tuio_thread.start()
draw_thread.start()
