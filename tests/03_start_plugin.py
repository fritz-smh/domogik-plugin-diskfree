#!/usr/bin/python
# -*- coding: utf-8 -*-


from domogik.tests.common.testplugin import TestPlugin



tp = TestPlugin("diskfree", "darkstar")
tp.request_startup()
tp.wait_for_startup()

