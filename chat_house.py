from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = 'GETNAME'

    def connectionMade(self):
        self.sendLine("what's your name?")

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]
        message = '<%s> is gone...' % self.name
        for user, protocol in self.users.iteritems():
            if user != self.name:
                protocol.sendLine(message)

    def lineReceived(self, line):
        if self.state == 'GETNAME':
            self.handle_getname(line)
        else:
            self.handle_chat(line)

    def handle_getname(self, name):
        if self.users.has_key(name):
            self.sendLine('Name taken, Choose another..')
            return
        self.sendLine('Welcome, %s' % name)
        self.name = name
        self.users[name] = self
        self.state = 'CHAT'

    def handle_chat(self, line):
        message = '<%s> %s' % (self.name, line)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Chat(self.users)


reactor.listenTCP(12345, ChatFactory())
reactor.run()
