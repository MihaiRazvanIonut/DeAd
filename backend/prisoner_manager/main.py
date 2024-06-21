import constants
import server

if __name__ == "__main__":
    server = server.ServerFacade(constants.HOST, constants.PORT)
    server.run()
