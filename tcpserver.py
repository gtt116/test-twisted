from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        data = 'PS:' + data
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print addr
        return Echo()


reactor.listenTCP(12345, EchoFactory())
reactor.run()
