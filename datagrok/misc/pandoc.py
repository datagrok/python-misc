"""Filter pandoc->html for use with e-mail clients like mutt."""

import subprocess
import re

# TODO: move email-specific bits to email module.

def pandoc(txt,
           _attr_re=re.compile(r'^[> ]*(.*wrote:)\n([> ]+)', re.M),
           _mailto_re=re.compile(r'<([^@]*@[^>]*)>')):
    # Signature marker would normally be converted to mdash with no line break,
    # so get rid of it.
    txt = txt.replace('\n-- \n', '\n\n')

    # Replace e-mail address with explicit markup to avoid pandoc's email
    # obfuscation logic (pandoc will have a command line option to avoid this in
    # the future)
    txt = _mailto_re.sub(r'<a href="mailto:\1">\1</a>', txt)

    # quoted email doesn't pandoc so well, pre-mark it a bit.
    txt = _attr_re.sub(r'\2<cite>\1</cite>  \n\2', txt)

    s = subprocess.Popen(
        ['pandoc',
         '-f', 'markdown',
         '-t', 'html',
         '-H', '/home/mike/etc/emailstyle.css',
         #'-S',
         '-s',
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    (ret, _) = s.communicate(txt)
    ret = ret.replace('<blockquote\n','<blockquote type="cite"\n')
    return ret

# vim: set ft=python :
