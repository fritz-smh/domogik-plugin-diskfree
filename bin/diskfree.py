#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
==============

Disk free

Implements
==========

- DiskManager

@author: Fritz <fritz.smh@gmail.com>
@copyright: (C) 2007-2012 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

from domogik.xpl.common.xplmessage import XplMessage
from domogik.xpl.common.plugin import XplPlugin
from domogik.xpl.common.queryconfig import Query
from domogik.mq.reqrep.client import MQSyncReq
from domogik.mq.message import MQMessage

from packages.plugin_diskfree.lib.diskfree import Disk
import threading
import traceback


class DiskManager(XplPlugin):
    """ Get disk free size over xPL
    """

    def __init__(self):
        """ Init plugin
        """
        XplPlugin.__init__(self, name='diskfree')

        # check if the plugin is configured. If not, this will stop the plugin and log an error
        if not self.check_configured():
            return

        # get interval between each check
        # TODO : configure this directly from the UI for each device
        self.interval = self.get_config("interval")

        # get the devices list
        self.devices = self.get_device_list()
        return

        # TODO : pour chaque device ajouter un param : intervalle
        #        creer une fonction dans la lib pour chaque fonctionnalité (get_total_space, ...)
        #        pour chaque sensor de chaque device, recuperer adresse+interval et appeler via un timer la fonction qui va bien
        #        envoyer le xpl correspondant
          



        ## Configuration : list of path to check
        #self.path_list = {}
        #num = 1
        #loop = True
        #while loop == True:
        #    path = self._config.query('diskfree', 'path-%s' % str(num))
        #    if path != None:
        #        self.log.info("Configuration : path=%s" % path)
        #        num += 1
        #        # init object list for path to None
        #        self.path_list[path] = None
        #    else:
        #        loop = False

        # no path configured
        #if num == 1:
        #    msg = "No path configured. Exiting plugin"
        #    self.log.info(msg)
        #    print(msg)
        #    self.force_leave()
        #    return
            
        ### Start listening each path
        for path in self.path_list:
            try:
                self.path_list[path] = Disk(self.log, self.send_xpl, self.get_stop())
                self.log.info("Start listening for '%s'" % path)
                path_listen = threading.Thread(None,
                                              self.path_list[path].listen,
                                              "listen_diskfree",
                                              (path, interval,),
                                              {})
                path_listen.start()
            except:
                self.log.error(traceback.format_exc())
                print(traceback.format_exc())
                # we don't quit plugin if an error occured
                # a disk can have been unmounted for a while
                #self.force_leave()
                #return

        self.ready()
        self.log.info("Plugin ready :)")


    def send_xpl(self, path, du_type, du_value):
        """ Send xPL message on network
        """
        print("path:%s, %s:%s" % (path, du_type, du_value))
        msg = XplMessage()
        msg.set_type("xpl-stat")
        msg.set_schema("sensor.basic")
        msg.add_data({"device" : path})
        msg.add_data({"type" : du_type})
        msg.add_data({"current" : du_value})
        self.myxpl.send(msg)


if __name__ == "__main__":
    DiskManager()
