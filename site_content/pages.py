import codecs
import os
from jinja2 import FileSystemLoader, Environment, meta

BASE_BREADCRUMB = [('Campl-NG', '/')]


class Pages(list):

    def __init__(self, *args):
        list.__init__(self, *args)
        for page in self:
            page.update_url()
        for page in self:
            page.update_breadcrumbs(self)


TEMPLATE_REFERENCES = {}

REFERENCING_TEMPLATES = {}

TEMPLATE_PAGES = []


def template_to_tuple(templates):
    return [
        (
            ' > '.join(t.split('/')),
            '/templates/%s/' % t
        ) for t in templates
    ]


t_env = Environment(loader=FileSystemLoader('templates'))

for template_name in t_env.list_templates():
    if not template_name.startswith(('.', 'meta')) and \
            template_name.endswith('.html'):

        refs = list(
            meta.find_referenced_templates(
                t_env.parse(
                    t_env.loader.get_source(t_env, template_name)[0]
                )
            )
        )
        TEMPLATE_REFERENCES[template_name] = refs
        for ref in refs:
            REFERENCING_TEMPLATES.setdefault(ref, []).append(template_name)


class Page(object):
    def __init__(
            self,
            title,
            source=None,
            context={},
            children=[],
            globals={},
            side_menu=True,
            scss=[]
    ):
        self.title = title
        self.source = source
        self._context = context
        self._url = '/%s' % self.title.lower().replace(' ', '_')
        self.children = children
        self.horizontal_breadcrumb = []
        self.vertical_breadcrumb = []
        self.vertical_breadcrumb_parent = None
        self.vertical_breadcrumb_children = None
        self.vertical_breadcrumb_siblings = []
        self.globals = globals
        self.side_menu = side_menu
        self.type = 'page'
        self.scss = scss

    def render(self, env):
        if self.source:
            template = env.get_template(self.source, globals=self.globals)
            context = self.context
            context['page'] = self
            destination = os.path.join('build', self.url[1:], 'index.html')

            if not os.path.exists(os.path.dirname(destination)):
                os.makedirs(os.path.dirname(destination))
            with codecs.open(destination, 'wb', 'utf-8') as fh:
                fh.write(template.render(**context))
        for child in self.children:
            child.render(env)

    @property
    def destination(self):
        return os.path.join(self.url[1:], 'index.html')

    def update_url(self, root=None, parent=None):
        self.parent = parent
        if root:
            self._url = root + self._url
        for child in self.children:
            child.update_url(self._url, self)

    def update_breadcrumbs(
            self,
            pages,
            vertical_breadcrumb=BASE_BREADCRUMB,
            horizontal_breadcrumb=BASE_BREADCRUMB,
            parent=None
    ):
        if self.source:
            self.horizontal_breadcrumb = horizontal_breadcrumb + \
                                         [(self.title, self.url)]
        else:
            self.horizontal_breadcrumb = horizontal_breadcrumb + [(self.title, None)]
        self.vertical_breadcrumb = vertical_breadcrumb + [(self.title, self.url)]

        vertical_breadcrumb_base = self.vertical_breadcrumb
        horizontal_breadcrumb_base = self.horizontal_breadcrumb

        if self.children:
            self.vertical_breadcrumb_parent = self.horizontal_breadcrumb[-1]
            self.vertical_breadcrumb = self.vertical_breadcrumb[:-1]
            self.vertical_breadcrumb_children = [
                (child.title, child.url) for child in self.children
            ]
            if parent:
                self.vertical_breadcrumb_siblings = [
                    (child.title, child.url) for child in parent.children
                ]
            else:
                self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
        elif not parent:
            self.vertical_breadcrumb = BASE_BREADCRUMB
            self.vertical_breadcrumb_parent = (self.title, self.url)
            self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
        else:
            self.vertical_breadcrumb_parent = self.horizontal_breadcrumb[-2]
            self.vertical_breadcrumb = self.vertical_breadcrumb[:-2]
            if parent:
                self.vertical_breadcrumb_children = [
                    (child.title, child.url) for child in parent.children
                ]
                self.vertical_breadcrumb_siblings = parent.vertical_breadcrumb_siblings
        for child in self.children:
            child.update_breadcrumbs(
                pages,
                vertical_breadcrumb_base,
                horizontal_breadcrumb_base,
                self
            )

    @property
    def url(self):
        if self.source:
            return self._url
        elif self.children:
            return self.children[0].url
        else:
            return ''

    @property
    def context(self):
        return self._context


class SCSSPage(Page):

    def __init__(self, title, source=None, **kwargs):
        super(SCSSPage, self).__init__(title, source, **kwargs)
        if source:
            self.title = title.lstrip('_')
        else:
            self.title = title.replace('_', ' ').title()
        self.type = 'scss'

    def render(self, env):
        if self.source:
            with open(
                    os.path.join('scss', *self.url.split('/')[2:]), 'r'
            ) as scss_file:
                scss = scss_file.read()
            template = env.get_template('meta/stylesheet.html')
            context = {
                'page': self,
                'scss': scss,
            }
            destination = os.path.join('build', self.url[1:], 'index.html')
            if not os.path.exists(os.path.dirname(destination)):
                os.makedirs(os.path.dirname(destination))
            with codecs.open(destination, 'wb', 'utf-8') as fh:
                fh.write(template.render(**context))
        for child in self.children:
            child.render(env)


class TemplatePage(Page):

    def __init__(self, title, source=None, **kwargs):
        super(TemplatePage, self).__init__(title, source, **kwargs)
        if not source:
            self.title = title.replace('_', ' ').title()
        self.type = 'template'

    def render(self, env):
        if self.source:
            template = env.get_template('meta/template.html')
            template_file = os.path.join(*self.url.split('/')[2:])
            context = {
                'page': self,
                'template': env.loader.get_source(env, template_file)[0],
                'template_references': template_to_tuple(
                    TEMPLATE_REFERENCES.get(template_file, [])
                ),
                'referencing_templates': template_to_tuple(
                    REFERENCING_TEMPLATES.get(template_file, [])
                ),
            }
            destination = os.path.join('build', self.url[1:], 'index.html')

            if not os.path.exists(os.path.dirname(destination)):
                os.makedirs(os.path.dirname(destination))
            with codecs.open(destination, 'wb', 'utf-8') as fh:
                fh.write(template.render(**context))
        for child in self.children:
            child.render(env)


class CoffeePage(Page):

    def __init__(self, title, source=None, **kwargs):
        super(CoffeePage, self).__init__(title, source, **kwargs)
        if not source:
            self.title = title.replace('_', ' ').title()
        self.type = 'template'

    def render(self, env):
        if self.source:
            with open(
                    os.path.join('coffee', *self.url.split('/')[2:]), 'r'
            ) as coffee_file:
                coffee = coffee_file.read()
            template = env.get_template('meta/script.html')
            context = {
                'page': self,
                'coffee': coffee,
            }
            destination = os.path.join('build', self.url[1:], 'index.html')
            if not os.path.exists(os.path.dirname(destination)):
                os.makedirs(os.path.dirname(destination))
            with codecs.open(destination, 'wb', 'utf-8') as fh:
                fh.write(template.render(**context))
        for child in self.children:
            child.render(env)


class FrontPage(Page):

    @property
    def destination(self):
        return 'index.html'

    @property
    def url(self):
        return ''

    def __init__(self, title, source, pages):
        super(FrontPage, self).__init__(title, source)
        self.vertical_breadcrumb = BASE_BREADCRUMB
        self.front_page = True
        self.vertical_breadcrumb_siblings = [(p.title, p.url) for p in pages]
        self.side_menu = False
