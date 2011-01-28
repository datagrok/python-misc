
"""A quick hack for making ansi colored text on the terminal.

Todo: make this more intuitive to use.
"""


"""
ESC[Ps;...;Psm
    Set Graphics Mode: Calls the graphics functions specified by the
    following values. These specified functions remain active until the next
    occurrence of this escape sequence. Graphics mode changes the colors and
    attributes of text (such as bold and underline) displayed on the
    screen.
 
    Text attributes
       0    All attributes off
       1    Bold on
       4    Underscore (on monochrome display adapter only)
       5    Blink on
       7    Reverse video on
       8    Concealed on
 
    Foreground colors
       30    Black
       31    Red
       32    Green
       33    Yellow
       34    Blue
       35    Magenta
       36    Cyan
       37    White
 
    Background colors
       40    Black
       41    Red
       42    Green
       43    Yellow
       44    Blue
       45    Magenta
       46    Cyan
       47    White
"""

class AnsiColor:
	_at_map = {
		None: "",
		"no":"0", #normal
		"bo":"1", #bold
		"un":"4", #underscore
		"bl":"5", #blink
		"rv":"7", #reverse video
		"cn":"8", #concealed
	}
	_fg_map = {
		None: "",
		"bk":"30",
		"r ":"31",
		"g ":"32",
		"y ":"33",
		"bl":"34",
		"m ":"35",
		"c ":"36",
		"w ":"37",
	}
	_bg_map = {
		None: "",
		"bk":"40",
		"r ":"41",
		"g ":"42",
		"y ":"43",
		"bl":"44",
		"m ":"45",
		"c ":"46",
		"w ":"47",
	}
	def __init__(self,attr=None,fg=None,bg=None):
		self.set_attr(attr)
		self.set_fg(fg)
		self.set_bg(bg)
	def set_attr(self,attr):
		if attr in self._at_map.keys():
			self.at = self._at_map[attr]
	def set_fg(self,color):
		if color in self._fg_map.keys():
			self.fg = self._fg_map[color]
	def set_bg(self,color):
		if color in self._bg_map.keys():
			self.bg = self._bg_map[color]
	def __str__(self):
		ret=["\033["]
		ret.append(self.at)
		ret.append(";")
		ret.append(self.fg)
		if self.bg:
			ret.append(";")
			ret.append(self.bg)
		ret.append("m")
		return "".join(ret)

class AnsiMarker:
		"""
    """
		def __init__(self):
			self.ac=AnsiColor()
			self.nc=AnsiColor()
		def __getattr__(self, key):
			if self.ac._at_map.has_key(key):
				self.ac.set_attr(key)
			elif self.ac._fg_map.has_key(key):
				self.ac.set_fg(key)
			elif key.startswith('b') and self.ac._bg_map.has_key(key[1:]):
				self.ac.set_bg(key[1:])
			else:
				raise AttributeError, repr(key)
			return self
		def __call__(self, string, *args, **kw):
			return ''.join([str(self.ac),string,str(self.nc)])

if __name__ == "__main__":
	x = AnsiColor()
	y = AnsiColor()
	for attr in x._at_map.keys():
		x.set_attr(attr)
		for fg in x._fg_map.keys():
			x.set_fg(fg)
			for bg in x._bg_map.keys():
				x.set_bg(bg)
				print x, (attr or "--"), (fg or "--"), (bg or "--"), y,
			print y
		print y
	print y, "Done."

	m=AnsiMarker()
	print "Hey there.", m.red.bold("this is a test."), "cool?", m.bgreen.black.normal("cool.")

# vim:ts=2:nowrap:sw=2
