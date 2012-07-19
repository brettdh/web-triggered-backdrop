#!/usr/bin/env python2.7

import sys, os, time, threading, Queue
from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File

class Publisher(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.__stale_threshold = 1.0

        self.__clients = {}
        
    def getData(self, ip):
        with self.__lock:
            if ip not in self.__clients:
                self.__clients[ip] = Queue.Queue()
            queue = self.__clients[ip]
            
        return queue.get()

    def notifyAll(self, data):
        with self.__lock:
            for ip in self.__clients:
                queue = self.__clients[ip]
                queue.put(data)

publisher = Publisher()

class PushedResource(Resource):
    def render_GET(self, request):
        return publisher.getData(request.getClientIP())

class ReaderThread(threading.Thread):
    def run(self):
        while True:
            line = sys.stdin.readline()
            if not line or line.startswith("quit"):
                publisher.notifyAll("quit")
                break
            
            publisher.notifyAll(line.replace("\n", "<br/>"))


if __name__ == '__main__':
    root = File(os.getcwd())
    pushed_resource = PushedResource()
    root.putChild("published_text", pushed_resource)
    
    reader_thread = ReaderThread()
    reader_thread.start()

    reactor.listenTCP(8080, server.Site(root))
    reactor.run()

    reader_thread.join()
