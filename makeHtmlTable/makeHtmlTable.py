#!/usr/bin/python

import os, sys, glob



def main():

    if len(sys.argv) > 1:
        dir = sys.argv[1]
        program = sys.argv[2]
    else:
        sys.exit(1)
    
    files = listdir(dir)
    nFiles = len(files)


    links = list(map(makeTag, files))
    fileName = program
    table = get_html_tbl(links,4)
    page = make_head_foot(program, nFiles, table)
    save_html(fileName, page)



def get_html_tbl(seq, col_count):
    if len(seq) % col_count:
        seq.extend([''] * (col_count - len(seq) % col_count))
    tbl_template = '<table style="border: 1px solid #000000; border-collapse: collapse;" border="1">%s</table>' % ('<tr>%s</tr>' % ('<td>%s</td>' * col_count) * (len(seq)/col_count))
    return tbl_template % tuple(seq)

def save_html(fileName,page):
    f =  open(fileName + '.html','w')
    f.write(page)
    f.close()

def make_head_foot(program, nFiles, table):

    page = """
       <!doctype html>
       <html>
       <head> 
       <meta charset="utf-8"/>
       <title></title>
       
       <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0"/>
       <link rel="stylesheet" href=""/>
       </head>
       
       <body>
       <header>
       <h1>Program: %s. Number of Files: %i</h1>
       </header>

       <div>
       %s
       </div>

       <footer>
       </footer>

       <script src=""></script>
       </body>

       </html> """ % (program, nFiles, table)

    return page

def makeTag(name):
    base_name = os.path.basename(name)
    name_no_ext = os.path.splitext(base_name)[0]
    link = 'http://skyserver.sdss3.org/dr8/en/tools/explore/obj.asp?sid=%s' % name_no_ext
    tag = '<a href="%s"><img src="%s/%s" width = "300" border="0" alt="Spectrum of %s"></a>' % (link, 'segue2', base_name, name_no_ext)

    return tag

def listdir(d):
    return glob.glob(d + '/*.png')


if __name__ == "__main__":
    main()


    