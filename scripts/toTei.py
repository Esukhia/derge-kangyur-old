import re


PAREN_RE = re.compile(r"\(([^\),]*),([^\),]*)\)")

def parrepl(match, mode, filelinenum):
    first = match.group(1)
    sec = match.group(2)
    if (len(first) > 0 and len(sec) > 0 and (
            (first[0] == '་' and sec[0] != '་') or 
            (sec[0] == '་' and first[0] != '་') or
            (first[-1] == '་' and sec[-1] != '་') or
            (sec[-1] == '་' and first[-1] != '་'))):
        print("error on line "+str(filelinenum)+" tsheg not matching in parenthesis")
    return mode == 'first' and first or sec

def parse_one_line(line, filelinenum, state, outf, options):
    if filelinenum == 1:
        outf.write("title: "+line)
        return
    pagelinenum = ''
    endpnumi = line.find(']')
    if endpnumi == -1:
        print("error on line "+str(filelinenum)+" cannot find ]")
        return
    pagelinenum = line[1:endpnumi]
    pagenum = -1
    pageside = -1
    linenum = 0
    doti = pagelinenum.find('.')
    if doti == -1:
        try:
            pagenum = int(pagelinenum[:-1])
        except ValueError:
            print("error on line "+str(filelinenum)+" cannot convert page to integer")
            return
        pageside = pagelinenum[-1]
        if pageside not in ['a', 'b']:
            print("error on line "+str(filelinenum)+" cannot understand page side")
            return
    else:
        pagenumstr = pagelinenum[0:doti-1]
        linenumstr = pagelinenum[doti+1:]
        try: 
            pagenum = int(pagenumstr)
            linenum = int(linenumstr)
        except ValueError:
            print("error on line "+str(filelinenum)+" cannot convert page / line to integer")
            return
        pageside = pagelinenum[doti-1]
        if pageside not in ['a', 'b']:
            print("error on line "+str(filelinenum)+" cannot understand page side")
            return
    newpage = False
    if 'pagenum' in state and 'pageside' in state:
        oldpagenum = state['pagenum']
        oldpageside = state['pageside']
        if oldpagenum != pagenum and oldpagenum != pagenum-1:
            print("error on line "+str(filelinenum)+" leap in page numbers from "+str(oldpagenum)+" to "+str(pagenum))
        if oldpagenum == pagenum and oldpageside == 'b' and pageside == 'a':
            print("error on line "+str(filelinenum)+" going backward in page sides")
        if oldpagenum == pagenum-1 and (pageside == 'b' or oldpageside == 'a'):
            print("error on line "+str(filelinenum)+" leap in page sides")
        if oldpagenum != pagenum or oldpageside != pageside:
            newpage = True
    state['pagenum'] = pagenum
    state['pageside'] = pageside
    if 'linenum' in state and linenum != 0:
        oldlinenum = state['linenum']
        if oldlinenum != linenum and oldlinenum != linenum-1:
            print("error on line "+str(filelinenum)+" leap in line numbers from "+str(oldlinenum)+" to "+str(linenum))
    state['linenum'] = linenum
    if len(line) > endpnumi+1:
        text = line[endpnumi+1:]
        if 'keep_errors_indications' not in options or not options['keep_errors_indications']:
            text = text.replace('[', '').replace(']', '')
        if 'fix_errors' not in options or not options['fix_errors']:
            text = re.sub(r"\(([^\),]*),([^\),]*)\)", lambda m: parrepl(m, 'second', filelinenum), text)
        else:
            text = re.sub(r"\(([^\),]*),([^\),]*)\)", lambda m: parrepl(m, 'second', filelinenum), text)
        if text.find('(') != -1 or text.find(')') != -1:
            print("error on line "+str(filelinenum)+", spurious parenthesis")
    if newpage:
        outf.write('</tei:p><tei:p n="'+str(pagenum)+pageside+'">')
    outf.write('<tei:milestone unit="line" n="'+str(linenum)+'"/>'+text)

def parse_one_file(infilename, outfilename, options):
    with open(infilename, 'r', encoding="utf-16le") as inf:
        with open(outfilename, 'w', encoding="utf-8") as outf:
            state = {}
            linenum = 1
            for line in inf:
                parse_one_line(line, linenum, state, outf, options)
                linenum += 1

if __name__ == '__main__':
    """ Example use """
    options = {
        "fix_errors": False,
        "keep_errors_indications": False
    }
    for i in range(1, 102):
        num = '{0:03d}'.format(i)
        infilename = '../derge-kangyur-tags/'+num+' FINAL tags.txt'
        print("transforming "+infilename)
        parse_one_file(infilename, './output/'+num+'.xml', options)
    # text = "ན་ཏན་(བརྫོད་‚བརྗོད་)པར་མཛད་པར་བཞེད"
    # print(re.sub(r"\(([^\),]*),([^\),]*)\)", r"\2", text))