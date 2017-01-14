import time

from pubsub.broker import Broker

if __name__ == '__main__':
    broker = Broker()
    counter = 1
    while 1:
        message = {'user2': 'message #%s' % counter}
        broker.publish(source='test_user1.py', channel='test', message=message)
        counter += 1
        time.sleep(5)
