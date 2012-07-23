#!/usr/bin/env python

import sys, os, time, threading, Queue
from twisted.web import server
from twisted.web.server import NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File

def print_on_enter(fn):
    def printing_fn(*args):
        print "entering %s" % fn.func_name
        ret = fn(*args)
        print "leaving %s" % fn.func_name
        return ret
    return printing_fn

class Publisher(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.__requests = []
        
    def registerForData(self, request):
        with self.__lock:
            print ("%s  **  got request: %s (total: %d)" %
                   (time.ctime(), str(request), len(self.__requests) + 1))
            self.__requests.append(request)

    def notifyAll(self, data):
        with self.__lock:
            print "  Sending %d responses" % len(self.__requests)
            for request in self.__requests:
                request.write(data)
                request.finish()
            del self.__requests[:]

    def cancel(self, request):
        with self.__lock:
            try:
                self.__requests.remove(request)
            except ValueError, e:
                pass # ignore

publisher = Publisher()

class PushedResource(Resource):
    def _responseFailed(self, err, request):
        print err
        publisher.cancel(request)

    def render_GET(self, request):
        request.notifyFinish().addErrback(self._responseFailed, request)
        publisher.registerForData(request)
        return NOT_DONE_YET

class ReaderThread(threading.Thread):
    def run(self):
        while True:
            line = sys.stdin.readline()
            if not line or line.startswith("quit"):
                publisher.notifyAll("quit")
                break
            
            publisher.notifyAll(line.replace("\n", "<br/>"))

class Trigger(Resource):
    def render_GET(self, request):
        publisher.notifyAll("boom")
        return "boom"

if __name__ == '__main__':
    root = File(os.getcwd())
    pushed_resource = PushedResource()
    root.putChild("published_text", pushed_resource)
    root.putChild("control", File("/control.html"))
    root.putChild("control_mobile", File("/control_mobile.html"))

    trigger = Trigger()
    root.putChild("trigger", trigger)
    
    reader_thread = ReaderThread()
    reader_thread.start()

    reactor.listenTCP(9999, server.Site(root))
    reactor.run()

    reader_thread.join()
