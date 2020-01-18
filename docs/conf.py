# std imports
import os
import sys
import json
import functools

# local
import sphinx_rtd_theme
import sphinx.environment
from docutils.utils import get_source_line

# for github.py
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath('sphinxext'))
github_project_url = "https://github.com/jquast/blessed"


# ! Monkey Patching!
#
# Seems many folks beside ourselves would like to see external image urls
# **not** generated as a warning. "nonlocal image URI found": we want our
# "badge icons" on pypi and github, but we don't want to miss out on any
# other "warnings as errors" which we wish to fail the build if it happens.
#
# https://github.com/SuperCowPowers/workbench/issues/172
# https://groups.google.com/forum/#!topic/sphinx-users/GNx7PVXoZIU
# http://stackoverflow.com/a/28778969
#
def _warn_node(self, msg, node):
    if not msg.startswith('nonlocal image URI found:'):
        self._warnfunc(msg, '%s:%s' % get_source_line(node))


sphinx.environment.BuildEnvironment.warn_node = _warn_node


def no_op_wraps(func):
    """Replaces functools.wraps in order to undo wrapping when generating Sphinx documentation."""
    if func.__module__ is None or 'blessed' not in func.__module__:
        return functools.orig_wraps(func)

    def wrapper(decorator):
        sys.stderr.write('patched for function signature: {0!r}\n'.format(func))
        return func
    return wrapper


# Monkey-patch functools.wraps and contextlib.wraps
# https://github.com/sphinx-doc/sphinx/issues/1711#issuecomment-93126473
functools.orig_wraps = functools.wraps
functools.wraps = no_op_wraps
import contextlib  # isort:skip # noqa
contextlib.wraps = no_op_wraps
from blessed.terminal import *  # isort:skip # noqa

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx',
              'sphinx.ext.viewcode',
              'github',
              'sphinx_paramlinks',
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Blessed'
copyright = u'2011 Erik Rose, Jeff Quast, Avram Lubkin'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = json.load(
    open(os.path.join(HERE, os.pardir, 'version.json'), 'r')
)['version']

# The full version, including alpha/beta/rc tags.
release = version

# The language for content auto-generated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'blesseddoc'


# -- Options for LaTeX output -------------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index', 'blessed.tex', u'Blessed Documentation',
     u'Erik Rose, Jeff Quast, Avram Lubkin', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'Blessed', u'Blessed Documentation',
     [u'Erik Rose, Jeff Quast, Avram Lubkin'], 1)
]

# sort order of API documentation is by their appearance in source code
autodoc_member_order = 'bysource'

# when linking to standard python library, use and prefer python 3
# documentation.
intersphinx_mapping = {'https://docs.python.org/3/': None}

# Both the class’ and the __init__ method’s docstring are concatenated and
# inserted.
autoclass_content = "both"
