#!/usr/bin/env python3

# The MIT License (MIT)
# Copyright (c) 2018 Esukhia
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import re
import os

TEI_BEGINNING = """<?xml version="1.0" encoding="UTF-8"?>
<tei:TEI xmlns:tei="http://www.tei-c.org/ns/1.0">
  <tei:teiHeader>
    <tei:fileDesc>
      <tei:titleStmt>
        <tei:title>{title} [{volnum}]</tei:title>
      </tei:titleStmt>
      <tei:publicationStmt>
        <tei:distributor>Text input by Esukhia for 84000, with support from BDRC and THDL at UVa. This TEI files has been automatically produced by a script from raw text files available on https://github.com/Esukhia/derge-kangyur</tei:distributor>
        <tei:idno type="TBRC_TEXT_RID">UT4CZ5369-I1KG9{ignum}-0000</tei:idno>
        <tei:idno type="page_equals_image">page_equals_image</tei:idno>
      </tei:publicationStmt>
      <tei:sourceDesc>
        <tei:bibl>
          <tei:idno type="TBRC_RID">W4CZ5369</tei:idno>
          <tei:idno type="SRC_PATH">eKangyur/W4CZ5369/sources/W4CZ5369-I1KG9{ignum}/W4CZ5369-I1KG9{ignum}-0000.txt</tei:idno>
        </tei:bibl>
      </tei:sourceDesc>
    </tei:fileDesc>
  </tei:teiHeader>
  <tei:text>
    <tei:body>
      <tei:div>
        <tei:p n="1" data-orig-n="1a">{title}"""

TEI_END = """</tei:p>
      </tei:div>
    </tei:body>
  </tei:text>
</tei:TEI>
"""

PAREN_RE = re.compile(r"\(([^\),]*),([^\),]*)\)")

def parrepl(match, mode, filelinenum):
    first = match.group(1)
    sec = match.group(2)
    return mode == 'first' and first or sec

def tohrepl(match):
    toh = match.group(1)
    return '<tei:milestone unit="text" toh="'+toh+'"/>'

def parse_one_line(line, filelinenum, state, outf, volnum, options):
    if filelinenum == 1:
        ignum = volnum + 126
        header = TEI_BEGINNING.format(title = line, volnum = volnum, ignum = ignum)
        outf.write(header)
        state['pageseqnum']= 1
        return
    pagelinenum = ''
    endpnumi = line.find(']')
    if endpnumi == -1:
        print("error on line "+str(filelinenum)+" cannot find ]")
        return
    pagelinenum = line[1:endpnumi]
    newpage = False
    linenumstr = ''
    pagestr = pagelinenum
    doti = pagelinenum.find('.')
    if doti != -1:
        pagestr = pagelinenum[:doti]
        linenumstr = pagelinenum[doti+1:]
    if 'pagestr' in state:
        oldpagestr = state['pagestr']
        if oldpagestr != pagestr:
            newpage = True
    if newpage:
        state['pageseqnum']+= 1
    state['pagestr']= pagestr
    text = ''
    if len(line) > endpnumi+1:
        text = line[endpnumi+1:]
        text = text.replace('&', '')
        if '{T' in text:
            closeidx = text.find('}')
            text = re.sub(r"\{T([^}]+)\}", lambda m: tohrepl(m), text)
        if 'keep_errors_indications' not in options or not options['keep_errors_indications']:
            text = text.replace('[', '').replace(']', '')
        if 'fix_errors' not in options or not options['fix_errors']:
            text = re.sub(r"\(([^\),]*),([^\),]*)\)", lambda m: parrepl(m, 'second', filelinenum), text)
        else:
            text = re.sub(r"\(([^\),]*),([^\),]*)\)", lambda m: parrepl(m, 'first', filelinenum), text)
    if newpage:
        outf.write('</tei:p>\n        <tei:p n="'+str(state['pageseqnum'])+'" data-orig-n="'+pagestr+'">')
    if text != '':
        outf.write('<tei:milestone unit="line" n="'+linenumstr+'"/>'+text)

def parse_one_file(infilename, outfilename, volnum, options):
    with open(infilename, 'r', encoding="utf-8") as inf:
        with open(outfilename, 'w', encoding="utf-8") as outf:
            state = {}
            linenum = 1
            for line in inf:
                if linenum == 1:
                    line = line[1:]# remove BOM
                # [:-1]to remove final line break
                parse_one_line(line[:-1], linenum, state, outf, volnum, options)
                linenum += 1
            outf.write(TEI_END)

if __name__ == '__main__':
    """ Example use """
    options = {
        "fix_errors": False,
        "keep_errors_indications": False
    }
    #parse_one_file('../derge-kangyur-tags/102-tagged.txt', '/tmp/test.xml', 1, options)
    volMappingForExport = {100: 101, 101: 102, 102: 100}
    os.makedirs('./output/', exist_ok=True)
    for volnum in range(1, 103):
        volnumstr = '{0:03d}'.format(volnum)
        infilename = '../derge-kangyur-tags/'+volnumstr+'-tagged.txt'
        print("transforming "+infilename)
        if volnum in volMappingForExport:
            print("reordering volume "+str(volnum)+" into "+str(volMappingForExport[volnum]))
            volnum = volMappingForExport[volnum]
        os.makedirs('./output/UT4CZ5369-I1KG9'+str(volnum+126), exist_ok=True)
        parse_one_file(infilename, './output/UT4CZ5369-I1KG9'+str(volnum+126)+'/UT4CZ5369-I1KG9'+str(volnum+126)+'-0000.xml', volnum, options)