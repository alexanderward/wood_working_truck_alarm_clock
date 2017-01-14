from pubsub.broker import Broker


def test(message):
    print('Test Channel message: %s' % message)


def sample(message):
    print('Sample Channel message: %s' % message)


if __name__ == '__main__':
    broker = Broker()
    broker.subscribe('test')
    broker.subscribe('sample')
    for source, channel, message in broker.listen():
        if channel == 'test':
            test(message)
        elif channel == 'sample':
            sample(message)
