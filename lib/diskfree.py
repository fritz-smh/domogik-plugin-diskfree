# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
==============

Send disk usage (free, total, etc) over xPL

Implements
==========

- Disk

@author: Fritz <fritz.smh@gmail.com>
@copyright: (C) 2007-2012 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import os
import traceback



class Disk:
    """ Disk usage 
    """

    def __init__(self, log, callback, stop):
        """ Init Disk object
            @param log : log instance
            @param callback : callback
        """
        self.log = log
        self._callback = callback
        self._stop = stop

    def get_total_space(self, path, interval):
        """ Get total space on a path
        """
        while not self._stop.isSet():
            try:
                du = os.statvfs(path)
                du_total = (du.f_blocks * du.f_frsize) 
                self._callback(path, "total_space", du_total)
            except:
                self.log.error(u"Error for getting total space on path {0} : {1}".format(path, traceback.format_exc()))
            self._stop.wait(interval*60)
    
    
    def get_free_space(self, path, interval):
        """ Get free space on a path
        """
        while not self._stop.isSet():
            try:
                du = os.statvfs(path)
                du_free = (du.f_bavail * du.f_frsize) 
                self._callback(path, "free_space", du_free)
            except:
                self.log.error(u"Error for getting free space on path {0} : {1}".format(path, traceback.format_exc()))
            self._stop.wait(interval*60)
    
    
    def get_used_space(self, path, interval):
        """ Get used space on a path
        """
        while not self._stop.isSet():
            try:
                du = os.statvfs(path)
                #du_used = ((du.f_blocks - du.f_bfree) * du.f_frsize) 
                du_used = ((du.f_blocks - du.f_bavail) * du.f_frsize) 
                self._callback(path, "used_space", du_used)
            except:
                self.log.error(u"Error for getting used space on path {0} : {1}".format(path, traceback.format_exc()))
            self._stop.wait(interval*60)
    
    
    def get_percent_used(self, path, interval):
        """ Get space used in % on a path
        """
        while not self._stop.isSet():
            try:
                du = os.statvfs(path)
                du_total = (du.f_blocks * du.f_frsize) 
                #du_used = ((du.f_blocks - du.f_bfree) * du.f_frsize) 
                du_used = ((du.f_blocks - du.f_bavail) * du.f_frsize) 
                # notice : % value is less than real value (df command) because of reserved blocks
                try:
                    du_percent = (du_used * 100) / du_total
                except ZeroDivisionError:
                    du_percent = 0
                self._callback(path, "percent_used", du_percent)
            except:
                self.log.error(u"Error for getting percent used on path {0} : {1}".format(path, traceback.format_exc()))
            self._stop.wait(interval*60)
