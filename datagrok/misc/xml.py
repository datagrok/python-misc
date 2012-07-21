"""Utilities for working with XML.

    Warning: this module overlaps the name of a module in the Python standard
    library. If you're a sensible and pragmatic developer who obeys the
    recommendations in the Python documentation, you may wish to rename this
    module before use.

XML is crap. Wow, I hate XML.

builder() lets you build your XML crap from a structure made of tuples, lists,
and dicts.

But really, why are you using XML in the first place?

I think it would be totally appropriate to trigger RuntimeWarnings whenever
this library is used for anything other than XHTML or ODF. And in those cases,
I think it would be appropriate to silently spam out an email to the W3C on
your behalf telling them where to stick their committee-based designs. Maybe in
the next version...

"""
from __future__ import absolute_import
import xml.dom.minidom

def builder(tree):
    """Converts a tree structure constructed from intrinsic types (tuples,
    dicts, lists) to an xml.dom.minidom tree.
    
    Each node in the input tree is a tuple or a string. Strings become DOM text
    elements. Tuples become node elements, and take one of the forms:

        (name, attrs, children)
        (name, attrs)
        (name, children)

    Where:
        - name(string):   the xml tag name
        - attrs(dict):    the string keys and string values representing the element attributes
        - children(list): a list of nodes in this same format.

    """

    d = (xml.dom.minidom
         .getDOMImplementation()
         .createDocument((tree[1] or {}).get('xmlns', None), tree[0], None))
    return _builder(d, d.documentElement, tree[1], tree[2])


def _builder(doc, node, attrs, children):
    """Recursive helper to builder"""
    for key in attrs or []:
        node.setAttribute(key, attrs[key])
    for child in children or []:
        if isinstance(child, str):
            node.appendChild(doc.createTextNode(child))
        elif len(child) == 2:
            if isinstance(child[1], dict): # no children
                node.appendChild(_builder(doc, doc.createElement(child[0]), child[1], None))
            else: # no attrs
                node.appendChild(_builder(doc, doc.createElement(child[0]), None, child[1]))
        elif len(child) == 3:
            node.appendChild(_builder(doc, doc.createElement(child[0]), child[1], child[2]))
        else:
            raise ValueError()
    return node
