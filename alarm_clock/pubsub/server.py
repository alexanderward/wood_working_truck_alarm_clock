import select
import socket
import logging
import signal
from pubsub.networking.communication import send, receive
from pubsub.networking.constants import SERVER_PORT, MAXIMUM_CONNECTIONS


class Server(object):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Server')

    def __init__(self):
        self.clients = 0
        self.client_map = {}  # Client map
        self.outputs = []  # Output socket list
        self.setup_socket()
        signal.signal(signal.SIGINT, self.sighandler)  # Trap keyboard interrupts

    def setup_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', SERVER_PORT))
        self.logger.info('SYSTEM - Listening to port %s' % SERVER_PORT)
        self.server.listen(MAXIMUM_CONNECTIONS)

    def sighandler(self, signum, frame):
        self.logger.info('SYSTEM - Shutting down server')
        for o in self.outputs:  # Close existing client sockets
            o.close()

        self.server.close()

    def terminate_session(self, incomming_connection):
        self.clients -= 1
        self.users.remove(incomming_connection)
        self.outputs.remove(incomming_connection)

    def serve(self):

        self.users = [self.server]
        self.outputs = []

        bool_running_flag = 1

        while bool_running_flag:
            try:
                inputready, outputready, exceptready = select.select(self.users, self.outputs, [])
            except select.error, e:
                break
            except socket.error, e:
                break

            for incomming_connection in inputready:

                if incomming_connection == self.server:  # Executes when a new client initially connects
                    client, address = self.server.accept()
                    self.logger.info('SYSTEM - Inbound connection %d from %s' % (client.fileno(), address))
                    # Compute client name and send back
                    self.clients += 1
                    self.users.append(client)
                    self.logger.info('SYSTEM - Total self.users: %d' % self.clients)
                    self.outputs.append(client)

                else:  # Follow on communications
                    try:
                        data = receive(incomming_connection)
                        if data:
                            for o in self.outputs:
                                send(o, data)
                        else:
                            incomming_connection.close()
                            self.terminate_session(incomming_connection)

                    except socket.error, e:
                        self.terminate_session(incomming_connection)

        self.server.close()


if __name__ == "__main__":
    Server().serve()
