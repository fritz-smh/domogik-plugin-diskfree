#!/usr/bin/python
# -*- coding: utf-8 -*-


from domogik.tests.common.testdevice import TestDevice
from domogik.common.utils import get_sanitized_hostname


if __name__ == "__main__":

    client_id = "plugin-diskfree.{0}".format(get_sanitized_hostname())
    td = TestDevice()
    params = td.get_params(client_id, "diskfree.disk_usage")

    # fill in the params
    params["device_type"] = "diskfree.disk_usage"
    params["name"] = "TestDevice"
    params["reference"] = "reference"
    params["description"] = "description"
    for idx, val in enumerate(params['no-xpl']):
        params['no-xpl'][idx]['value'] = 60
    for idx, val in enumerate(params['xpl']):
        params['xpl'][idx]['value'] = '/'

    # go and create
    td.create_device(params)


# TODO : fonction pour supprimer tous les devices avec un nom donné
