# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../elaspy"))
sys.path.insert(0, os.path.abspath("../elaspy/mexclp"))
sys.path.insert(0, os.path.abspath("../elaspy/advanced_plotting"))


# -- Project information -----------------------------------------------------

project = "ELASPY"
author = "Nanne A. Dieleman, Caroline J. Jagtenberg"

# The full version, including alpha/beta/rc tags
release = "0.0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "sphinx_favicon",
]

napoleon_use_rtype = False
napoleon_use_param = False
napoleon_use_ivar = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
html_show_sourcelink = False
html_show_copyright = False
html_title = "ELASPY"

html_theme_options = {
    "logo": {
        "alt_text": "ELASPY - Home",
        "image_light": "_static/ELASPY_light.svg",
        "image_dark": "_static/ELASPY_dark.svg",
    },
    "show_prev_next": False,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/NanneD/ELASPY",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        }
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

favicons = [
   {"rel": "icon", "href": "ELASPY_favicon.png", "type": "image/png"},
   {"rel": "apple-touch-icon", "href": "ELASPY_favicon.png"}
]
