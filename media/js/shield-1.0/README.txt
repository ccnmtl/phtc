SHIELD v. 1.0 is a simple JS-based widget that writes out a warning box to alert users that their browser is incompatible to those being listed as the minimum required browsers.

It is a prohibitive model, that is, the listed required browsers are the only ones supported.  Currently, this script supports browsers Chrome, Safari, Firefox and MSIE (Internet Explorer).

HOW TO USE:
-----------

1. Cut-and-paste the following code in the <head> section of your site:

<link rel="stylesheet" href="http://ccnmtl.columbia.edu/remote/alerts/shield-1.0/shield.css" type="text/css" media="all" />
<script src="http://ccnmtl.columbia.edu/remote/alerts/shield-1.0/browserdetect.js" type="text/javascript" language="javascript"></script>
<script type="text/javascript" src="http://ccnmtl.columbia.edu/remote/alerts/shield-1.0/shield.js"></script>
<script type="text/javascript">
/* Select from list: Chrome, Firefox, Safari, MSIE */
shieldbrowser({"<browser_name>":<minimum_version>});
</script>

Explanation:

<link rel="stylesheet" href="http://ccnmtl.columbia.edu/remote/alerts/shield-1.0/shield.css" type="text/css" media="all" />
This is to call the CSS which defines what the warning box will look like.

<script src="http://ccnmtl.columbia.edu/remote/alerts/shield-1.0/browserdetect.js" type="text/javascript" language="javascript"></script>
This script details the browser detection. It is taken from http://www.quirksmode.org/js/detect.html

<script type="text/javascript" src="http://ccnmtl.columbia.edu/remote/alerts/shield-1.0/shield.js"></script>
This script is homebrewed, and it takes advantage of browserdetect.js and writes out the warning box. The function shieldbrowser() is defined in this file.

<script type="text/javascript">
/* Select from list: Chrome, Firefox, Safari, MSIE */
shieldbrowser({"<browser name>":<version>});
</script>
shieldbrowser() is the function that calls the check and writes out the warning box.
<browser name> should be from the following list: Chrome, Firefox, Safari, MSIE
<minimum_version> is the integer of the minimum required version of the browser.
For example, with COMMA SEPARATED, multiple browser-version pairings:
shieldbrowser({"Firefox":6,"Safari":5,"MSIE":9,"Chrome":13});
This means that the site will function nicely in at least  Fifefox v.6, Safari v.5, Internet Explorer v.9 and Chrome v.13

SHIELD looks at the list of browsers called here and compares the browser name and versions to what the user has. If there's a mismatch, SHIELD will write out the error and the icon-link pairs to the browers defined. In other word, if you list out only the browsers you list out in the function call.

Right now, the versions are interger values. This developer understands the possibility of decimal versions and will be including the fixes in shield.js soon.


2. Cut-and-paste the following code where you want the alert to appear.
<div id="shieldbox"></div>

3. Test on your browsers.

Developer: Zarina Mustapha
Adapted from codes by:
http://www.ie6nomore.com/
and
