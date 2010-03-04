#!/usr/bin/env python 
'''
Copyright (C) 2008 Aaron Spike, aaron@ekips.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
import inkex, math

class MyEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--icons",
                        action="store", type="int", 
                        dest="icons", default=1,
                        help="number of icon templates to create")
        self.OptionParser.add_option("--columns",
                        action="store", type="int", 
                        dest="columns", default=1,
                        help="wrap the icon templates after this many columns")
        self.OptionParser.add_option("--offset",
                        action="store", type="int", 
                        dest="offset", default=0,
                        help="skip this number of icon templates before creating more")
    def add_layer(self, name, parent=None):
        attr = {inkex.addNS('groupmode','inkscape'):'layer',
                inkex.addNS('label','inkscape'):name,
                'style':'display:inline'
               }
        if parent is None:
            parent = self.document.getroot()
        return inkex.etree.SubElement(parent, inkex.addNS('g','svg'), attr)
    def add_square(self, size, x, y, parent):
        attr = {inkex.addNS('label','inkscape'):'%sx%s' % (size, size),
                'width':str(size),
                'height':str(size),
                'x':str(x),
                'y':str(y),
                'style':'opacity:1;fill:#eeeeec;fill-opacity:1;fill-rule:nonzero;stroke:none;visibility:visible;display:inline;enable-background:accumulate'
               }
        return inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attr)
    def add_text(self, label, x, y, parent, bold=False):
        attr = {inkex.addNS('label','inkscape'):label,
                'x':str(x),
                'y':str(y),
                'style':'font-size:18px;font-style:normal;font-weight:normal;fill:#000000;fill-opacity:1;stroke:none;display:inline;enable-background:new;font-family:Bitstream Vera Sans'
               }
        text = inkex.etree.SubElement(parent, inkex.addNS('text','svg'), attr)
        tspan = inkex.etree.SubElement(text, inkex.addNS('tspan','svg'))
        tspan.text = label
        return text
    def effect(self):
        width=400
        height=300
        for icon in range(self.options.offset, self.options.offset+self.options.icons):
            row = icon / self.options.columns
            column = icon % self.options.columns
            top = height * row
            left = width * column
            icon_layer = self.add_layer('icon %s' % icon)
            plate = self.add_layer('baseplate %s' % icon, icon_layer)
            self.add_square(256, left + 20, top + 30, plate)
            self.add_square(48, left + 300, top + 50, plate)
            self.add_square(32, left + 300, top + 125, plate)
            self.add_square(24, left + 300, top + 176, plate)
            self.add_square(22, left + 301, top + 177, plate)
            self.add_square(16, left + 300, top + 220, plate)
            self.add_text('context', left + 20, top + 20, plate)
            self.add_text('icon-name', left + 200, top + 20, plate)
        doc_width = self.options.columns * width
        doc_height = math.ceil(((self.options.offset+self.options.icons) / float(self.options.columns))) * height
        doc = self.document.getroot()
        doc.set('width', str(doc_width))
        doc.set('height', str(doc_height))

if __name__ == '__main__':
    e = MyEffect()
    e.affect()

# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 encoding=utf-8 textwidth=99
