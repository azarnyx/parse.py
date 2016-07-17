#! /usr/bin/env python

import re
import operator
import glob
import optparse
import sys

class InputError:
    """ Pease use as: parse.py -d path_to_txt_files"""

class ParseMostPublished:
    """Parser of txt files. It takes the name of the folder. Table of
    most-published people in the field is available in self.author_top.
    """
    def __init__(self,records):
        self.key_for_author="AU"
        self.record_dict = self._records2list(records)
        self.author_top = self._sortbyauthors(self.record_dict)

    def _records2list(self, records):
        """Make a list of dictionaries from every record"""
        lrec = []
        for crec in records:
            keys = re.split("([\n^][A-Z][A-Z0-9])", crec)
            keys.pop(0)
            rec = {}
            for (ke, el) in zip( keys[::2], keys[1::2]):
                lkey1 = ke.replace("\n", "")
                lkey2 = lkey1.replace('U - ','')
                lkey= lkey2.replace(' - ','')
                if lkey==self.key_for_author:
                    rec[lkey] = [e.strip() for e in el.split("\n")]
                else:
                    rec[lkey] = el
            lrec.append(rec)
        return lrec
        
    def _sortbyauthors(self, rlist):
        """Returns a list of authors sorted by number of publications"""
        adict = dict()
        for record in rlist:
            # If author of the publication is unknown, which is rare,
            # just do not count it
            try:
                alit = record[self.key_for_author]
            except:
                pass
            for au in alit:
                if au in adict:
                    adict[au]=adict[au]+1
                else:
                    adict[au]=1
        sorted_adict = sorted(adict.iteritems(), key=operator.itemgetter(1))
        return sorted_adict[::-1]

        
def md_out(ranking):
    print "| Place 	| Name 	| # Publications 	|"
    print "| ------: | :---------: | :--------- |"
    for n,(name,num) in enumerate(ranking):
        print "|"+ str(n+1)+". | "+str(name)+" | "+str(num)+"|"
        
    
def main():
    usage = """ The script parse Web-Of-Science data output files.
    Example of usage: 
    
    python parse.py -d data_ml
    
    Changin of output options available with:
    
    python parse.py -d data_ml -n 20
    """

    fmt = optparse.IndentedHelpFormatter(max_help_position=50, width=100)
    parser = optparse.OptionParser(usage=usage, formatter=fmt)
    args = optparse.OptionGroup(parser, 'Parser arguments', '')

    args.add_option('-d', '--directory', metavar='Directory', default=None,
                     help='Path to directory with txt files')

    args.add_option('-n', '--outnumber', type='int', default=20,
                     help='Number of top output names')

    args.add_option('-m', '--markdown', default=0,
                     help='Output in txt or markdown table, if not 0, then output markdown')

    parser.add_option_group(args)
    options, _ = parser.parse_args()

    if options.directory:
        folname = options.directory+"/*"
    else:
        raise InputError(msg)

    if options.outnumber:
        outnumber = options.outnumber
            
    lfiles = glob.glob(folname)
    linefile = ''

    for fi in lfiles:
        li = open(fi, 'r').read()
        linefile+=li+"\n\n"
        li2=li
    records = re.split("\n\n", linefile)
    bib = ParseMostPublished(records)
    
    if options.markdown:
        md_out(bib.author_top[:outnumber])
    else:
        for (Auth, numpap) in bib.author_top[:outnumber]:
            print Auth, numpap

    return 0

if __name__ == "__main__":
    sys.exit(main())
    
