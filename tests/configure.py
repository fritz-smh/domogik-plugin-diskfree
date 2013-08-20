#!/usr/bin/python

import zmq
from zmq.eventloop.ioloop import IOLoop
from domogik.mq.reqrep.client import MQSyncReq
from domogik.mq.message import MQMessage


def configure(key, value):
    cli = MQSyncReq(zmq.Context())
    msg = MQMessage()
    msg.set_action('config.set')
    msg.add_data('type', 'plugin')
    msg.add_data('host', 'darkstar')
    msg.add_data('name', 'diskfree')
    msg.add_data('data', {key : value})
    print cli.request('dbmgr', msg.get(), timeout=10).get()



configure("configured", True)
configure("interval", 20)

