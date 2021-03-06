# -*- coding: utf-8 -*-

from os.path import dirname
import sys
sys.path.insert(0, dirname(dirname(dirname(__file__))))

# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'matplotlib.sphinxext.plot_directive',
]

templates_path = []  # ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# General information about the project.
project = u'fillplots'
copyright = u'2013, Takafumi Arakaki'

# The short X.Y version.
version = '0.0.3'
# The full version, including alpha/beta/rc tags.
release = '0.0.3.dev1'

exclude_patterns = []

pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'fillplotsdoc'


# -- Options for LaTeX output ---------------------------------------------
latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'fillplots.tex', u'fillplots Documentation',
   u'Takafumi Arakaki', 'manual'),
]


# -- Options for manual page output ---------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'fillplots', u'fillplots Documentation',
     [u'Takafumi Arakaki'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------
# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'fillplots', u'fillplots Documentation',
   u'Takafumi Arakaki', 'fillplots', 'One line description of project.',
   'Miscellaneous'),
]


# -- Options for extensions -----------------------------------------------

intersphinx_mapping = {
    'pythone': ('http://docs.python.org/', None),
    'matplotlib': ('http://matplotlib.org/', None),
}

autodoc_member_order = 'bysource'
autodoc_default_flags = ['members']
