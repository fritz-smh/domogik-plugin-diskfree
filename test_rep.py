#!/usr/bin/python
# -*- coding: utf-8 -*-
from domogik.mq.reqrep.worker import MQRep
from domogik.mq.message import MQMessage
from zmq.eventloop.ioloop import IOLoop
import zmq


class Rep(MQRep):

    def __init__(self):
        '''
        Initialize database and xPL connection
        '''
        MQRep.__init__(self, zmq.Context(), 'dbmgr')
        IOLoop.instance().start() 

    def on_mdp_request(self, msg):
        print(msg)
        self._mdp_reply()

    def _mdp_reply(self):
        msg = MQMessage()
        msg.set_action('config.result')
        msg.add_data('plugin', 'foo')
        print msg.get()
        self.reply(msg.get())


if __name__ == "__main__":
    Test = Rep()
