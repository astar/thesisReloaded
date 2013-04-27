#!/usr/bin/python
""" check fits files for update throught ssa protocol

"""
import pandas as p
import datetime
import dateutil as du
from optparse import OptionParser
import os
import sys
from IPython import embed

def main():

    prg = os.path.basename(sys.argv[0])
    usage = prg + ' [ <OPTIONS> ] <ARGS>'

    #
    # parse command line, result is stored to 'opts'
    #
    parser = OptionParser(usage, version='%s version 0.1' % prg)

    parser.add_option(
        '-s', '--source', action='store', dest='source',
        default='statistics.csv', help='specify input file')

    parser.add_option(
        '-o', '--output', action='store', dest='output',
        default='statistics.html', help='specify output file')

    opts, args = parser.parse_args()

    #
    # Main logic
    #
    file_name = opts.source
    output_file = opts.output
    cols = ['cat', 'star', 'spectra', 'ra', 'dec', 'min_date', 'max_date']
    data = p.read_csv(file_name, names=cols, header=None)
    #embed()
    #define columns for difference in days between max and min and now and max
    data['max-min'] = data.apply(lambda x: (du.parser.parse(x['max_date']) - du.parser.parse(x['min_date'])).days, axis=1)
    data['max-now'] = data.apply(lambda x: ( datetime.datetime.now() - du.parser.parse(x['max_date'])).days, axis=1)

    data_one_spectrum = data[data.spectra==1]
    sorted_data = data_one_spectrum.sort(['cat','max-now'], ascending=False)
    data_html = sorted_data.to_html()
    with open(output_file, 'w') as file:
        file.write(data_html)
        
if __name__ == '__main__':
    main()
