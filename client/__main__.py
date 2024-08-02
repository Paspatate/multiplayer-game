from .the_client import Client

print("start client")
c = Client()
c.init()

try:
    c.run()
except KeyboardInterrupt:
    c.clean()

# SIMPLE CLIENT TO TEST CONNECTION
