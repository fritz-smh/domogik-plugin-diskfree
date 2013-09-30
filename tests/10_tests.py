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


if __name__ == "__main__":
    # TODO : allow to bypass hand questions for full auto tests
    # TODO : create devices
    # TODO : start plugin
    # TODO : ... and check the plugin is in the appropriate status
    # TODO : add some generic tests about plugin not configured, no devices created and check the plugin status ?

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
   

    # delete existing devices for this plugin on this host
    # TODO

    # create a test device
    #td = TestDevice()
    #td.create_device("plugin", "diskfree", get_sanitized_hostname(), "test_device_diskfree", "diskfree.disk_usage")
    #td.configure_global_parameters({"device" : "/home", "interval" : 1})

    ### prepare and run the test suite
    suite = unittest.TestSuite()
    # check domogik is running, configure the plugin
    suite.addTest(DiskfreeTestCase("test_0001_domogik_is_running", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0010_configure_the_plugin", xpl_plugin, name, cfg))
    
    # start the plugin
    # TODO : move in PluginTestCase and create some tests : test_0020
    tp = TestPlugin("diskfree", "darkstar")
    tp.request_startup()
    tp.wait_for_startup()

    # do the specific plugin tests
    suite.addTest(DiskfreeTestCase("test_0100_dummy", xpl_plugin, name, cfg))

    # do some tests comon to all the plugins
    suite.addTest(DiskfreeTestCase("test_9999_hbeat", xpl_plugin, name, cfg))
    unittest.TextTestRunner().run(suite)
    
    # quit
    xpl_plugin.force_leave()
    
