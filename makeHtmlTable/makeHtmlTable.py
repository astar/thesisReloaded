#!/usr/bin/python
# generate html table from input files
# usage:l
# ../makeHtmlTable/makeHtmlTable.py "4/*_preview.png"
# generate html; table of directory ../data/corrupt_segue_small named 4.htm


import os, sys, glob, re



def main():

    if len(sys.argv) > 1:
        dir = sys.argv[1]
    else:
        sys.exit(1)

    local = 1 # use local file or sdss link
#    import ipdb; ipdb.set_trace()
    nFiles, files = listdir(dir)

#    import ipdb; ipdb.set_trace()
    l = [local for x in files] # prasarna mp needs local value for every file
    links = list(map(makeTag, files, l))
    fileName = os.path.split(dir)[0]
    table = get_html_tbl(links,4)
    page = make_head_foot(fileName, nFiles, table)
    save_html(fileName, page)



def get_html_tbl(seq, col_count):
    if len(seq) % col_count:
        seq.extend([''] * (col_count - len(seq) % col_count))
    tbl_template = '<table style="border: 1px solid #000000; border-collapse: collapse;" border="1">%s</table>' % ('<tr>%s</tr>' % ('<td>%s</td>' * col_count) * (len(seq)/col_count))
    return tbl_template % tuple(seq)

def save_html(name, page):
#    import ipdb; ipdb.set_trace()
    f =  open(name + '.html','w')
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

def makeTag(name, local):
    base_name = os.path.basename(name)
    name_no_ext = os.path.splitext(base_name)[0]
    name_no_ext = re.sub('.*_.*_','', name_no_ext)
    if local:
        link = name.replace('preview.png','detail.html')
        
    else:
        link = 'http://skyserver.sdss3.org/dr8/en/tools/explore/obj.asp?sid=%s' % name_no_ext
#    tag = '<a href="%s"><img src="%s/%s" width = "300" border="0" alt="Spectrum of %s"></a>' % (link, 'thm', base_name, name_no_ext)

#    tag = '<a href="%s"><img src="%s" width = "300" border="0" alt="Spectrum of %s"></a>' % (link, base_name, name_no_ext)
    tag = '<a href="%s"><img src="%s" width = "300" border="0" alt="Spectrum of %s"></a>' % (link, name, name_no_ext)

    return tag

def listdir(d):
    return len(glob.glob(d)), glob.glob(d)


if __name__ == "__main__":
    main()
