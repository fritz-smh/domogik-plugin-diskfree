#!/usr/bin/python
# -*- coding: utf-8 -*-

from domogik.xpl.common.plugin import XplPlugin
from domogik.tests.common.plugintestcase import PluginTestCase
from domogik.tests.common.testplugin import TestPlugin
from domogik.tests.common.testdevice import TestDevice
from domogik.tests.common.testsensor import TestSensor
from domogik.common.utils import get_sanitized_hostname
from datetime import datetime
import unittest
import sys
import os
import traceback
import time

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
        global path
        global device_id

        # get the current total space on the device
        du = os.statvfs(path)
        du_total = (du.f_blocks * du.f_frsize) 

        # do the test
        print(u"Check that a message about total space is sent. The message must be received each {0} minute(s)".format(interval))
        
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "total_space", 
                                                  "device" : path,
                                                  "current" : du_total},
                                          timeout = interval * 60))
        print(u"Check that the value of the xPL message has been inserted in database")
        sensor = TestSensor(device_id, "get_total_space")
        self.assertTrue(sensor.get_last_value()[1] == self.xpl_data.data['current'])
        msg1_time = datetime.now()
        
        # TODO doc : tell that the last xpl message is available in self.xpl_data

        print(u"Check there is a second message is sent and the interval between them")
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "total_space", 
                                                  "device" : path,
                                                  "current" : du_total},
                                          timeout = interval * 60))
        msg2_time = datetime.now()
        self.assertTrue(self.is_interval_of(interval * 60, msg2_time - msg1_time))


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
        global interval
        global path
        global device_id

        # do the test
        print(u"Check that a message about free space is sent. The message must be received each {0} minute(s)".format(interval))
        
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "free_space", 
                                                  "device" : path},
                                          timeout = interval * 60))

        msg1_time = datetime.now()
        xpl_current = float(self.xpl_data.data['current'])
        # get the current free space on the device
        du = os.statvfs(path)
        du_free_space = float((du.f_bavail * du.f_frsize))
        diff_percent = float(abs(float(xpl_current) - du_free_space)/du_free_space)
        # as the disk free size can change, we assume that a difference which is less than 2% is a good result)
        if diff_percent > 0.02:
            ok = False
        else:
            ok = True
        print(u"Real free size on disk = {0}".format(du_free_space))
        print(u"Plugin indicates free size on disk = {0}".format(xpl_current))
        print(u"The allowed difference is 2%. The difference is {0}%".format(diff_percent*100))
        self.assertTrue(ok)

        print(u"Check that the value of the xPL message has been inserted in database")
        sensor = TestSensor(device_id, "get_free_space")
        self.assertTrue(float(sensor.get_last_value()[1]) == float(xpl_current))

        # TODO doc : tell that the last xpl message is available in self.xpl_data
        # TODO doc : tell to use percent comparison for non fixed values

        print(u"Check there is a second message is sent and the interval between them")
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "free_space", 
                                                  "device" : path},
                                          timeout = interval * 60))
        msg2_time = datetime.now()
        self.assertTrue(self.is_interval_of(interval * 60, msg2_time - msg1_time))

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
        global interval
        global path
        global device_id

        # do the test
        print(u"Check that a message about used space is sent. The message must be received each {0} minute(s)".format(interval))
        
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "used_space", 
                                                  "device" : path},
                                          timeout = interval * 60))
        msg1_time = datetime.now()
        xpl_current = float(self.xpl_data.data['current'])
        # get the current used space on the device
        du = os.statvfs(path)
        #du_used = float(((du.f_blocks - du.f_bfree) * du.f_frsize))
        du_used = float(((du.f_blocks - du.f_bavail) * du.f_frsize))
        diff_percent = float(abs(float(xpl_current) - du_used)/du_used)
        # as the disk used size can change, we assume that a difference which is less than 2% is a good result)
        if diff_percent > 0.02:
            ok = False
        else:
            ok = True
        print(u"Real used size on disk = {0}".format(du_used))
        print(u"Plugin indicates used size on disk = {0}".format(xpl_current))
        print(u"The allowed difference is 2%. The difference is {0}%".format(diff_percent*100))
        self.assertTrue(ok)

        # TODO : move after the second message received 
        print(u"Check that the value of the xPL message has been inserted in database")
        sensor = TestSensor(device_id, "get_used_space")
        self.assertTrue(float(sensor.get_last_value()[1]) == float(xpl_current))

        # TODO doc : tell that the last xpl message is available in self.xpl_data
        # TODO doc : tell to use percent comparison for non fixed values

        print(u"Check there is a second message is sent and the interval between them")
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "used_space", 
                                                  "device" : path},
                                          timeout = interval * 60))
        msg2_time = datetime.now()
        self.assertTrue(self.is_interval_of(interval * 60, msg2_time - msg1_time))


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
        global interval
        global path
        global device_id

        # do the test
        print(u"Check that a message about percent used is sent. The message must be received each {0} minute(s)".format(interval))
        
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "percent_used", 
                                                  "device" : path},
                                          timeout = interval * 60))
        msg1_time = datetime.now()
        xpl_current = float(self.xpl_data.data['current'])

        # get the current percent used of the device
        du = os.statvfs(path)
        du_total = (du.f_blocks * du.f_frsize) 
        #du_used = ((du.f_blocks - du.f_bfree) * du.f_frsize)
        du_used = ((du.f_blocks - du.f_bavail) * du.f_frsize)
        # notice : % value is less than real value (df command) because of reserved blocks
        try:
            du_percent = (du_used * 100) / du_total
        except ZeroDivisionError:
            du_percent = 0

        diff_percent = float(abs(float(xpl_current) - du_percent)/du_percent)
        # as the disk percent used can change, we assume that a difference which is less than 2% is a good result)
        if diff_percent > 0.02:
            ok = False
        else:
            ok = True
        print(u"Real percent used of the disk = {0}".format(du_percent))
        print(u"Plugin indicates percend used of the disk = {0}".format(xpl_current))
        print(u"The allowed difference is 2%. The difference is {0}%".format(diff_percent*100))
        self.assertTrue(ok)

        print(u"Check that the value of the xPL message has been inserted in database")
        sensor = TestSensor(device_id, "get_percent_used")
        self.assertTrue(float(sensor.get_last_value()[1]) == float(xpl_current))

        # TODO doc : tell that the last xpl message is available in self.xpl_data
        # TODO doc : tell to use percent comparison for non fixed values

        print(u"Check there is a second message is sent and the interval between them")
        self.assertTrue(self.wait_for_xpl(xpltype = "xpl-stat",
                                          xplschema = "sensor.basic",
                                          xplsource = "domogik-{0}.{1}".format(self.name, get_sanitized_hostname()),
                                          data = {"type" : "percent_used", 
                                                  "device" : path},
                                          timeout = interval * 60))
        msg2_time = datetime.now()
        self.assertTrue(self.is_interval_of(interval * 60, msg2_time - msg1_time))


if __name__ == "__main__":
    ### global variables
    interval = 1    
    path = "/home"

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

    # load the test devices class
    td = TestDevice()

    # delete existing devices for this plugin on this host
    client_id = "{0}-{1}.{2}".format("plugin", name, get_sanitized_hostname())
    try:
        td.del_devices_by_client(client_id)
    except: 
        print(u"Error while deleting all the test device for the client id '{0}' : {1}".format(client_id, traceback.format_exc()))
        sys.exit(1)

    # create a test device
    #try:
    #    device_id = td.create_device(client_id, "test_device_diskfree", "diskfree.disk_usage")
    #    td.configure_global_parameters({"device" : path, "interval" : interval})
    #except: 
    #    print(u"Error while creating the test devices : {0}".format(traceback.format_exc()))
    #    sys.exit(1)

    # create a test device
    try:
        params = td.get_params(client_id, "diskfree.disk_usage")

        # fill in the params
        params["device_type"] = "diskfree.disk_usage"
        params["name"] = "test_device_diskfree"
        params["reference"] = "reference"
        params["description"] = "description"
        # global params
        for the_param in params['global']:
            if the_param['key'] == "interval":
                the_param['value'] = interval
        print params['global']
        # xpl params
        for the_param in params['xpl']:
            if the_param['key'] == "device":
                the_param['value'] = path
        print params['xpl']
        # create
        device_id = td.create_device(params)['id']

    except:
        print(u"Error while creating the test devices : {0}".format(traceback.format_exc()))
        sys.exit(1)

    
    ### prepare and run the test suite
    suite = unittest.TestSuite()
    # check domogik is running, configure the plugin
    suite.addTest(DiskfreeTestCase("test_0001_domogik_is_running", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0010_configure_the_plugin", xpl_plugin, name, cfg))
    
    # start the plugin
    suite.addTest(DiskfreeTestCase("test_0050_start_the_plugin", xpl_plugin, name, cfg))

    # do the specific plugin tests
    #suite.addTest(DiskfreeTestCase("test_0100_dummy", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0110_total_space", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0120_free_space", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0130_used_space", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_0140_percent_used", xpl_plugin, name, cfg))
    # wait for 2 seconds... why ? well... this is quite embarrasing to explain!
    # on my laptop, when the "stop the plugin" test is launched, an "active" 
    # plugin.status message is sent just before the "stopped" plugin.status 
    # message... and so, the plugin is seen as still active and the test fails
    # yeah, this need to be fixed in the testplugin.py file, but this will be 
    # done later so...
    time.sleep(2)

    # do some tests comon to all the plugins
    #suite.addTest(DiskfreeTestCase("test_9900_hbeat", xpl_plugin, name, cfg))
    suite.addTest(DiskfreeTestCase("test_9990_stop_the_plugin", xpl_plugin, name, cfg))
    
    # quit
    res = unittest.TextTestRunner().run(suite)
    if res.wasSuccessful() == True:
        rc = 0   # tests are ok so the shell return code is 0
    else:
        rc = 1   # tests are ok so the shell return code is != 0
    xpl_plugin.force_leave(return_code = rc)
     
    
