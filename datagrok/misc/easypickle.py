"""Manage a single pickled object.

Nothing much clever here. Just a small adapter to make a pickle object easier
to use (like a shelf.)

        import easypickle
        d = easypickle.open(filename)	# open, with filename
		print d.data
		d.data = "blah"
        d.close()						# close it
"""
from __future__ import absolute_import
import pickle
import os

class EasyPickle(object):

	__slots__ = ['data', 'filename']
	
	def __init__(self, filename):
		self.filename = filename
		self.data = None
		if os.path.exists(filename):
			fh = file(self.filename)
			self.data = pickle.load(fh)
			fh.close()
	
	def write(self):
		fh = file(self.filename, 'wb')
		pickle.dump(self.data, fh)
		fh.close()
		del fh
	
	close = write

	def __del__(self):
		self.write()

if __name__ != "__main__":
	def open(filename):
		return EasyPickle(filename)
