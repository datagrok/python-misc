
"""
Object-oriented color manipulation

A Color object holds information about a color, which may be accessed through
methods corresponding to various color spaces.

>>> x=Color(html="#ff0000") # red
>>> x.rgb
(1.0, 0.0, 0.0)
>>> x.hls
(0.0, 0.5, 1.0)


"""

from __future__ import absolute_import
import colorsys

def HLSColor(hls):
	return Color(hls=hls)

def RGBColor(rgb):
	return Color(rgb=rgb)

def HTMLColor(html):
	return Color(html=html)

class Color(object):
	"""A color, represented internally by floating-point
	(colorsys-compatable) rgb values."""
	def __init__(self, rgb=None, hls=None, hsv=None, html=None):
		if rgb:		self.set_rgb(rgb)
		elif hls:	self.set_hls(hls)
		elif html:	self.set_html(html)
		elif hsv:	raise NotImplementedError
		else:		self.set_rgb((0.0,0.0,0.0))
	def set_rgb(self, (r,g,b)):
		# if given ints, assume we need to do range
		# conversion.
		if isinstance(r, int): r /= 255.0
		if isinstance(g, int): g /= 255.0
		if isinstance(b, int): b /= 255.0
		r,g,b = [max(min(c, 1.0), 0.0) for c in [r,g,b]]
		self._rgb = (r,g,b)
		self._hls = colorsys.rgb_to_hls(r,g,b)
	def set_hls(self, (h,l,s)):
		# if given ints, assume we need to do range
		# conversion.
		if isinstance(h, int): h = (h%360)/360.0
		if isinstance(l, int): l /= 100.0
		if isinstance(s, int): s /= 100.0
		h = h % 1.0
		l,s = [max(min(c, 1.0), 0.0) for c in [l,s]]
		self._hls = (h,l,s)
		self._rgb = colorsys.hls_to_rgb(h,l,s)
	def _set_hlsc(n):
		def s(self, x):
			hls = list(self._hls)
			hls[n] = x
			self.set_hls(hls)
		return s
	def _set_rgbc(n):
		def s(self, x):
			rgb = list(self._rgb)
			rgb[n] = x
			self.set_rgb(rgb)
		return s
	def set_html(self, html):
		try:
			rgb = int(html[1:3],16), int(html[3:5],16), int(html[5:7],16)
		except:
			print "--%s--" % repr(html)
			raise
		self.set_rgb(rgb)
	def get_rgb(self):
		return self._rgb[:]
	def get_hls(self):
		return self._hls[:]
	def get_irgb(self):
		return tuple([int(round(x*255)) for x in self._rgb])
	def get_html(self):
		return "#%02x%02x%02x" % self.get_irgb()
	def _get_hlsc(n):
		return lambda s: s._hls[n]
	def _get_rgbc(n):
		return lambda s: s._rgb[n]
	rgb=property(get_rgb,set_rgb)
	hls=property(get_hls,set_hls)
	html=property(get_html,set_html)
	h=property(_get_hlsc(0),_set_hlsc(0))
	l=property(_get_hlsc(1),_set_hlsc(1))
	s=property(_get_hlsc(2),_set_hlsc(2))
	r=property(_get_rgbc(0),_set_rgbc(0))
	g=property(_get_rgbc(1),_set_rgbc(1))
	b=property(_get_rgbc(2),_set_rgbc(2))
	def __str__(self):
		return self.html
