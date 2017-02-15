#!/usr/bin/env python

##  extract.py - convert pdf into images and html files
##
##  Copyright (C) 2010 Willem Jan Faber
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##


import os, os.path, sys, warnings
from pprint import pprint
warnings.simplefilter("ignore",DeprecationWarning)
import urllib

try:
    from pyPdf import PdfFileWriter, PdfFileReader
except Exception as e:
    sys.stdout.write(str(e) + '\n')
    sys.stdout.write("PyPdf not found\nsudo apt-get install python-pypdf\n")
    sys.exit(-1)

try:
    import poppler
except Exception as e:
    sys.stdout.write(str(e) + '\n')
    sys.stdout.write("poppler not found\nsudo apt-get install python-poppler\n")
    sys.exit(-1)

try:
    import gtk
except Exception as e:
    sys.stdout.write(str(e) + '\n')
    sys.stdout.write("gtk not found\nsudo apt-get install python-gtk2\n")
    sys.exit(-1)

class pdf2png(object):
    def __init__(self, ifname, ofname, width = 1024, height = 1322):
        self.width = width
        self.height = height
        self.ifname = ifname
        self.ofname = ofname

        self.doc = poppler.document_new_from_file('file://%s' % \
            urllib.pathname2url(self.ifname), password = None)

    def out(self, pagenr):
        page = self.doc.get_page(pagenr)
        ww = self.width
        wh = self.height
        pw, ph = page.get_size()
        with gtk.gdk.lock:
                # Render to a pixmap
                pixmap = gtk.gdk.Pixmap(None, ww, wh, 24) # FIXME: 24 or 32?
                cr = pixmap.cairo_create()
                cr.set_source_rgb(1, 1, 1)

                scale = min(ww/pw, wh/ph)
                cr.scale(scale, scale)

                cr.rectangle(0, 0, pw, ph)
                cr.fill()
                page.render(cr)

                # Convert pixmap to pixbuf
                pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, ww, wh)
                pixbuf.get_from_drawable(pixmap, gtk.gdk.colormap_get_system(),
                                         0, 0, 0, 0, ww, wh)

#        page.render_to_pixbuf(src_x = 0, src_y = 0, src_width = self.width, src_height = self.height, \
#            scale = self.width/page.get_size()[0], rotation=0, pixbuf = pixbuf)
        pixbuf.save(self.ofname + os.sep + str(pagenr) + ".png", 'png')

class parse_pdf(object):
    """
        parses the pdf and generate an index file
    """
    def __init__(self, fname):
        self.fhandle = open(fname)
        fhandle = PdfFileReader(self.fhandle)
        new_path = os.sep.join(fname.split('/')[0:-1]) + os.sep + ".".join(fname.split('/')[-1].split('.')[0:-1])
        png = pdf2png(fname, new_path)

        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        for i in range(1, fhandle.numPages):
            print("Parsing page " + str(i))
            data = os.popen('pdftohtml -nodrm -stdout -p -i -f ' + str(i) + ' -l ' + str(i) + ' "' + fname + '"').read()
            data = data.replace('</HEAD>', '<link href="../book_style.css" rel="stylesheet" type="text/css"/>\n</HEAD>')
            data = data.replace('<BODY bgcolor="#A0A0A0" vlink="blue" link="blue">','<BODY>')
            new_fname = new_path+os.sep + str(i)
            f=open(new_fname + ".html", "w")
            f.write(data)
            f.close()
            print("\t\thtml done")
            png.out(i-1)
            print("\t\tpng done")

    def sub(self, inv):
        inv=ord(inv)
        if ( (inv >= 8) and (inv <= 10)):
            return(True)
        if ((inv >= 32 ) and (inv <= 126)):
            return(True)
        if ((inv >= 160) and (inv <= 256)):
            return(True)
        return(False)

    def pstr(self, buff_in):
        buff=[]
        for item in buff_in:
            if self.sub(item):
                buff.append(item)
            else:
                buff.append('\n')
        return("".join(buff).replace('\n','<br>\n'))

if __name__ == "__main__":
    try:
        work_path = os.path.abspath(sys.argv[1])
    except:
        work_path = ""
    if (not os.path.isdir(work_path)) or (len(sys.argv) == 1):
        sys.stdout.write("Usage : " + os.path.abspath(sys.argv[0]).split('/')[-1] + " <path to pdf_files>\n")
        sys.exit(0)

    print("Working on path : " + work_path)

    for fname in os.listdir(work_path):
        if fname.lower().endswith(".pdf"):
             print("Parsing : " + os.path.abspath(work_path+os.sep+fname))
             parser = parse_pdf(os.path.abspath(work_path + os.sep+fname))
