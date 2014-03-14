import zipfile, glob, os, datetime

usage = """
    Search PAIR doc list file infn in form as produced by listPAIRdocs.py for all
    instances where documents matching any of the doctypes in doctypelist
    appear at least minhits times within a time window of timewindow days.
    Write output to outfn. Doctypes are the PTO codes as listed in
    http://www.uspto.gov/ebc/portal/ifw-tab-doccodes.html.

"""
infn = 'PAIRdoclist.txt'  #include paths
outfn = 'rslts1.txt'
doctypelist = ['CTAV','SADV','SAFR','A.NE','ANE.I']
minhits = 3
timewindow = 180

class AppDocs:
    def __init__(self, appno, doclist):
        self.appno = appno
        self.docs = []
        for ln in doclist:
            flds = ln.rstrip().split('\t')
            doc = (flds[0], datetime.datetime.strptime(flds[1],'%Y-%m-%d').date(), flds[2])
            self.docs += [doc]

    def matchPairs(self, a, b, maxsep=100000): #a and b are doc codes (third field of PAIRdoclist.txt,
                                #search doclist for instances where a and b are present, b occurs
                                #on the same date or after a, and if maxsep is given, not more than
                                #maxsep days after a
                                #return val is is a tuple of doc pairs satisfying the criteria
                                #each doc is (appno, date object, doctype code)
        pairs = []
        allb = [x for x in self.docs if x[2] == b]    
        for doc in self.docs:
            if doc[2] != a: continue
            pairs += [(doc, d2) for d2 in allb if d2[1] > doc[1] and (d2[1] - doc[1]).days < maxsep]
        return pairs    
    
    def multDocs(self, alist, minhits=1, maxsep=100000):   # alist is a list of doc codes. If app contains multiple instances of any of the doc codes
                                            # within maxsep (days) timespan, return the app no and the no of instances. Else return None.
        alla = [x for x in self.docs if x[2] in alist]
        maxinsts = 0
        basedate = None
        for i in range(len(alla)):
            maxtemp = 0
            for j in range(i + 1, len(alla)):
                if (alla[j][1] - alla[i][1]).days <= maxsep:
                    maxtemp += 1
            if maxtemp > maxinsts:
                maxinsts = maxtemp
                basedate = alla[i][1]
        if maxinsts >= minhits:
            return (self.appno, maxinsts, basedate)
        else:
            return None
            


def docToString(d):
    return d[0] + '\t' + d[1].isoformat() + '\t' + d[2]
  
if os.path.exists(outfn): os.remove(outfn)
outf = open(outfn, 'a')

alldocs = []
allapps = []
appno = ""
for ln in open(infn, 'r'):
    if ln[0:8] != appno:  #first line of new set of docs
        if appno != "":
            allapps += [AppDocs(appno, alldocs)]
        alldocs = [ln]
        appno = ln[0:8]
    else:
        alldocs += [ln]
allrslts = [app.multDocs(doctypelist, minhits, timewindow) for app in allapps]
hitrslts = [rslt for rslt in allrslts if rslt != None]
    
for h in hitrslts:
    #outf.write(docToString(h[0]) + '\t' + docToString(h[1]) + '\t' + str((h[0][1] - h[1][1]).days) + '\n' )
    outf.write(h[0] + '\t' + str(h[1]) + '\t' +  h[2].isoformat() + '\n' )
outf.close()
print 'done'
