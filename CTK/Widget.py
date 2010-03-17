# CTK: Cherokee Toolkit
#
# Authors:
#      Alvaro Lopez Ortega <alvaro@alobbs.com>
#
# Copyright (C) 2009 Alvaro Lopez Ortega
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from consts import *
from PageCleaner import Postprocess

widget_uniq_id = 1;


class RenderResponse:
    def __init__ (self, html='', js='', headers=[], helps=[]):
        self.html    = html
        self.js      = js
        self.headers = headers[:]
        self.helps   = helps[:]

    def clean_up_headers (self):
        noDupes = []
        [noDupes.append(i) for i in self.headers if not noDupes.count(i)]
        self.headers = noDupes

    def __add__ (self, other):
        assert isinstance(other, RenderResponse)

        # New response obj
        i = RenderResponse()

        # Append the new response
        i.html    = self.html    + other.html
        i.js      = self.js      + other.js
        i.headers = self.headers + other.headers
        i.helps   = self.helps   + other.helps

        # Sort the headers
        i.clean_up_headers()
        return i

    def toStr (self):
        txt = self.html
        if self.js:
            txt += HTML_JS_ON_READY_BLOCK %(self.js)
        return Postprocess(txt)


class Widget:
    def __init__ (self):
        global widget_uniq_id;

        widget_uniq_id += 1;
        self.uniq_id = widget_uniq_id;
        self.id      = "widget_%d" %(widget_uniq_id)
        self.binds   = []

    def Render (self):
        render = RenderResponse()

        for event, js in self.binds:
            render.js += "$('#%s').bind('%s', function(){ %s });\n" %(self.id, event, js)

        return render

    # Javacript events
    #
    def bind (self, event, js):
        self.binds.append ((event, js))

    def JS_to_trigger (self, event, param=None):
        if param:
            return "$('#%s').trigger('%s', %s);" %(self.id, event, param)
        else:
            return "$('#%s').trigger('%s');" %(self.id, event)

