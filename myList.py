import os
import webbrowser

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
lst = os.listdir('.')

f = open("list.html", "w")
f.write(top)

for l in lst:
	f.write("<li>" + l + "</li>")

f.write("</ul></body></html>")
f.close()

# http://stackoverflow.com/a/5943706
webbrowser.open('file://' + os.path.realpath("list.html"))
