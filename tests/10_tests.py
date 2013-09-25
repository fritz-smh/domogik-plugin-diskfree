#!/usr/bin/python
# -*- coding: utf-8 -*-

from domogik.xpl.common.plugin import XplPlugin
from domogik.tests.common.plugintestcase import PluginTestCase
from domogik.tests.common.helpers import check_domogik_is_running
from domogik.tests.common.helpers import delete_configuration
from domogik.tests.common.helpers import configure
#from configure import configure
import unittest
import sys

class DiskfreeTestCase(PluginTestCase):
    """ This is the class containing all the tests for the plugin
    """

    # this function is the same for all plugins
    def __init__(self, testname, xpl_plugin, name, configuration):
        """ Constructor
            @param testname : used by unittest to choose the test to launch
            @param xpl_plugin : an instance of XplPlugin to allow to use xPL features 
            @param name : name of the plugin we are testing
            @param configuration : dict containing the plugin configuration
        """
        super(self.__class__, self).__init__(testname)
        self.myxpl = xpl_plugin.myxpl
        self.name = name
        self.configuration = configuration
        self.get_sanitized_hostname = xpl_plugin.get_sanitized_hostname

    # this function is the same for all plugins
    def test_0001_domogik_is_running(self):
        self.assertTrue(check_domogik_is_running())

    # this function is the same for all plugins
    def test_0010_configure_the_plugin(self):
        # first, clean the plugin configuration
        print("Delete the current plugin configuration")
        self.assertTrue(delete_configuration("plugin", self.name, self.get_sanitized_hostname()))
        for key in self.configuration:
            print("Set up configuration : {0} = {1}".format(key, self.configuration[key]))
            self.assertTrue(configure("plugin", self.name, self.get_sanitized_hostname(), key, self.configuration[key]))

    # this function is the same for all plugins
    def test_0020_create_the_devices(self):
        pass

    # this function is the same for all plugins
    def test_9999_hbeat(self):
        print("Check that a heartbeat is sent. This could take up to 5 minutes.")
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat", 
                                          xplschema = "hbeat.app", 
                                          xplsource = "domogik-{0}.{1}".format(self.name, self.get_sanitized_hostname()),
                                          timeout = 600))

    def test_0100_dummy(self):
        self.assertTrue(True)


if __name__ == "__main__":
    # TODO  : check domogik is up
    # TODO : allow to bypass hand questions for full auto tests
    # TODO : configure plugin
    # TODO : create devices
    # TODO : start plugin
    # TODO : ... and check the plugin is in the appropriate status
    # TODO : add some generic tests about plugin not configured, no devices created and check the plugin status ?

    # TODO : create a higher level class which handles all generic tests (00** and 99**)

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
    #suite.addTest(DiskfreeTestCase("test_0001_domogik_is_running", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0010_configure_the_plugin", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0100_dummy", xpl_plugin, name, cfg))
    #suite.addTest(DiskfreeTestCase("test_9999_hbeat", xpl_plugin, name, cfg))
    unittest.TextTestRunner().run(suite)
    
    xpl_plugin.force_leave()
    
