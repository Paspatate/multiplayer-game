from server.server import Server

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("stop")