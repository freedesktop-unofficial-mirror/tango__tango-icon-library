#!/usr/bin/env python

import glob, os, sys, dircache, xml.dom.minidom
import new

INKSCAPE = "/usr/bin/inkscape"
SRC = "./svg"

# getText() by Mark Pilgrim
def getText(self):
    def isTextNode(node):
        return isinstance(node, xml.dom.minidom.Text)
    def getData(node):
        return node.data
    try:
        return "".join(map(getData, filter(isTextNode, self.childNodes)))
    except:
        return ""

def render(file):
    print "\t%s" % (file)
    svg = xml.dom.minidom.parse(SRC + "/" + file)
    for icon in svg.getElementsByTagName("g"):
        if icon.getAttribute("inkscape:label") != "plate":
            continue
        for in_node in icon.getElementsByTagName("text"):
            if in_node.getAttribute("inkscape:label") == "icon-name":
                icon_name = getText(in_node.getElementsByTagName("tspan")[0])
            if in_node.getAttribute("inkscape:label") == "context":
                context = getText(in_node.getElementsByTagName("tspan")[0])
        print "\t\t%s/%s" % (context, icon_name)
        for box in icon.getElementsByTagName("rect"):
            bid = box.getAttribute("id")
            size = "%sx%s" % (box.getAttribute("width"),
                              box.getAttribute("height"))
            destdir = "%s/%s" % (size, context)
            src = "%s/%s" % (SRC, file)
            dest = "%s/%s.png" % (destdir, icon_name)
            cmd = INKSCAPE + " -i " + bid + " -e " + dest + " " + src + " > /dev/null 2>&1"
            if not os.path.isdir(destdir):
                os.makedirs(destdir)
            print "\t\t\t%s/%s" % (destdir, icon_name)
            os.system(cmd)
    return

if len(sys.argv) < 2:
    print "Rendering from SVGs in %s" % (SRC)
    for file in dircache.listdir(SRC):
        if file.endswith(".svg"):
            render(file)
else:
    for svgname in sys.argv[1:]:
        file = svgname + ".svg"
        if os.path.isfile(SRC + "/" + file):
            render(file)
        else:
            print "Error: No such file: %s" % (file)

