# based on http://tirl.org/blogs/media-lab-blog/50/

from django.contrib.markup.templatetags import markup
from django import template
register = template.Library()

@register.tag
def markdown(parser, token):
    args = token.contents[len("markdown"):].strip()
    nodelist = parser.parse(('endmarkdown',))
    parser.delete_first_token()
    return MarkdownNode(nodelist, args)

class MarkdownNode(template.Node):
    def __init__(self, nodelist, args):
        self.nodelist = nodelist
        self.args = args
    def render(self, context):
        output = self.nodelist.render(context)
        return markup.markdown(output, self.args)
