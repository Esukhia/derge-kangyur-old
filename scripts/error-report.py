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

PAREN_RE = re.compile(r"\(([^\),]*),([^\),]*)\)")

def parrepl(match, mode, filelinenum):
    first = match.group(1)
    sec = match.group(2)
    if (len(first) > 0 and len(sec) > 0 and (
            (first[0]== '་' and sec[0]!= '་') or 
            (sec[0]== '་' and first[0]!= '་') or
            (first[-1]== '་' and sec[-1]!= '་') or
            (sec[-1]== '་' and first[-1]!= '་'))):
        printerror("error on line "+str(filelinenum)+" tsheg not matching in parenthesis")
    return mode == 'first' and first or sec

error_regexps = [
        {"reg": re.compile(r"([^ །\(\[,]།[^ །\]\)༽,]|(?:[^ངོེིུ]|ང[^ངོེིུ])་།)"), "msg": "invalid shad sequence"},
        {"reg": re.compile(r"[^ཀ-ྼ][ཱ-྄྆྇ྍ-ྼ]"), "msg": "invalid unicode combination sequence"},
        {"reg": re.compile(r"[^ༀ-࿚#-~ \[\]\{\}\.]"), "msg": "invalid unicode characters (non-Tibetan, non-ascii)"},
        {"reg": re.compile(r"([ྱུྲཿཾ྄ྃྭིྀ་ ])\1"), "msg": "invalid double diactitic sign (shabkyu, gigu, etc.) or tshek"},
        {"reg": re.compile(r"[ༀ-༃༆-༊༎-༟]"), "msg": "suspicious Tibetan character"},
        {"reg": re.compile(r"([ཀགཤ།] །|[^ ཀགཤ།]། |[ཀགཤ།]། |[ཀགཤ།][། ]|[༽ཿ་ \]nl])$"), "msg": "invalid end of line", "type": "punctuation", "neg": True},
        # see https://docs.microsoft.com/en-us/typography/script-development/tibetan#reor
        {"reg": re.compile(r"([ཱ-྇][ྍ-ྼ]|[ི-྄]ཱ|[ྃཾཿ][ཱ-ཽྀ])"), "msg": "invalid character order (vowel before subscript or achung after vowel)", "type": "invalid"},
        {"reg": re.compile(r"(ཪ[ླྙྲྱཱ-྇]|རྻ)"), "msg": "wrong form of rago used (0F62 vs. 0F65)", "type": "invalid"},
        {"reg": re.compile(r"([ཱེཻོཽ])\1"), "msg": "invalid vowel duplication (use 0F7D and 0F7B when relevant)", "type": "invalid"},
    ]
    # opposite of last is sort of ([ཀགཤ།]། |[^ ཀགཤ།]།|[༽ཿ་\]nl] )\n

def check_simple_regexp(line, filelinenum, volnum, options):
    for regex_info in error_regexps:
        if "neg" in regex_info and regex_info["reg"]:
            if not regex_info["reg"].search(line):
                printerror("error on vol "+str(volnum)+" line "+str(filelinenum)+" "+regex_info["msg"])
            continue
        for match in regex_info["reg"].finditer(line):
            printerror("error on vol "+str(volnum)+" line "+str(filelinenum)+" "+regex_info["msg"]+" : ")
            s = match.start()
            e = match.end()
            printerror(line[:s]+"**"+line[s:e]+"**"+line[e:])


def parse_one_line(line, filelinenum, state, volnum, options):
    if filelinenum == 1:
        state['pageseqnum']= 1
        state['pagenum']= 1
        state['pageside']= 'a'
        return
    pagelinenum = ''
    endpnumi = line.find(']')
    if endpnumi == -1:
        printerror("error on line "+str(filelinenum)+" cannot find ]")
        return
    pagelinenum = line[1:endpnumi]
    pagenum = -1
    pageside = -1
    linenum = 0
    isBis = False
    doti = pagelinenum.find('.')
    if doti == -1:
        pageside = pagelinenum[-1]
        if pageside not in ['a', 'b']:
            printerror("error on line "+str(filelinenum)+" cannot understand page side")
            return
        pagenumstr = pagelinenum[:-1]
        if pagelinenum[-2]== 'x':
            isBis = True
            pagenumstr = pagelinenum[:-2]
        try:
            pagenum = int(pagenumstr)
        except ValueError:
            printerror("error on line "+str(filelinenum)+" cannot convert page to integer")
            return
    else:
        linenumstr = pagelinenum[doti+1:]
        pageside = pagelinenum[doti-1]
        if pageside not in ['a', 'b']:
            printerror("error on line "+str(filelinenum)+" cannot understand page side")
            return
        pagenumstr = pagelinenum[0:doti-1]
        if pagelinenum[doti-2]== 'x':
            isBis = True
            pagenumstr = pagelinenum[0:doti-2]
        try: 
            pagenum = int(pagenumstr)
            linenum = int(linenumstr)
        except ValueError:
            printerror("error on line "+str(filelinenum)+" cannot convert page / line to integer")
            return
    newpage = False
    if 'pagenum' in state and 'pageside' in state:
        oldpagenum = state['pagenum']
        oldpageside = state['pageside']
        if oldpagenum != pagenum and oldpagenum != pagenum-1:
            printerror("error on line "+str(filelinenum)+" leap in page numbers from "+str(oldpagenum)+" to "+str(pagenum))
        if oldpagenum == pagenum and oldpageside == 'b' and pageside == 'a':
            printerror("error on line "+str(filelinenum)+" going backward in page sides")
        if oldpagenum == pagenum-1 and (pageside == 'b' or oldpageside == 'a'):
            printerror("error on line "+str(filelinenum)+" leap in page sides")
        if oldpagenum != pagenum or oldpageside != pageside:
            newpage = True
    if newpage:
        state['pageseqnum']+= 1
    state['pagenum']= pagenum
    state['pageside']= pageside
    if 'linenum' in state and linenum != 0:
        oldlinenum = state['linenum']
        if oldlinenum != linenum and oldlinenum != linenum-1:
            printerror("error on line "+str(filelinenum)+" leap in line numbers from "+str(oldlinenum)+" to "+str(linenum))
    state['linenum']= linenum
    check_simple_regexp(line, filelinenum, volnum, options)
    text = ''
    if len(line) > endpnumi+1:
        text = line[endpnumi+1:]
        if '{T' in text:
            if not '}' in text:
                printerror("error on line "+str(filelinenum)+", missing closing }")
            closeidx = text.find('}')
            if not text.startswith('༄༅༅། །', closeidx+1):
                rightcontext = text[closeidx+1:closeidx+5]
                printerror("warning on line "+str(filelinenum)+" possible wrong beginning of text: \""+rightcontext+"\" should be \"༄༅༅། །\"")
            locstr = str(pagenum)+pageside+str(linenum)+" ("+str(volnum)+")"
        if 'keep_errors_indications' not in options or not options['keep_errors_indications']:
            text = text.replace('[', '').replace(']', '')
        if 'fix_errors' not in options or not options['fix_errors']:
            text = re.sub(r"\(([^\),]*),([^\),]*)\)", lambda m: parrepl(m, 'first', filelinenum), text)
        else:
            text = re.sub(r"\(([^\),]*),([^\),]*)\)", lambda m: parrepl(m, 'second', filelinenum), text)
        if text.find('(') != -1 or text.find(')') != -1:
            printerror("error on line "+str(filelinenum)+", spurious parenthesis")

def parse_one_file(infilename, volnum, options):
    with open(infilename, 'r', encoding="utf-8") as inf:
        state = {}
        linenum = 1
        for line in inf:
            if linenum == 1:
                line = line[1:]# remove BOM
            # [:-1]to remove final line break
            parse_one_line(line[:-1], linenum, state, volnum, options)
            linenum += 1

errfile = open("errors.txt","w")

def printerror(err):
    errfile.write(err+"\n")

if __name__ == '__main__':
    """ Example use """
    options = {
        "fix_errors": False,
        "keep_errors_indications": False
    }
    # regexp tests:
    # check_simple_regexps("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། བ།ཀ བཀྲ་ཤིས་བདེ་ལེགས།", 1, 1, options)
    # check_simple_regexps("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། །ྫ བཀྲ་ཤིས་བདེ་ལེགས།", 2, 1, options)
    # check_simple_regexps("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། · བཀྲ་ཤིས་བདེ་ལེགས།", 3, 1, options)
    # check_simple_regexps("༄༅། །འདུལ་བ་ཀ་བཞུགས་སོ། ཀུུ བཀྲ་ཤིས་བདེ་ལེགས།", 4, 1, options)
    for volnum in range(1, 103):
        volnumstr = '{0:03d}'.format(volnum)
        infilename = '../derge-kangyur-tags/'+volnumstr+'-tagged.txt'
        print("checking "+infilename)
        parse_one_file(infilename, volnum, options)

errfile.close()