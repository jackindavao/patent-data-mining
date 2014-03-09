import sys, os, glob, time, re, datetime
#   This sets up a class heirarchy for parsing USPTO full text patent and app xml
#   and outputting to flat text file, one field per line.
#   Author: Jack S. Emery, www.jacksemerypa.com
def hastag(s, tag):  #return whether tag is present in s, followed by space or > but not -
    if s.find('<' + tag + ' ') >= 0:
        return True
    if s.find('<' + tag + '>') >= 0:
        return True
    return False

def makeRX(tag):   #use with findall(txt), txt must be string not list
    tgrx = re.compile('<' + tag + '.+?</' + tag + '>', re.S)
    return tgrx

def makeRXCapture(tag):  #use with .search(txt).group(1), gets only first match
    tgrx = re.compile('<' + tag + '.*?>(.+?)</' + tag, re.S)
    return tgrx
    
def getCapture(rx, txt):   #rx is compiled regex with one capture paren set, txt is srchtext string not list
    m = rx.search(txt)
    if m:
        return m.group(1)
    else:
        return ''

def getCaptures(rx, txt):
    h = rx.findall(txt)
    return '|'.join(h)
    
def extractIPC(txt):
    cs = rx_ipcx.findall(txt)
    r = []
    for c in cs:
        r += [rx_zapdd.sub('-', rx_zapns.sub('', rx_zaptag.sub('-', c)))[1:-1]]
    return '|'.join(r)

def countRXHits(rx, txt):
    h = rx.findall(txt)
    return len(h)
    
def diffdates(dp, ds):   #dp is string in form yyyymmdd, ds is list of strings, return diff betw dp and earliest date in ds
    if len(ds) == 0: return str(0)
    if len(dp) != 8: return str(-1)
    try:
        dtp = datetime.date(int(dp[0:4]),int(dp[4:6]),int(dp[6:8]))
        dmax = 0
        for x in ds:
            d0 = x.split(':')[2]
            if not len(d0) == 8: return str(-1)
            d = datetime.date(int(d0[0:4]),int(d0[4:6]),int(d0[6:8]))
            df = dtp - d
            if df.days > dmax:
                dmax = df.days
        return str(dmax)
    except Exception, ex:
        return str(0)

def extractNames(ns):
    nlist = []
    for n in ns:
        org = getCapture(rx_orgname, n)
        if len(org) > 0:
            nlist += [org]
        else:
            nnp = getCapture(rx_lastname, n) + ' ' + getCapture(rx_firstname, n)
            nlist += [nnp]
    return '|'.join(nlist).upper()

class AllFiles:
    def __init__(self, indir, sscope, startdate=None, utilonlyQ=False, singlefileQ=False):   #sscope: 'pat', 'app', or 'both', to search indicated db's
        self.utilonlyQ = utilonlyQ
        self.startdate = int(startdate)
        self.nfilesread = 0       #total files processed
        self.nlns = 0         #total lines read
        self.ndocs = 0        #total no of patents or apps processed
        if singlefileQ:
            self.infns = [indir]
            if sscope == 'app':
                infappQ = True
        else:
            indirs = []
            if sscope == 'pat' or sscope == 'both':
                indirs += glob.glob(indir + 'pat/*')
            if sscope == 'app' or sscope == 'both':
                indirs += glob.glob(indir + 'app/*')
            self.infns = []
            for d in indirs:
                self.infns += glob.glob(d + '/*.xml')
            self.infns = sorted(self.infns, reverse=True)
            
        if self.startdate:
            self.infns = [x for x in self.infns if int(x.rstrip()[-10:-4]) >= self.startdate]
        self.inf = None
        self.infnidx = -1
        self.infappQ = None  # T => app, F=> grant
        self.ln = ''   
        self.lns = []

    def next_inf(self):
        if self.inf: self.inf.close()
        self.infnidx += 1
        if self.infnidx >= len(self.infns): raise StopIteration
        nextf = self.infns[self.infnidx]
        if nextf.find(r'app') >= 0:
            self.infappQ = True
        else:
            self.infappQ = False
        self.inf = open(nextf, 'r')
        while True:  #read to first opening tag
            self.ln = self.inf.readline()
            if self.infappQ:
                if self.ln.find('<us-patent-application ') >= 0: break
            else:
                if self.ln.find('<us-patent-grant ') >= 0: break
        self.nfilesread += 1
        return True

    def next(self):
        if self.utilonlyQ:
            while True:
                self.nextdoc()
                for ln in self.lns:
                    if ln.find(r'<application-reference appl-type') >= 0:
                        if ln.find('utility') >= 0:
                            return Document(self.lns, self.infappQ)
                        else:
                            break
        else:
            self.nextdoc()
            return Document(self.lns, self.infappQ)
            
            
    def nextdoc(self):
        self.lns = []
        if self.ln == '':
            self.next_inf()
        if self.infappQ:
            while True:
                self.lns += [self.ln]
                self.ln = self.inf.readline()
                if self.ln == '':
                    self.ndocs += 1
                    return
                self.nlns += 1
                if self.ln.find('<us-patent-application ') >= 0:
                    self.ndocs += 1
                    return
        else:
            while True:
                self.lns += [self.ln]
                self.ln = self.inf.readline()
                if self.ln == '':
                    self.ndocs += 1
                    return
                self.nlns += 1
                if self.ln.find('<us-patent-grant ') >= 0:
                    self.ndocs += 1
                    return


rx_bib = re.compile('<us-bibliographic-data-.+?</us-bibliographic-data-', re.S)
rx_drg = makeRX('drawings')
rx_abs = makeRX('abstract')
rx_dsc = makeRX('description')
rx_cls = makeRX('claims')

class DocParts:
    def __init__(self, lns, appQ):     
        self.lns = lns
        self.appQ = appQ
        self.bib = []
        self.abs = []
        self.drg = []
        self.dsc = []
        self.cls = []
        z = 0    #state: 0: nothing 1= in bib; 2= in abs; 3= in drgs; 4= in desc; 5= in claims
        for ln in lns:
            if ln.find('US08474070')>=0:
                pass
            if z == 0:
                if ln.find('<us-bibliographic-data-') >= 0:
                    z = 1
                    self.bib += [ln]
            elif z == 1:
                self.bib += [ln]
                if ln.find('</us-bibliographic-data-') >= 0:
                    z = 2
            elif z == 2:        
                if ln.find('<abstract ') >= 0:
                    z = 3
                    self.abs += [ln]
            elif z == 3:
                self.abs += [ln]
                if ln.find('</abstract>') >= 0:
                    z = 4
            elif z == 4:
                if ln.find('<drawings ') >= 0:
                    z = 5
                    self.drg += [ln]
            elif z == 5:
                self.drg += [ln]
                if ln.find('</drawings>') >= 0:
                    z = 6
            elif z == 6:
                if ln.find('<description ') >= 0:
                    z = 7
                    self.dsc += [ln]
            elif z == 7:
                self.dsc += [ln]
                if ln.find('</description>') >= 0:
                    z = 8
            elif z == 8:
                if ln.find('<claims ') >= 0:
                    z = 9
                    self.cls += [ln]
            elif z == 9:
                self.cls += [ln]
                if ln.find('</claims>') >= 0:
                    break
                
        if len(self.bib) == 0 or len(self.drg) == 0 or len(self.abs) == 0 or len(self.dsc) == 0 or len(self.cls) == 0:
            #means one section at least missing, which breaks the above, so do it the hard way
            dptxt = '@^@^@'.join(self.lns)
            self.bib = getCaptures(rx_bib, dptxt).split('@^@^@')
            self.drg = getCaptures(rx_drg, dptxt).split('@^@^@')
            self.abs = getCaptures(rx_abs, dptxt).split('@^@^@')
            self.dsc = getCaptures(rx_dsc, dptxt).split('@^@^@')
            self.cls = getCaptures(rx_cls, dptxt).split('@^@^@')
                    
                    



    
    

rx_pubref = makeRX('publication-reference')
rx_docno = makeRXCapture('doc-number')
rx_date = makeRXCapture('date')
rx_appref = makeRX('application-reference')
rx_apptype = re.compile(r'appl-type\s*=\s*"(.+?)"')
rx_ipc = makeRX('classifications-ipcr')
rx_ipcx = re.compile('<classification-level>.+?<action-date>', re.S)
rx_usc = makeRX('classification-national')
rx_uscx = re.compile('classification>([^<>]+?)</')
rx_title = makeRXCapture('invention-title') 
rx_usrefs = makeRX('us-references-cited') 
rx_ncls = makeRXCapture('number-of-claims') 
rx_usfldclass = makeRX('us-field-of-classification-search')
rx_usflds = re.compile('<main-classification>(.+?)</main-classification>', re.S)
rx_nfigs = makeRXCapture('number-of-figures') 
rx_reldocs = makeRXCapture('us-related-documents')
rx_child = makeRXCapture('child-doc')
rx_parent = makeRXCapture('parent-doc')
rx_pct = makeRXCapture('<pct-or-regional-filing-data')
rx_usparties = makeRX('us-parties')
rx_assgn = makeRX('assignee')
rx_exmrs = makeRX('examiners')
rx_prexamr = makeRX('primary-examiner')
rx_asexamr = makeRX('assistant-examiner')
rx_zaptag = re.compile('<.+?>')
rx_zapns = re.compile('\n')
rx_zapdd = re.compile('--')
rx_zapss = re.compile('  +') #two or more spaces
rx_refcount = re.compile('</us-citation>')
rx_appcite = re.compile('cited by applicant')
rx_exrcite = re.compile('cited by examiner')
rx_prov = makeRX('us-provisional-application')
rx_inv = makeRX('inventor')
rx_usapplicant = makeRX('us-applicant')
rx_applicant = makeRX('applicant')
rx_firstname = makeRXCapture('first-name')
rx_lastname = makeRXCapture('last-name')
rx_agent = makeRX('agent')
rx_orgname = makeRXCapture('orgname')




class Biblio:
    def __init__(self, lns, appQ):     
        bibtxt = ''.join(lns)
        bibtxt = rx_amps.sub(df, bibtxt)
        self.appQ = appQ
        self.title = getCapture(rx_title, bibtxt)
        self.ncls = getCapture(rx_ncls, bibtxt)  
        self.nfigs = getCapture(rx_nfigs, bibtxt)
        pubref = ''.join(rx_pubref.findall(bibtxt))
        if not appQ:
            self.patno = getCapture(rx_docno, pubref)
            self.issuedate = getCapture(rx_date, pubref)
            self.pubno = ''
            self.pubdate = ''
        else:
            self.pubno = getCapture(rx_docno, pubref)
            self.pubdate = getCapture(rx_date, pubref)
            self.patno = ''
            self.issuedate = ''

        appref = ''.join(rx_appref.findall(bibtxt))
        self.appno = getCapture(rx_docno, appref)
        self.appdate = getCapture(rx_date, appref)
        if not appQ:
            self.ageapp = diffdates(self.issuedate, ['x:x:' + self.appdate])
            self.agepub = ''
        else:
            self.agepub = diffdates(self.pubdate, ['x:x:' + self.appdate])
            self.ageapp = ''
        self.apptype = getCapture(rx_apptype, appref)
        ipcraw = ''.join(rx_ipc.findall(bibtxt))
        self.ipc = extractIPC(ipcraw)
        uscraw = ''.join(rx_usc.findall(bibtxt))
        self.usc = getCaptures(rx_uscx, uscraw)
        self.usc = rx_zapns.sub('', self.usc)
        usrefs = ''.join(rx_usrefs.findall(bibtxt))
        self.nusrefs = str(countRXHits(rx_refcount, usrefs))
        self.nusrefapp = str(countRXHits(rx_appcite, usrefs))
        self.nusrefexr = str(countRXHits(rx_exrcite, usrefs))
        usfldclass = ''.join(rx_usfldclass.findall(bibtxt))
        self.usfldsrch = getCaptures(rx_usflds, usfldclass)
        self.rldx = ''
        self.nrld = ''
        self.npct = ''
        self.nprv = ''
        (self.rldx, self.nrld, self.npct, self.nprv) = self.getRelDocs(bibtxt)
        if not appQ:
            self.ageall = diffdates(self.issuedate, self.rldx.split('|') + ['x:x:' + self.appdate])
        else:
            self.ageall = ''
        usparties = ''.join(rx_usparties.findall(bibtxt))
        if usparties == '':
            invs = rx_applicant.findall(bibtxt)
            self.inventors = extractNames(invs)
            agts = rx_agent.findall(bibtxt)
            self.agent = extractNames(agts)
            self.applicant = ''
        else:
            appls = rx_usapplicant.findall(usparties)
            self.applicant = extractNames(appls)
            invs = rx_inv.findall(usparties)
            self.inventors = extractNames(invs)
            agts = rx_agent.findall(usparties)
            self.agent = extractNames(agts)
        assgns = rx_assgn.findall(bibtxt)
        self.assignee = extractNames(assgns)
        exmrs = ''.join(rx_exmrs.findall(bibtxt))
        prexamr = rx_prexamr.findall(exmrs)
        asexamr = rx_asexamr.findall(exmrs)
        self.examiner = extractNames(prexamr + asexamr)
        pass

    def getRelDocs(self, bibtxt):
        reldoctxt = ''.join(rx_reldocs.findall(bibtxt))
        pcttxt = getCapture(rx_pct, bibtxt)
        i = 0
        tc = 0
        bq = False
        chns = []  #child nodes
        idx1 = 0
        ft = False
        tg = ''
        for c in reldoctxt:
            if c == '<':
                bq = True
            elif c == ' ' or c == '>':
                if ft:
                    tg = reldoctxt[idx1 + 1: i]
                    ft = False
            else:
                if bq == True:
                    if c == '/':
                        tc -= 1
                        if tc == 0:
                            chn = reldoctxt[idx1:i - 1]
                            chns += [(chn, tg)]
                    else:
                        if tc == 0:
                            ft = True
                            idx1 = i - 1
                        tc += 1
                bq = False
            i += 1        
        chntxts = []
        npct = 0
        nprv = 0
        nrld = len(chns)
        for chn in chns:
            (txt, nt) = chn
            if nt.startswith('continuation-in-part'):
                nts = 'CIP:'
            elif nt.startswith('division'):
                nts = 'DIV:'
            elif nt.startswith('continuation'):
                nts = 'CON:'
            elif nt.startswith('us-provisional'):
                nts = 'PRV:'
                nprv += 1
            elif nt.find('reissue') >= 0:
                nts = 'REI:'
            else:
                nts = 'XXX:'
            parent = getCapture(rx_parent, txt)
            pno = ''
            pdt = ''
            cno = ''
            if parent:
                pno = getCapture(rx_docno, parent)
                pdt = getCapture(rx_date, parent)
                if pno.find('PCT') >= 0:
                    npct += 1
            else:  #must be other category that doesn't have parent/child
                pno = getCapture(rx_docno, txt)
                pdt = getCapture(rx_date, txt)
            child = getCapture(rx_child, txt)
            if pno.startswith('61'):
                if not nts == 'PRV:':
                    nts = 'PRV:'
                    nprv += 1
            if child:
                cno = getCapture(rx_docno, child)
                chntxt = nts + pno + ':' + pdt + ':' + cno
            else:
                chntxt = nts + pno + ':' + pdt
            chntxts += [chntxt]
        if pcttxt:
            pno = getCapture(rx_docno, txt)
            pdt = getCapture(rx_date, txt)
            chntxt = 'PCTX:' + pno + ':' + pdt
            chntxts += [chntxt]
            nrld += 1
        return ('|'.join(chntxts), str(nrld), str(npct), str(nprv))


amps = {'&#xa1;' : '!', '&#xa2;' : 'c', '&#xa3;' : 'LL', '&#xa5;' : 'Y', '&#xa6;' : '|', '&#xa7;' : 'Sec. ', \
        '&#xa9;' : '(c)', '&#xaa;' : 'a', '&#xab;' : '<<', '&#xac;' : '^', '&#xad;' : '-', '&#xae;' : '(R)', \
        '&#xaf;' : '_', '&#xb0;' : 'deg.', '&#xb1;' : '+-', '&#xb2;' : '^2', '&#xb3;' : '^3', '&#xb5;' : 'u', \
        '&#xb6;' : 'Para.', '&#xb7;' : '.', '&#xb9;' : '^1', '&#xbb;' : '>>', '&#xbc;' : '1/4', \
        '&#xbd;' : '1/2', '&#xbe;' : '3/4', '&#xbf;' : '?', '&#xc0;' : 'A', '&#xc1;' : 'A', '&#xc2;' : 'A', \
        '&#xc3;' : 'A', '&#xc4;' : 'A', '&#xc5;' : 'A', '&#xc6;' : 'AE', '&#xc7;' : 'C', '&#xc8;' : 'E', \
        '&#xc9;' : 'E', '&#xca;' : 'E', '&#xcb;' : 'E', '&#xcc;' : 'I', '&#xcd;' : 'I', '&#xce;' : 'I', \
        '&#xcf;' : 'I', '&#xd0;' : 'D', '&#xd1;' : 'N', '&#xd2;' : 'O', '&#xd3;' : 'O', '&#xd4;' : 'O', \
        '&#xd5;' : 'O', '&#xd6;' : 'O', '&#xd7;' : ' x ', '&#xd8;' : 'O', '&#xd9;' : 'U', '&#xda;' : 'U', \
        '&#xdb;' : 'U', '&#xdc;' : 'U', '&#xdd;' : 'Y', '&#xe0;' : 'a', '&#xe1;' : 'a', '&#xe2;' : 'a', \
        '&#xe3;' : 'a', '&#xe4;' : 'a', '&#xe5;' : 'a', '&#xe6;' : 'ae', '&#xe7;' : 'c', '&#xe8;' : 'e', \
        '&#xe9;' : 'e', '&#xea;' : 'e', '&#xeb;' : 'e', '&#xec;' : 'i', '&#xed;' : 'i', '&#xee;' : 'i', \
        '&#xef;' : 'i', '&#xf0;' : 'd', '&#xf1;' : 'n', '&#xf2;' : 'o', '&#xf3;' : 'o', '&#xf4;' : 'o', \
        '&#xf5;' : 'o', '&#xf6;' : 'o', '&#xf7;' : ' / ', '&#xf9;' : 'u', '&#xfa;' : 'u', '&#xfb;' : 'u', \
        '&#xfc;' : 'u', '&#xfd;' : 'y', '&#xff;' : 'y', '&#x27;' : "'", '&#x22;' : '"', '&#x3e;' : '>', \
        '&#x3c;' : '<', '&#x26;' : '&', '&#x201c;' : '"', '&#x201d;' : '"', '&#x2033;' : '"', \
        '&#x2036;' : '"', '&#x2032;' : "'"}

def df(m):
    a = m.group(0)
    if amps.has_key(a):
        return amps[a]
    else:
        return ':u' + a[2:]

rx_amps = re.compile(r'&.+?;')   #use: rx_amps.sub(df, ''.join(txt_to_unescape))
rx_tables = re.compile('<tables.+?</tables>', re.S)
rx_maths = re.compile('<maths.+?</maths>', re.S)
rx_comment = re.compile(r'<\?.+?\?>', re.S)
rx_blankline = re.compile(r'^\s*$')
rx_heading = makeRXCapture('heading')
rx_newline = re.compile(r'[\n\r]+')

class Descr:
    def __init__(self, lns, appQ):
        dtxt = ''.join(lns)
        self.appQ = appQ
        dtxt = rx_tables.sub('[TABLE]', dtxt)
        dtxt = rx_maths.sub('[MATH]', dtxt)
        dtxt = rx_comment.sub('', dtxt)
        dtxt = dtxt.replace('<heading ', 'X@X@X<heading')
        secs = dtxt.split('X@X@X')
        secs0 = rx_zaptag.sub('', secs[0]).strip()
        if len(secs0) == 0:
            secs = secs[1:]  #get rid of first sec if no content
        self.sections = ['']   #to make it 1-indexed
        self.headings = ['Not found']
        self.dsclen = 0
        i = 0
        #self.summary = 0
        #self.background = 0
        #self.drawingdesc = 0
        #self.detaileddesc = 0
        self.summarylen = 0
        self.backgroundlen = 0
        self.drawingdesclen = 0
        self.detaileddesclen = 0

        zstate = 0
        for sec in secs:
            i += 1
            sec = rx_amps.sub(df, sec).strip()
            lns = sec.split('\n')
            seclns = []
            for ln in lns:
                
                if ln.startswith('<headingid'):
                    hdg = getCapture(rx_heading, ln)
                    hdg = hdg.upper()    
                    self.headings += [hdg]    
                    if hdg.find('SUMMARY') >= 0:
                        self.summary = i
                        seclns += ['DHSM:: ' + hdg]
                        zstate = 1
                    elif hdg.find('BACKGROUND') >= 0:
                        self.background = i
                        seclns += ['DHBK:: ' + hdg]
                        zstate = 2
                    elif hdg.find('DRAWING') >= 0:
                        self.drawingdesc = i
                        seclns += ['DHDR:: ' + hdg]                        
                        zstate = 3
                    elif hdg.find('DETAILED') >= 0:
                        self.detaileddesc = i
                        seclns += ['DHDD:: ' + hdg]                        
                        zstate = 4
                    else: #zstate unchanged, probably a subheading
                        if zstate == 1:
                            seclns += ['DHSM:: ' + hdg]  
                        elif zstate == 2:
                            seclns += ['DHBK:: ' + hdg]
                        elif zstate == 3:
                            seclns += ['DHDR:: ' + hdg]
                        elif zstate == 4:
                            seclns += ['DHDD:: ' + hdg]
                        else:
                            seclns += ['DHXX:: ' + hdg]                            
                    if zstate == 1:
                        self.summarylen += len(sec)
                    elif zstate == 2:
                        self.backgroundlen += len(sec)
                    elif zstate == 3:
                        self.drawingdesclen += len(sec)
                    elif zstate == 4:
                        self.detaileddesclen += len(sec)
                    continue
                #so then is not heading:
                ln = rx_zaptag.sub('', ln).strip()
                if ln == '': continue
                if zstate == 1:
                    seclns += ['DDSM:: ' + ln]
                elif zstate == 2:
                    seclns += ['DDBK:: ' + ln]
                elif zstate == 3:
                    seclns += ['DDDR:: ' + ln]
                elif zstate == 4:
                    seclns += ['DDDD:: ' + ln]
                else:
                    seclns += ['DDXX:: ' + ln]
            rsec = '\n'.join(seclns) + '\n'
            rsec = rx_zapss.sub(' ', rsec)
            self.dsclen += len(rsec)
            self.sections += [rsec]
        self.backgroundlen = str(self.backgroundlen / 6)
        self.detaileddesclen = str(self.detaileddesclen / 6)
        self.drawingdesclen = str(self.drawingdesclen / 6)
        self.dsclen = str(self.dsclen / 6)
        self.summarylen = str(self.summarylen / 6)
    
    def getSummary(self):
        s = [x for x in self.sections if x[0:6] == 'DHSM::']
        return ''.join(s)
                
    def alltxt(self):
        rtxt = ''.join(self.sections)
        return rtxt
    
rx_claims = re.compile('<claim .+?>(.+?)</claim>', re.S)

class Claims:
    def __init__(self, lns, appQ):
        ctxt = ''.join(lns)
        ctxt = rx_amps.sub(df, ctxt)
        self.appQ = appQ
        clms = rx_claims.findall(ctxt)
        self.claims = []
        nc = 0
        self.claim1len = 0
        self.maxclilen = 0
        self.maxcldlen = 0
        self.ncli = 0
        self.ncld = 0
        for clm in clms:
            nc += 1
            clm = rx_newline.sub(' ', clm)
            if nc == 1:
                ctype = 'CLI :: '
                self.ncli += 1
            elif clm.find('<claim-ref ') >= 0:
                ctype = 'CLD :: '
                self.ncld += 1
            else:
                ctype = 'CLI :: '
                self.ncli += 1
            clm = rx_zaptag.sub('', clm)
            clm = rx_zapss.sub(' ', clm)
            self.claims += [ctype + clm.strip()]
        nc = 0
        for clm in self.claims:
            nc += 1
            if nc == 1:
                self.claim1len = len(clm) - 6
                self.maxclilen = len(clm)
            elif clm.startswith('CLI::'):
                if len(clm) > self.maxclilen:
                    self.maxclilen = len(clm)
            else:
                if len(clm) > self.maxcldlen:
                    self.maxcldlen = len(clm)
        self.nclaims = str(len(self.claims))
        self.claim1len = str(self.claim1len / 6)
        self.maxclilen = str(self.maxclilen / 6)
        self.maxcldlen = str(self.maxcldlen / 6)
        self.ncli = str(self.ncli)
        self.ncld = str(self.ncld)
 
    def alltxt(self):
        rtxt = '\n'.join(self.claims) + '\n'
        return rtxt
 
class Document:
    def __init__(self, d, appQ):
        self.dp = DocParts(d, appQ)
        self.appQ = appQ
        self.bib = Biblio(self.dp.bib, appQ)
        self.dsc = Descr(self.dp.dsc, appQ)
        self.cls = Claims(self.dp.cls, appQ)
        ab = ''.join(self.dp.abs)
        ab = rx_amps.sub(df, ab)
        ab = rx_zaptag.sub('', ab)
        self.abs = rx_zapns.sub(' ', ab).strip() + '\n'

    def doctostring(self):
        lns = []
        lns += ['TITL:: ' + self.bib.title]
        if self.appQ:
            lns += ['DTYP:: app']
        else: 
            lns += ['DTYP:: pat']
        lns += ['ATYP:: ' + self.bib.apptype]
        lns += ['PTNO:: ' + self.bib.patno]
        lns += ['ISDT:: ' + self.bib.issuedate]
        lns += ['APNO:: ' + self.bib.appno]
        lns += ['APDT:: ' + self.bib.appdate]
        lns += ['PBNO:: ' + self.bib.pubno]
        lns += ['PBDT:: ' + self.bib.pubdate]
        
        lns += ['AGAP:: ' + self.bib.ageapp]
        lns += ['AGPB:: ' + self.bib.agepub]
        lns += ['AGAL:: ' + self.bib.ageall]
        
        
        lns += ['INVS:: ' + self.bib.inventors]
        lns += ['APLS:: ' + self.bib.applicant]
        lns += ['LREP:: ' + self.bib.agent]
        lns += ['ASSE:: ' + self.bib.assignee]
        lns += ['EXMR:: ' + self.bib.examiner]    
        
        lns += ['NCLS:: ' + self.cls.nclaims]
        lns += ['NCLI:: ' + self.cls.ncli]
        lns += ['NCLD:: ' + self.cls.ncld]
        lns += ['NFIG:: ' + self.bib.nfigs]
        lns += ['DSCL:: ' + self.dsc.dsclen]
        lns += ['SUML:: ' + self.dsc.summarylen]
        lns += ['BKGL:: ' + self.dsc.backgroundlen]
        lns += ['DDRL:: ' + self.dsc.drawingdesclen]
        lns += ['DDSL:: ' + self.dsc.detaileddesclen]
        
        lns += ['CLFL:: ' + self.cls.claim1len]
        lns += ['CLIL:: ' + self.cls.maxclilen]
        lns += ['CLDL:: ' + self.cls.maxcldlen]
        lns += ['NREF:: ' + self.bib.nusrefs]
        lns += ['NRFA:: ' + self.bib.nusrefapp]
        lns += ['NRFX:: ' + self.bib.nusrefexr]
    
        lns += ['IPCC:: ' + self.bib.ipc]
        lns += ['USCC:: ' + self.bib.usc]
        lns += ['SFLD:: ' + self.bib.usfldsrch]    
        
        lns += ['RLDX:: ' + self.bib.rldx]
        lns += ['NRLD:: ' + self.bib.nrld]
        lns += ['NPRV:: ' + self.bib.nprv]
        lns += ['NPCT:: ' + self.bib.npct]
        
        lns += ['ABST:: ' + self.abs]
        pdoc = '\n'.join(lns) + self.dsc.alltxt() + self.cls.alltxt() + 'ENDRECORD' + '\n'  #alltxt already has newlines
        return pdoc
     