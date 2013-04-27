#!/usr/bin/python
# generate SAMP html page
# usage:l
# ../makeHtmlTable/makeHtmlTable.py "4/*_detail.png"
# generate html with SAMP button (which send spectra to splat)


import os, sys, glob, re



def main():

    if len(sys.argv) > 1:
        dir = sys.argv[1]
    else:
        sys.exit(1)


    files = glob.glob(dir)

    for f in files:
        (dir_name, file_name) = os.path.split(f)
        star_name = file_name.split('_')[0] # betcas_detail.png -> betcas
        path = os.path.join(dir_name, star_name, '*.fits')
        fits = glob.glob(path)
        fits_names = [os.path.split(path)[1] for path in fits]
        fits_list =(', '.join('"' + item + '"' for item in fits_names))
        page = get_page(fits_list, star_name,file_name)
        page_name = f.replace('.png','.html')
        save_page(page_name, page)

        
def save_page(file_name, page):
    with open(file_name,'w') as f:
        f.write(page)


def get_page(fits, star_name, file_name):

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
</header>
<script src="../../lib/samp.js"></script>

<script>
  // URL of table to send.
  var baseUrl = window.location.href.toString().replace(new RegExp("[^/]*$"), "");
  var fits = new Array(%s)

  // Broadcasts a table given a hub connection.
  var send = function(connection) {
      for (var i = 0; i < fits.length; i++) {
	  var link = baseUrl + "%s/" + fits[i]
          var msg = new samp.Message("spectrum.load.ssa-generic", {"url": link});
	  connection.notifyAll([msg]);		  
      };
  };

  // Adjusts page content depending on whether the hub exists or not.
  var configureSampEnabled = function(isHubRunning) {
      document.getElementById("sendButt").hidden = !isHubRunning;
  };

  // Arrange for document to be adjusted for presence of hub every 2 sec.
  var connector = new samp.Connector("Sender");
  onload = function() {
      connector.onHubAvailability(configureSampEnabled, 2000);
  };
  onunload = function() {
      connector.unregister();
  };
</script>

<img src="%s" alt="%s" >
<p>
<button id="sendButt" type="button" onclick="connector.runWithConnection(send)">SAMP</button>
</p>


<footer>
</footer>
</body>

</html> 
 """ % (fits, star_name, file_name, file_name)

    return page



if __name__ == "__main__":
    main()
