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

from domogik_packages.plugin_diskfree.lib.diskfree import Disk
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
        #if not self.check_configured():
        #    return

        # get the devices list
        self.devices = self.get_device_list(quit_if_no_device = True)
       

        disk_manager = Disk(self.log, self.send_xpl, self.get_stop())

        ### Start listening each path
        threads = {}
        for a_device in self.devices:
            try:
                # global device parameters
                interval = self.get_parameter(a_device, "interval")

                # feature get_total_space
                path = self.get_parameter_for_feature(a_device, "xpl_stats", "get_total_space", "device")
                if path == None or interval == None:
                    self.log.error(u"Invalid values for device '{0}' : path = '{1}' / interval = '{2}'. Nothing will be done for this device!".format(a_device['name'], path, interval))
                    break
                self.log.info(u"Start monitoring total space for '%s'" % path)
                thr_name = "dev_{0}-{1}".format(a_device['id'], "get_total_space")
                threads[thr_name] = threading.Thread(None,
                                               disk_manager.get_total_space,
                                              thr_name,
                                              (path, interval,),
                                              {})
                threads[thr_name].start()
                self.register_thread(threads[thr_name])

                # feature get_free_space
                path = self.get_parameter_for_feature(a_device, "xpl_stats", "get_free_space", "device")
                self.log.info(u"Start monitoring free space for '%s'" % path)
                thr_name = "dev_{0}-{1}".format(a_device['id'], "get_free_space")
                threads[thr_name] = threading.Thread(None,
                                               disk_manager.get_free_space,
                                              thr_name,
                                              (path, interval,),
                                              {})
                threads[thr_name].start()
                self.register_thread(threads[thr_name])

                # feature get_used_space
                path = self.get_parameter_for_feature(a_device, "xpl_stats", "get_used_space", "device")
                self.log.info(u"Start monitoring used space for '%s'" % path)
                thr_name = "dev_{0}-{1}".format(a_device['id'], "get_used_space")
                threads[thr_name] = threading.Thread(None,
                                               disk_manager.get_used_space,
                                              thr_name,
                                              (path, interval,),
                                              {})
                threads[thr_name].start()
                self.register_thread(threads[thr_name])

                # feature get_percent_used
                path = self.get_parameter_for_feature(a_device, "xpl_stats", "get_percent_used", "device")
                self.log.info(u"Start monitoring percent used for '%s'" % path)
                thr_name = "dev_{0}-{1}".format(a_device['id'], "get_percent_used")
                threads[thr_name] = threading.Thread(None,
                                               disk_manager.get_percent_used,
                                              thr_name,
                                              (path, interval,),
                                              {})
                threads[thr_name].start()
                self.register_thread(threads[thr_name])

            except:
                self.log.error(u"{0}".format(traceback.format_exc()))
                # we don't quit plugin if an error occured
                # a disk can have been unmounted for a while
                #self.force_leave()
                #return



        self.ready()


    def send_xpl(self, path, du_type, du_value):
        """ Send xPL message on network
        """
        self.log.debug(u"Values for {0} on {1} : {2}".format(du_type, path, du_value))
        msg = XplMessage()
        msg.set_type("xpl-stat")
        msg.set_schema("sensor.basic")
        msg.add_data({"device" : path})
        msg.add_data({"type" : du_type})
        msg.add_data({"current" : du_value})
        self.myxpl.send(msg)


if __name__ == "__main__":
    DiskManager()
