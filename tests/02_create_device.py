#!/usr/bin/python
# -*- coding: utf-8 -*-


from domogik.tests.common.helpers import get_rest_url
from domogik.common.utils import get_sanitized_hostname
import requests
import json
import sys


class TestDevice():
    """ Tool to create test devices
    """

    def __init__(self):
        """ Construtor
            @param rest_url : url of the rest server
        """
        # rest url
        self.rest_url = get_rest_url()

        # package informations
        self.type = None
        self.id = None
        self.host = None

        # device informations
        self.device_name = None
        self.device_type = None

    def create_device(self, type, id, host, device_name, device_type):
        """ Call POST /device/... to create the device
        """
        # package informations
        self.type = type
        self.id = id
        self.host = host
        # device informations
        self.device_name = device_name
        self.device_type = device_type
        description = "a test device"
        reference = "for test only"
        print("Create a test device for the {0} {1} on {2}. Device type is '{3}', name is '{4}'".format(self.type,
                                                                                                          self.id,
                                                                                                          self.host,
                                                                                                          self.device_type,
                                                                                                          self.device_name))

        response = requests.post("{0}/device/".format(self.rest_url), \
            headers={'content-type':'application/x-www-form-urlencoded'},
            data="name={0}&type={1}&id={2}&host={3}&description={4}&reference={5}&device_type={6}".format(self.device_name,
                                                                                                          self.type,
                                                                                                          self.id,
                                                                                                          self.host,
                                                                                                          description,
                                                                                                          reference,
                                                                                                          self.device_type))
        print("Response : [{0}] {1}".format(response.status_code, response.text))
        if response.status_code != 201:
            raise RuntimeError("Error when creating the device")

        # get the device id for later calls to REST
        device = json.loads(response.text)
        self.device_id = device['id']
        print("The device id is '{0}'".format(self.device_id))

    def configure_global_parameters(self, params):
        """ Call PUT /device/addglobal/... to set the global parameters for a device
            @param params : dict of params
        """
        print("Configure the global parameters...")
        # build the data part
        first = True
        data = ""
        for key in params:
            if first == False:
                data += "&"
            else:
                first = False
            data += "{0}={1}".format(key, params[key])
        response = requests.put("{0}/device/addglobal/{1}".format(self.rest_url, self.device_id), \
                                 headers={'content-type':'application/x-www-form-urlencoded'},
                                 data="{0}".format(data))
        print("Response : [{0}] {1}".format(response.status_code, response.text))
        if response.status_code != 200:
            raise RuntimeError("Error when configuring the device global parameters")


if __name__ == "__main__":

    td = TestDevice()
    td.create_device("plugin", "diskfree", get_sanitized_hostname(), "test_device_diskfree", "diskfree.disk_usage")
    td.configure_global_parameters({"device" : "/home", "interval" : 1})


# TODO : gérer le host dynamiquement (fonction dans helpers ?)
# TODO : renommer le fichier pour pouvoir importer la fonction en lib
# TODO : fonction pour supprimer tous les devices avec un nom donné
