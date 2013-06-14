from twisted.web import server, resource
from twisted.internet import reactor

class HelloResource(resource.Resource):
    isLeaf = True
    number_requests = 0

    def render_GET(self, request):
        self.number_requests += 1
        request.setHeader("content-type", "text/plain")
        return "I'am requst #" + str(self.number_requests) + '\n'


reactor.listenTCP(12345, server.Site(HelloResource()))
reactor.run()
print 'stop run..'
