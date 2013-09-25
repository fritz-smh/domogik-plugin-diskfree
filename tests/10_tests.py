#!/usr/bin/python
# -*- coding: utf-8 -*-

from domogik.xpl.common.plugin import XplPlugin
from domogik.tests.common.plugintestcase import PluginTestCase
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
    # TODO : clean existing configuration
    cfg = { 'configured' : True }

    
    # prepare and run the test suite
    suite = unittest.TestSuite()
    suite.addTest(DiskfreeTestCase("test_0001_domogik_is_running", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0010_configure_the_plugin", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0100_dummy", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_9999_hbeat", xpl_plugin, name, cfg))
    unittest.TextTestRunner().run(suite)
    
    xpl_plugin.force_leave()
    
