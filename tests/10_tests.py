#!/usr/bin/python
# -*- coding: utf-8 -*-

from domogik.xpl.common.plugin import XplPlugin
from domogik.tests.common.plugintestcase import PluginTestCase
from domogik.tests.common.testplugin import TestPlugin
from domogik.tests.common.testdevice import TestDevice
from domogik.common.utils import get_sanitized_hostname
import unittest
import sys

class DiskfreeTestCase(PluginTestCase):

    def test_0100_dummy(self):
        self.assertTrue(True)

    def test_0110_total_space(self):
        """ check if the xpl messages about total space are OK
            Sample message : 
            xpl-stat
            {
            hop=1
            source=domogik-diskfree.darkstar
            target=*
            }
            sensor.basic
            {
            device=/home
            type=total_space
            current=19465224
            }
        """
        global interval
        print("Check that a message about total space is sent. The message must be received each {0} minute(s)".format(interval))
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "total_space", 
                                                  "device" : "/home"},
                                          timeout = interval * 60))
        # TODO : do it twice to check the interval is ok


    def test_0120_free_space(self):
        """ check if the xpl messages about free space are OK
            Sample message : 
            xpl-stat
            {
            hop=1
            source=domogik-diskfree.darkstar
            target=*
            }
            sensor.basic
            {
            device=/home
            type=free_space
            current=4109696
            }
        """
        pass

    def test_0130_used_space(self):
        """ check if the xpl messages about used space are OK
            Sample message : 
            xpl-stat
            {
            hop=1
            source=domogik-diskfree.darkstar
            target=*
            }
            sensor.basic
            {
            device=/home
            type=used_space
            current=14378992
            }
        """
        pass

    def test_0140_percent_used(self):
        """ check if the xpl messages about percent used are OK
            Sample message : 
            xpl-stat
            {
            hop=1
            source=domogik-diskfree.darkstar
            target=*
            }
            sensor.basic
            {
            device=/home
            type=percent_used
            current=73
            }
        """
        pass

    # TODO : tests about the interval

if __name__ == "__main__":
    # TODO : allow to bypass hand questions for full auto tests
    # TODO : create devices
    # TODO : start plugin
    # TODO : ... and check the plugin is in the appropriate status
    # TODO : add some generic tests about plugin not configured, no devices created and check the plugin status ?

    ### global variables
    interval = 1    

    ### configuration

    # set up the xpl features
    xpl_plugin = XplPlugin(name = 'test', 
                           daemonize = False, 
                           parser = None, 
                           nohub = True,
                           test  = True)

    # set up the plugin name
    name = "diskfree"

    # set up the configuration of the plugin
    # configuration is done in test_0010_configure_the_plugin with the cfg content
    # notice that the old configuration is deleted before
    cfg = { 'configured' : True }
   

    ### start tests

    # delete existing devices for this plugin on this host
    # TODO

    # create a test device
    #td = TestDevice()
    #td.create_device("plugin", "diskfree", get_sanitized_hostname(), "test_device_diskfree", "diskfree.disk_usage")
    #td.configure_global_parameters({"device" : "/home", "interval" : interval})

    ### prepare and run the test suite
    suite = unittest.TestSuite()
    # check domogik is running, configure the plugin
    suite.addTest(DiskfreeTestCase("test_0001_domogik_is_running", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0010_configure_the_plugin", xpl_plugin, name, cfg))
    
    # start the plugin
    # TODO : move in PluginTestCase and create some tests : test_0020
    #tp = TestPlugin("diskfree", "darkstar")
    #tp.request_startup()
    #tp.wait_for_startup()

    # do the specific plugin tests
    suite.addTest(DiskfreeTestCase("test_0100_dummy", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0110_total_space", xpl_plugin, name, cfg))

    # do some tests comon to all the plugins
    suite.addTest(DiskfreeTestCase("test_9999_hbeat", xpl_plugin, name, cfg))
    unittest.TextTestRunner().run(suite)
    
    # quit
    xpl_plugin.force_leave()
    
