"""Making ANSI-format colored text for the terminal.

TODO: make this more intuitive to use.

TODO: There are other, more robust general-purpose libraries to interface with
ANSI-compatible terminals. Find one that is at least as intuitive and
featureful as this hack and upgrade to it.

"""

# ANSI Colors documentation:
#
# ESC[Ps;...;Psm
#     Set Graphics Mode: Calls the graphics functions specified by the
#     following values. These specified functions remain active until the next
#     occurrence of this escape sequence. Graphics mode changes the colors and
#     attributes of text (such as bold and underline) displayed on the screen.
#
#     Text attributes
#         0      All attributes off
#         1      Bold on
#         4      Underscore (on monochrome display adapter only)
#         5      Blink on
#         7      Reverse video on
#         8      Concealed on
#
#     Foreground colors
#         30      Black
#         31      Red
#         32      Green
#         33      Yellow
#         34      Blue
#         35      Magenta
#         36      Cyan
#         37      White
#
#     Background colors
#         40      Black
#         41      Red
#         42      Green
#         43      Yellow
#         44      Blue
#         45      Magenta
#         46      Cyan
#         47      White

class AnsiColor(object):
    """An object which wraps text in ANSI terminal color codes.

    >>> words = ['ERROR:', 'attempting to fix problem...', 'fixed.']

    Side-effect chainable accessor interface:

    >>> m = AnsiColor()
    >>> print ' '.join([
    ...     m.red.bold(words[0]),
    ...     words[1],
    ...     m.reset.bg_green.black(words[2])])
    ...
    \x1b[31;1mERROR:\x1b[m attempting to fix problem... \x1b[0;42;30mfixed.\x1b[m

    Python3 "new format" interface:

    >>> pattern = '{0:red/bold} {1} {2:reset/bg_green/black}'
    >>> print pattern.format(*(AnsiColor(x) for x in words))
    \x1b[31;1mERROR:\x1b[m attempting to fix problem... \x1b[0;42;30mfixed.\x1b[m
    """

    # TODO: split accessor-based and format()-based api into two different
    # classes.

    attributes = {
        None: 0,
        "reset": 0,

        "bold": 1, #bold
        "underline": 4, #underscore
        "underscore": 4, #underscore
        "blink": 5, #blink
        "reverse": 7, #reverse video
        "conceal": 8, #concealed

        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,

        "bg_black": 40,
        "bg_red": 41,
        "bg_green": 42,
        "bg_yellow": 43,
        "bg_blue": 44,
        "bg_magenta": 45,
        "bg_cyan": 46,
        "bg_white": 47,
    }

    def __init__(self, string=None):
        self.atts = []
        self.string = string

    def __add__(self, other):
        for att in other.atts:
            self.pushatt(att)
        return self

    def pushatt(self, att):
        if not att:
            self.atts = []
        elif att <= 8:
            self.atts = [x for x in self.atts if x > 8]
        elif att >= 30 and att <= 37:
            self.atts = [x for x in self.atts if x < 30 or x > 37]
        elif att >= 40 and att <= 47:
            self.atts = [x for x in self.atts if x < 40 or x > 47]
        self.atts.append(att)

    def __getattr__(self, key):
        val = self.attributes[key]
        self.pushatt(val)
        return self

    def __str__(self):
        return '\033[%sm' % ';'.join([str(x) for x in self.atts])

    def __call__(self, string):
        return '%s%s%s' % (str(self), string, '\033[m')

    def __format__(self, format_spec):
        if not format_spec:
            return self.string
        for f in format_spec.split('/'):
            if not f:
                continue
            getattr(self, f)
        return '%s%s%s' % (str(self), self.string, '\033[m')
