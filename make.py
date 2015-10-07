#!/usr/bin/env python

import os
import shutil
import urllib
from subprocess import call
import argparse
import simplejson as json
from ordereddict import OrderedDict
from jinja2 import FileSystemLoader, Environment
import codecs

from site_content import structure, functions
from site_content.examples import EXAMPLES

SITE_NAME = 'CamPL-NG'

LOCAL_JS = (
  'js/campl.js',
  'js/theme_switcher.js',
)

REMOTE_JS = (
  'https://code.jquery.com/jquery-1.11.3.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/moment.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/locale/en-gb.js',
  'https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.0.3/js.cookie.js',
  'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.37/js/bootstrap-datetimepicker.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/js/bootstrap.min.js',
)

JS = [os.path.basename(js) for js in REMOTE_JS + LOCAL_JS]

with open('themes.json') as f:
  COLOURS = json.loads(f.read(), object_pairs_hook=OrderedDict)

env = Environment(loader=FileSystemLoader('templates'))

# add functions
for fname in functions.__all__:
  env.globals.update(**{fname:functions.__dict__[fname]})

with open('site_content/links.json') as f:
  env.globals['LINKS'] = json.loads(f.read(), object_pairs_hook=OrderedDict)
  
env.globals['EXAMPLES'] = EXAMPLES

env.globals.update(**{
  'SITE_NAME': SITE_NAME,
  'LOCAL_JS': LOCAL_JS,
  'REMOTE_JS': REMOTE_JS,
  'MENU': structure.pages,
  'COLOURS': COLOURS,
})


for page in structure.pages:
  page.render(env)

structure.front_page.render(env)


