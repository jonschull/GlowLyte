glowlyte
ShowLive

GlowLyte: GlowScript in Glitch
Pure Python GlowsScript, online and offline, with imports.

This is an experimental framework for Glowscript (Vpython) in the browser, and on the web. Based on Lyte and GlowScript.

To Bruce Sherwood's [GlowScript Offline system],(https://groups.google.com/forum/#!starred/glowscript-users/Qq0rExnxOYc) it adds the ability to import pure python and as-you-type real-time recompilation.

To run a program click in Glitch, click the green "Show Live" button above.

To remix the program, you should only need to modify the forGlowScript() function at the end of index.html

This demo is a force-directed graph layout routine written in python-compatible glowscript (based on [this])(http://patrickfuller.github.io/jgraph/examples/ipython.html).

Because it is written in python-compatible Glowscript the two pure python files can be run with the Python compiler, or via GlowLyte/RapydScript/GlowScript/Glitch in the browser.

The Project
← layerouter.py and main.py
layerouter.py contains the graph layout
it is imported by main.py
← README.md
That's this file.

← index.html
Adds to the GlowScript Offline system just enough javascript to enable rapydscript to install python.py files into rapydscript's virtual file system. In this case we install utils.py.

← style.css
CSS files add styling rules to your content.

← the jg directory
breaks glowscript.js into two sections to sandwich my stuff

first.js
(My stuff)
third.js
jg-style.css tweaks the GlowScript style sheet in order to hide the GlowScript source in the left-most pane. (You can drag it open.)

Author
Jon Schull, jschull@gmail.com, a python programmer who has tried to learn just enough javascript to not need javascript.
