from .the_server import Server

s = Server()
s.init()

try:
    s.run()
except KeyboardInterrupt:
    s.clean()
