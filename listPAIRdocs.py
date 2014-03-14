import zipfile, glob, os
usage = """Assumes directory d contains zipped PAIR archives as downloaded from
        Google, see http://www.google.com/googlebooks/uspto-patents-pair.html.
        The filenames of the individual pdf document files are parsed out from the
        zip archive, formatted to a more readable format, and output to file outfn.
        """

d='e:/p/PAIR/'
outfn = 'PAIRdoclist.txt'  #include path if desired
fs = glob.glob(d + '*.zip')
if os.path.exists(outfn): os.remove(outfn)
outf = open(outfn, 'a')
for f in fs:
    z=zipfile.ZipFile(f)
    zl=z.infolist()
    zn=[x.filename for x in zl if x.filename.find('image_file_wrapper') > 0]
    for s in zn:
        sn = os.path.basename(s).strip()
        if sn.lower().endswith('.pdf'):
            flds = sn[:-4].split('-')
            ln = '\t'.join([flds[0], '-'.join(flds[1:4]), flds[5]]) + '\n'
            outf.write(ln)
outf.close()
print 'done'
                
        

    