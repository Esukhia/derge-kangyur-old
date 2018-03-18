import re
import os

TEI_BEGINNING = """
<?xml version="1.0" encoding="UTF-8"?>
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
        <tei:p n="1">{title}</tei:p>
"""

TEI_END = """
      </tei:div>
    </tei:body>
  </tei:text>
</tei:TEI>
"""

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

def parse_one_line(line, filelinenum, state, outf, volnum, options):
    if filelinenum == 1:
        ignum = volnum + 126
        header = TEI_BEGINNING.format(title = line, volnum = volnum, ignum = ignum)
        outf.write(header)
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
    text = ''
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
        outf.write('</tei:p>\n        <tei:p n="'+str(pagenum)+pageside+'">')
    if text != '':
        outf.write('<tei:milestone unit="line" n="'+str(linenum)+'"/>'+text)

def parse_one_file(infilename, outfilename, volnum, options):
    with open(infilename, 'r', encoding="utf-16le") as inf:
        with open(outfilename, 'w', encoding="utf-8") as outf:
            state = {}
            linenum = 1
            for line in inf:
                # [:-1] to remove final line break
                parse_one_line(line[:-1], linenum, state, outf, volnum, options)
                linenum += 1
            outf.write(TEI_END)

if __name__ == '__main__':
    """ Example use """
    options = {
        "fix_errors": False,
        "keep_errors_indications": False
    }
    for volnum in range(1, 103):
        volnumstr = '{0:03d}'.format(volnum)
        infilename = '../derge-kangyur-tags/'+volnumstr+'-tagged.txt'
        print("transforming "+infilename)
        os.makedirs('./output/', exist_ok=True)
        parse_one_file(infilename, './output/W4CZ5369-I1KG9'+str(volnum+126)+'-0000.xml', volnum, options)