"""Small HTML tree helpers for the static portfolio build."""
from html.parser import HTMLParser
from html import escape

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Node:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []

    def find(self, fn):
        result = [self] if fn(self) else []
        for child in self.children:
            if isinstance(child, Node):
                result += child.find(fn)
        return result

    def has(self, cls):
        return cls in self.attrs.get('class', '').split()

    def text(self):
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)

    def inner(self):
        return ''.join(c.html() if isinstance(c, Node) else escape(c, quote=False) for c in self.children)

    def html(self):
        if not self.tag:
            return self.inner()
        attrs = ''.join(' ' + k if v is None else f' {k}="{escape(str(v), quote=True)}"' for k, v in self.attrs.items())
        return f'<{self.tag}{attrs}>' + ('' if self.tag in VOID else self.inner() + f'</{self.tag}>')


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)
