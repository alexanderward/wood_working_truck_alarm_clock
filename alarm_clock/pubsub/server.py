import select
import socket
import logging
import signal
from pubsub.networking.communication import send, receive, SocketError
from pubsub.networking.constants import SERVER_PORT, MAXIMUM_CONNECTIONS


class Server(object):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Server')

    def __init__(self):
        self.clients = 0
        self.client_map = {}  # Client map
        self.outputs = []  # Output socket list
        self.user_dict = {}
        self.setup_socket()
        signal.signal(signal.SIGINT, self.sighandler)  # Trap keyboard interrupts

    def setup_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', SERVER_PORT))
        self.logger.info('SYSTEM - Listening to port %s' % SERVER_PORT)
        self.server.listen(MAXIMUM_CONNECTIONS)
        self.users = [self.server]

    def sighandler(self, signum, frame):
        self.logger.info('SYSTEM - Shutting down server')
        for o in self.outputs:  # Close existing client sockets
            o.close()

        self.server.close()

    def log_total_users(self):
        self.logger.info('SYSTEM - Total self.users: %d' % self.clients)

    def update_users(self, client, address):
        self.clients += 1
        self.users.append(client)
        self.outputs.append(client)
        if address[0] not in self.user_dict:
            self.user_dict[address[0]] = [address[1]]
        elif address[1] not in self.user_dict[address[0]]:
            self.user_dict[address[0]].append(address[1])
        self.logger.info("SYSTEM - Current Users: %s" % str(self.user_dict))

    def terminate_session(self, incomming_connection):
        try:
            self.clients -= 1
            self.users.remove(incomming_connection)
            self.outputs.remove(incomming_connection)
            self.log_total_users()
            ip, port = incomming_connection.getpeername()
            self.user_dict[ip].remove(port)
            if len(self.user_dict[ip]) == 0:
                del self.user_dict[ip]
            self.logger.info("SYSTEM - Current Users: %s" % str(self.user_dict))
        except ValueError:
            pass

    def serve(self):
        while True:
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
                    self.update_users(client, address)
                    self.log_total_users()

                else:  # Follow on communications
                    try:
                        data = receive(incomming_connection)
                        if isinstance(data, SocketError):
                            self.terminate_session(incomming_connection)
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
