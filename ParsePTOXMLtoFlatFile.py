import sys, os, glob, time, re, datetime
from PyPatUtils import *

usage = """This writes all patents (or apps) to a flat file. It expects the
        following file locations and options settings:
            indir: the folder location of the raw xml files as downloaded from
                google (www.google.com/googlebooks/uspto-patents-grants-text.html
                for patents and www.google.com/googlebooks/uspto-patents-applications-text.html
                for apps. There should be a subfolder named app and one named pat.
                In each of these folders should be a subfolder for each year, with
                the xml files in the subfolder (as downloaded do not rename them,
                however they must be xml files, not zip files)).
            outfn: the file path of the output flat text file
            logfn: the file path of the log file (noting any errors)
            dtype: valid values are 'app' or 'pat' (note that the xml is somewhat
                different for each).
            utilityonlyQ: if True, exclude plant and design patents
            startdate: if None, process all files in indir into new output file.
                WARNING: this will overwrite outfn file, back it up first.
                Otherwise, set to (string) yymmdd, program will parse and append
                data to output file for all xml files equal to or greater than
                that date.
        Author: Jack S. Emery, www.jacksemerypa.com
        """
dtype = 'pat'
startdate = '131210' 
utilityonlyQ = True
indir = 'E:/p/gxml/'
outfn = 'e:/p/db/' + dtype + '.txt'
if startdate == None and os.path.exists(outfn):
    h = raw_input("WARNING: this will delete existing version of " + outfn + " -- continue?")
    if h == None or not (h.startswith("Y") or h.startswith("y")):
        exit(0)
    os.remove(outfn)
else:
    tempoutfn = outfn
    outfn = os.path.join(os.path.dirname(outfn), 'out.txt')
outf = open(outfn, 'a')
logfn = 'e:/p/db/log' + dtype + '.txt'
if os.path.exists(logfn): os.remove(logfn)
logf = open(logfn, 'a')

sst = time.clock()
af = AllFiles(indir, dtype, startdate, utilityonlyQ)  #True => utility patents only
prev = ''
ndocs = 0
print "starting"
while True:
    try:
        d = af.next()
        ndocs += 1
        outf.write(d.doctostring())    
        prev = d.bib.patno
    except StopIteration:
        outf.close()
        print 'done', str(af.ndocs), 'lines'
        break
    except KeyboardInterrupt:
        break
    except Exception, ex:
        nexc =+ 1
        if nexc > 10000: break
        xs = 'exception, af.ndocs: ' + str(af.ndocs) + " " + prev + " " + str(time.clock() - sst) +  ex.message + '\n'
        logf.write(xs)
        print xs
        logf.flush()
    if af.ndocs % 1000 == 0:
        print "ndocs", str(ndocs), "time", str(time.clock() - sst)
    pass
if startdate:  #then we're concatenating
    print "concatenating, concat file will be " + outfn + ", rename if desired"
    with open(outfn, 'a') as outf:
        with open(tempoutfn, 'r') as oldf:
            for line in oldf:
                outf.write(line)
raw_input("ALL DONE, any key to exit")


    

