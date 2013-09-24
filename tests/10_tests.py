#!/usr/bin/python
# -*- coding: utf-8 -*-

from domogik.xpl.common.plugin import XplPlugin
from domogik.tests.common.plugintestcase import PluginTestCase
import unittest

class DiskfreeTestCase(PluginTestCase):
    """ This is the class containing all the tests for the plugin
    """

    def __init__(self, testname, xpl_plugin, name):
        """ Constructor
            @param testname : used by unittest to choose the test to launch
            @param xpl_plugin : an instance of XplPlugin to allow to use xPL features 
            @param name : name of the plugin we are testing
        """
        super(DiskfreeTestCase, self).__init__(testname)
        self.myxpl = xpl_plugin.myxpl
        self.name = name
        self.get_sanitized_hostname = xpl_plugin.get_sanitized_hostname

    def test_9999_hbeat(self):
        print("Check that a heartbeat is sent. This could take up to 5 minutes.")
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat", 
                                          xplschema = "hbeat.app", 
                                          xplsource = "domogik-diskfree.{0}".format(self.get_sanitized_hostname()),
                                          timeout = 600))

    def test_200_hbeat(self):
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat", 
                                          xplschema = "sensor.basic", 
                                          timeout = 120))


xpl_plugin = XplPlugin(name = 'test', 
                       daemonize = False, 
                       parser = None, 
                       nohub = True,
                       test  = True)
name = "diskfree"

suite = unittest.TestSuite()
suite.addTest(DiskfreeTestCase("test_9999_hbeat", xpl_plugin, name))
unittest.TextTestRunner().run(suite)

xpl_plugin.force_leave()

