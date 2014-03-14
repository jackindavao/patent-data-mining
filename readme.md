OVERVIEW
--------

Google has provided a large number of U.S. patent documents in downloadable [archives](http://www.google.com/googlebooks/uspto-patents.html). The tools presented here relate to two datasets in particular:

1. The full text of issued patents, and full text of published patent applications (applications are usually, but not necessarily, published about 18 months after filing). Google provides these as zipped xml files, with each file corresponding to one week of the U.S. Patent Office's output. The size of these files is on the order of 100M zipped, or 500M unzipped.

2. PAIR files for some but not all patent applications. The USPTO's PAIR (Patent Application Information Retrieval) database includes all papers filed during prosecution of an application, all examiner actions, etc. -- the complete USPTO file. For each patent application, Google provides a separate zip archive containing several files with index and metadata, plus a folder containing all of the filed documents, each as a separate pdf.

Presented here are instructions, tools, and resources for building corpora from these datasets and performing data-mining operations.

WHAT IS THIS GOOD FOR?
----------------------

Obviously, a number of patent related search tools already exist. The USPTO provides [search tools](http://www.uspto.gov/patents/process/search/index.jsp) for issued patents and published applications (which are generally pathetic). However, several considerably better free search tools exist, including [Google Patents](https://www.google.com/?tbm=pts), [FreePatentsOnline](http://www.freepatentsonline.com/), and [PatentLens](http://www.lens.org/lens/). These provide functionality adequate for basic patentability-type searching. Commercial search tools can also be found, offering as much sophisticated search functionality as the user is willing to pay for.

So why, then, would anyone take the trouble to build corpora and tools of the kind described here? Here are a few of the motivations (apart from the enjoyment of coding :)

1. A main goal was not patentability searching, it was trying to learn to write better patent applications by observing techniques used by others. I wanted to be able to assemble statistics and examples, and obtain metrics of interesting characteristics. (For an example, see [this post](http://www.jackemery.com/jsepa/content/words-in-patents.php).  

2. As best I am aware, there are no good tools --- certainly no free ones --- available for searching PAIR records. These are very large archives, and pdf is a notoriously difficult format for data mining. Yet these are a rich source of useful examples.

3. Even for patentability searching, the available tools are missing some features that I wanted to have available. The [commercial search tool](https://acclaimip.com/) that I use is very good at zeroing in on a search topic, but it uses what amounts to a software "black box" to rank search hits by relevance. There are times when I don't want the software deciding what is relevant --- I want to be able to do a boolean word search and be absolutely positive that I have found *every* reference that contains that word combination. I'd also like to be able to do regex searching, and I'm not aware of any patent search tool that offers that functionality. And I'd often like not to have to skim through an entire patent to find my search terms, even if they are highlighted -- I'd like to have the option to pull out just the paragraphs or sentences that I searched for. Some of this functionality can be gotten, or at least kludged, from available tools if one is determined enough, but a five-minute python script will drill down on exactly what I want and output the results in exactly the form that I specify.

SYSTEM REQUIREMENTS
-------------------

The programs posted here were written in either Python 2.7 or VB.NET 2010 and tested on a Windows 7 system. 


WHAT THIS REPOSITORY CONTAINS
-----------------------------

In the material to follow, I will describe the usage and functionality of each of the tools and resources provided. The programs have been tested and I have performed various consistency checks. I used them to generate complete corpora for both issued patents and published applications for 2007 through the present (I update them periodically), as well as a large corpus of PAIR data; I use these resources in my patent practice and as best I can determine the programs produced complete and accurate corpora. 

These programs are intended for programmers who are at least familiar with Python, and I have not taken the time to build in the kind of extensive exception handling required to deal with end users. For the most part, details like filenames and directory structure are hard-wired; a programmer will find it easier to change a line of code where necessary than to try to navigate through all the possible options using command line arguments or a GUI. It is critical to maintain a consistent file and directory structure, so best results will be obtained by not renaming data components unless clearly necessary.

Setting up a corpus of full-text patent documents
-------------------------------------------------

The full text corpora comprise two large flat text files each containing an entire dataset (one file for issued patents, named pat.txt, and one for issued applications, named app.txt). In this flat file, each field is represented as a single newline-terminated line. Each line begins with a 6-character identifier in the form XXXX:: followed by a space. This identifier indicates the field. As an example here are a few lines from one record:

```
TITL:: Eyewear with rigid lens support
DTYP:: pat
ATYP:: utility
PTNO:: 08661562
ISDT:: 20140304
APNO:: 13465272
. . . .
INVS:: CALILUNG RYAN|JANAVICIUS JASON
LREP:: KNOBBE MARTENS OLSON & BEAR, LLP
```

Each document is terminated by an ENDRECORD line. A short sample file of a few records (2000 lines) is included as head_pat.txt.

Why do it this way? Why not just use the zipped xml files the way they come from the PTO? Several reasons. With a flat file, it's trivially easy to test search code in a Python console. The PTO's xml is quite complex, and has changed several times. (My parse utility, PyPatUtils.py, handles the different versions back at least through 2007.) There are a number of details in the xml that need massaging, especially those involving special characters and element properties. There are also some additional metrics (word counts, for example) that I wanted to generate during the parse. And finally, my intention eventually is to put this dataset in a relational database, so the flat file is a good intermediate step. 

Using these flat files, it's very simple to write code that will pull out lines or combinations of lines that match pretty much any search criteria imaginable. Searches won't be instantaneous --- my current corpus spans 7+ years, each of the two flat files (pat.txt and app.txt) is on the order of 100G in size, and it typically takes on the order of two hours for a Python script to search either file. (However, the time consuming part of this kind of searching isn't the search, it's reading all the results, so I'm happy to go do something else for a few hours if it means I can greatly reduce the amount of output that I have to read.)

Obtaining the xml files
-----------------------

To obtain the weekly zipped xml files and prepare the input data:

1. Go to [ http://www.google.com/googlebooks/uspto-patents-grants-text.html]( http://www.google.com/googlebooks/uspto-patents-grants-text.html) for issued patents, and/or [http://www.google.com/googlebooks/uspto-patents-applications-text.html](http://www.google.com/googlebooks/uspto-patents-applications-text.html) for published applications. Copy the desired links into a text file. Use [wget](http://gnuwin32.sourceforge.net/packages/wget.htm) to bulk download the files.
2. Unzip the xml files. Do not rename them. On a Windows system this is easiest done by using Explorer to search the folder containing the zip archives for ".xml". This will produce a list of all the xml files; then they can be copied to a destination folder by drag and drop, and they will be unzipped in the process. The directory structure is a directory named gxml, which has two sub-directories named app and pat, each subdirectory has one sub-sub-directory for each year. This can be changed in the code if desired, and it will be necessary to change the code to reflect your own base directory, drive letter, etc.
3. Output is to a single flat file -- for issued patents, named pat.txt, for applications, app.txt.

PyPatUtils.py
-------------

This file implements the functionality for parsing the USPTO's xml. A class heirarchy is created in which each document is broken into its main sections (bibliographic section, description section, claims, and abstract) and each of these section is parsed into a separate class object encompassing the various sub-fields. Once each document is fully parsed, it is output in the desired flat file representation.

The field identifiers used in the flat files are as follows. (Some of these correspond to xml elements in the original file; some are generated during the parse (e.g. lengths and counts of various elements); and in some cases xml elements with multiple short child elements are condensed into a single field with the child values delimited within the field by the | character (classification fields, for example).

List of fields and class heirarchy
All fields are string, including numbers

```
**Document**
appQ   is doc an app (T) or patent (F)
bib      bibliographic section, a Bibio object
dsc    description section, a Descr object
cls     claims section, a Claims object
abs   abstract   (string)

**Biblio fields **
appQ
TITL  title
NCLS  ncls
NFIG  nfigs
PTNO patno       will be '' for apps
ISDT  issuedate  will be '' for apps
PBNO pubno     will be '' for patents
PBDT pubdate   will be '' for patents
APNO  appno
APDT  appdate
AGAP  ageapp   days from appdate to issuedate for patents, '' for apps
AGPB  agepub   days from appdate to pubdate for apps, '' for patents
AGAL  ageall     for patents, time from earliest related app date to issuedate; for apps, ''
ATYP  apptype    (design, utility, reissue, etc)
IPCC  ipc        ipc class
USCC   usc        us class
NREF  nusrefs   total cited refs,   patents only
NRFA  nusrefapp   total refs cited by applicant
NRFX  nusrefexr   total refs cited by examiner
SFLD  usfldsrch       field of search
RLDX related doc nos and dates
NRLD no of related docs
NPCT no of parent PCT's
NPRV  no of parent provisionals
PCTQ  T or F, T if natl phase of PCT
INVS inventors
ASSE  assignee
APLS applicant  (only after 2012)
LREP  agent
EXMR  examiner

**Descr fields**
Do not use codes starting with DD except as per here, so that all description text can be easily parsed out
sections   list of strings, one element per section. These
may have multiple lines. Each line is coded with:
DDSM if part of summary
DDBK if part of background
DDDR  if part of drawing desc
DDDD if part of detailed desc
DDXX otherwise
DHSM, DHBK, DHDR, DHDD, DHXX  headings  (list of strings, aligned with sections)
DSCL  dsclen     description length in chars, int
summary  (summary section)     these should not be used, use line headings as above
background
drawingdesc
SUML  summarylen
BKGL  backgroundlen
DDRL   drawingdesclen
DDSL   detaileddesclen       

**Claims fields**
claims  (list of strings, one per claim, lead with CLI :: or CLD ::)
CLFL  claim1len
CLDL  maxclilen
CLIL  maxcldlen
NCLI  ncli
NCLD  ncld
```

I have posted here the relevant DTD files. Also posted is a file xml_outline.txt that summarizes the main xml elements in outline form. (DTD patent-grant-v44-2013-05-16.txt and 
DTD US Patent Application Publications v43 2012-12-04.dtd.txt). 

ParsePTOXMLtoFlatFile.py
------------------------

This is the driver code that sets up the parse using PyPatUtils.py. The variables pertaining to file hierarchy and settings are described in the file.


Utilities For Handling PAIR Archives
------------------------------------

The US Patent Office maintains an official file for each patent application. The file contains the application papers as well as all of the documents filed by the applicant or produced by the Patent Office during examination. These files become publicly available (in most cases) about 18 months after the application is filed, and in any case once a patent is issued. The Patent Office provides access through its [PAIR] ((http://www.uspto.gov/portal-home.jsp)) (Patent Application Information Retrieval) portal.

These files embody a great deal of useful information about patent examining procedure, since they provide a record of what the Patent Office has done in actual cases. Unfortunately, they are not searchable. They are impracticable to access in bulk on the PTO site; the files are large (typically in the 5 - 30M range), and the site is Capcha protected and does not lend itself readily to spidering or scraping.

However, Google has made available individual zip archives of a large number of PAIR files [here](http://www.google.com/googlebooks/uspto-patents-pair.html). These zip archives are easily downloaded using an URL in the form http://storage.googleapis.com/uspto-pair/applications/APP_NUM.zip, where APP_NUM is replaced with the application number of the file being sought. However, PAIR archives are not available for many application numbers. It is possible to obtain a list of the 5,200,000 available archives using a utility described on the google download page, which can also download archives, but that approach did not entirely fit my needs so I took a different approach.

Posted here is a utility, MakePAIRDownloadList, to facilitate downloading a large corpus of PAIR archives. This is a VB.net 2010 application and operates as follows:

1. It first generates a list of application numbers of issued patents (the application number is not the same as the patent number) by scanning the pat.txt flat file described above in reverse chronological order. Since pat.txt includes only issued patents, this assures that we get PAIR files representing the entire examination process, and not partial archives, and that they are the most recent ones available.
2. It then checks the folder containing the already downloaded archives and removes those from the download list.
3. Next for each application number in the list it makes an HTTP request on the download site to determine whether an archive is available for that number and if so what size it is. This is done because some archives are extremely large -- 100M or more -- usually because they include a large number of foreign references (pdf's of journal articles, etc.), which are not useful for my purposes, so I impose an arbitrary size cutoff.
4. It outputs a list of URLs suitable for wget, for the applications that pass the above filters.

The archives can then be easily downloaded in bulk using [wget](http://gnuwin32.sourceforge.net/packages/wget.htm). Using this method I have downloaded ~10,000 archives.

Also posted is a simple utility, listPAIRdocs.py, to scan through all of the downloaded archives and output a list of the archived documents, showing application number, date, and document type of each. The USPTO categorizes all documents using type codes which are listed [here]( http://www.uspto.gov/ebc/portal/ifw-tab-doccodes.html) and which form part of the filename. The document list can be searched for particular document types or patterns of interest using simple Python scripts or in any other preferred way. I have posted one example of such a script, in this case to find multiple instances of specified document types occuring within a specified time window. See searchPAIRidx.py.

(To merely find single document types, Windows 7's search utility works well, but must be set to search within zip archives. This has the advantage that the found documents can be viewed in the Windows Explorer preview pane.) 

I have not yet figured out any good way to search document content. Unfortunately, all documents are in pdf format and are not searchable without first doing OCR. I have not found a practicable way to do bulk OCR on a few hundred thousand pdf's. If anyone has any good ideas, I would be very happy to hear them. 









