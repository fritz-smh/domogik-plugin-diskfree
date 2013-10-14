#!/usr/bin/python
# -*- coding: utf-8 -*-


from domogik.tests.common.testdevice import TestDevice
from domogik.common.utils import get_sanitized_hostname


if __name__ == "__main__":

    td = TestDevice()
    td.create_device("plugin", "diskfree", get_sanitized_hostname(), "test_device_diskfree", "diskfree.disk_usage")
    td.configure_global_parameters({"device" : "/home", "interval" : 1})


# TODO : fonction pour supprimer tous les devices avec un nom donné
