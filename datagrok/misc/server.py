#!/usr/bin/python

"""MultiviewsRequestHandler

Serve the files from the current directory on port 8000. Also,
	- Simulate the apache option +Multiviews.
	- Pages returned for folders are named "contents.*" not "index.*"

I (used to) use this to test-serve web files on my local box before I upload
them. Lately, I'm trying a different approach that does not employ MultiViews,
so this may go without any updates for a long time.

"""
from __future__ import absolute_import
import os
import SimpleHTTPServer

class MultiViewsRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def send_head(self):
		"""Common code for GET and HEAD commands.

		This really just implements file existence checking for the Multiviews
		trick, and calls the send_head method of the superclass.
		"""
				
		path = self.translate_path(self.path, forreal=True)

		"""This is the code for Multiviews"""
		if not os.path.exists(path):
			(parent,file)=os.path.split(path)
			if not file:
				self.send_error(404, "File not found")
				return None
			if not os.path.exists(parent):
				self.send_error(404, "File not found")
				return None
			for f in os.listdir(parent):
				if f.startswith(file):
					file=f
					break
			path=os.path.join(parent,file)

		"""This pre-empts the auto-dirlist code in SimpleHTTPServer"""
		if os.path.isdir(path):
			if not self.path.endswith("/"):
				self.send_response(301)
				self.send_header('Location', self.path + "/")
				return None
			for index in "contents.html", "contents.htm":
				index = os.path.join(path, index)
				if os.path.exists(index):
					path = index
					break
				else:
					return self.list_directory(path)

		self.path=path
		return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

	def translate_path(self, path, forreal=False):
		"""Translate a /-separated PATH to the local filename syntax.

		MultiViewsRequestHandler calls this twice, (because I'd rather do funky
		subclassing tricks than copy+paste+edit lots of code) so we have to
		turn this off once it's been done."""
		if forreal:
			return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)
		return path

def test(HandlerClass=MultiViewsRequestHandler,):
	SimpleHTTPServer.test(HandlerClass=HandlerClass)

serve = test

if __name__ == "__main__":
	test()
