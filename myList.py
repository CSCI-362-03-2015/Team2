import os
import webbrowser

#This first part is the HTML styling. Makes things look nice. Also is the top portion of the HTML file.#
top = """<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Project Directory Contents</title>
	<style>
		body {
			font-family: "Helvetica", "Verdana", sans-serif;	
		}
		h1 {
			text-align: center;
		}
		ul {
			list-style-type: none;
			padding-left: 0px;
			width: 50%;
			margin: 0 auto;
		}
		ul:last-child {
			border-bottom: 1px #777 solid;
		}
		li {
			font-size: 16pt;
			margin: 0;
			padding: 5px;
			border: 1px #777 solid;
			border-bottom: none;
			text-align: center
		}
		li:hover {
			opacity: 0.8;
		}
		li:nth-child(even) {
			background-color: #c9d5df;
		}
		li:nth-child(odd) {
			background-color: #e6e4e4;
		}
		@media (max-width: 640px) {
			ul {
				width: 80%;
			}
		}
	</style>
</head>
<body>
<h1>Project Directory Listing</h1>
<ul>
"""
                            #notice how the HTML starts the list header to be written#
lst = os.listdir('.')       #lists the directory#

f = open("list.html", "w")  #opens the list.html to be written, as variable 'f'#
f.write(top)                #writes the style and first header for the HTML list (ie: top part)#

for l in lst:
    f.write("<li>" + l + "</li>")   #writes the list 'lst' with the HTML inside the HTML file#

f.write("</ul></body></html>")      #writes the bottom of the HTML body to the file.#
f.close()

webbrowser.open('file://' + os.path.realpath("list.html"))  #opens the HTML file with the default web browser.#

#http://stackoverflow.com/a/5943706 >> credit for figuring out "os.path.realpath"#
