#!/usr/bin/python

from domogik.tests.common.helpers import configure, delete_configuration

delete_configuration("plugin", "diskfree", get_sanitized_hostname())
configure("plugin", "diskfree", get_sanitized_hostname(), "configured", True)

