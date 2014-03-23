#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Jan-Philip Gehrcke (http://gehrcke.de).
# See LICENSE file for details.


"""beautiful-readme.
"""


from __future__ import unicode_literals


import os
import re
import sys
import shutil
import urllib
import logging
import argparse
from collections import OrderedDict
from subprocess import Popen, PIPE


try:
    import HTMLParser as htmlparser
except ImportError:
    import html.parser as htmlparser


log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s,%(msecs)-6.1f - %(levelname)s: %(message)s',
    datefmt='%H:%M:%S')
ch.setFormatter(formatter)
log.addHandler(ch)


try:
    import jinja2
except ImportError:
    err("Missing dependency: cannot import jinja2.")


__version__ = "0.1.0"


# To be populated by argparse from cmdline arguments.
cmdlineopts = None


# To be popluated when executing config file.
config = {}


def main():
    global markdown
    global docutils
    global conf

    parse_options()

    resdir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "resources")
    log.debug("Identified resource dir: %s", resdir)
    if not os.path.isdir(resdir):
        err("Cannot access identified resource dir: %s" % resdir)

    log.info("Read config.")
    exec_config_file(cmdlineopts.configfile)

    try:
        if config["converter"] == "markdown":
            log.info("Importing markdown.")
            import markdown
            converter = MarkdownConverter()
        elif config["converter"] == "docutils":
            log.info("Importing docutils.")
            import docutils.core
            converter = DocutilsConverter()
        else:
            err("Config error: converter must be 'markdown' or 'docutils.")
    except ImportError:
        err("Missing dependency: cannort import %s." % config["converter"])

    # (Re-)create build directory.
    log.info("Create build directory.")
    if os.path.isdir(config["builddir"]):
        log.info("Purge previously existing build directory: %s",
            config["builddir"])
        shutil.rmtree(config["builddir"])
    os.mkdir(config["builddir"])
    # TODO: only do this if necessary (i.e. if CSS/JS resources required).
    log.info("Copy static files to build dir.")
    shutil.copytree(
        os.path.join(resdir, "static"),
        os.path.join(config["builddir"], "static"))

    jinjaenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=resdir),
        trim_blocks=False)
    # Read basic HTML scaffold.
    log.info("Read HTML template from %s", "index.html.tpl")
    htmltemplate = jinjaenv.get_template("index.html.tpl")

    sourceenc = "utf-8"
    log.info("Read %s, decode with %s codec.",
        cmdlineopts.readmefile, sourceenc)
    if not os.path.isfile(cmdlineopts.readmefile):
        err("Cannot find file: %s" % cmdlineopts.readmefile)
    with open(cmdlineopts.readmefile, "rb") as f:
        bodysource = f.read().decode(sourceenc)

    log.info("Create document body: convert source to HTML.")
    htmlbody = converter.process(bodysource)

    # Filter body.
    bodyfilter = []
    if config["converter"] == "markdown":
        bodyfilter.append(MarkdownTitleFilter())
    for bfilter in bodyfilter:
        htmlbody = bfilter.process(htmlbody)

    # Modify body on the fly (populate h2 tags with with ids).
    # Generate Table Of Contents HTML code on the fly.
    htmlbody, toc = auto_toc_from_h2(htmlbody)

    sidebar = config["sidebar"]
    # Just don't include TOC HTML if not desired (modified h2 tags are still
    # convenient).
    if config["sidebar_toc"]:
        log.info("Prepare sidebar TOC inclusion.")
        sidebar += "\n" + toc,
    else:
        log.info("Do not include sidebar TOC.")

    # Create HTML document: fill basic HTML template.
    log.info("Create main HTML document (fill template).")
    template_mapping = {
        "title": config["title"],
        "description": config["description"],
        "body": htmlbody,
        "about": config["about"],
        "copyright": config["copyright"],
        "sidebar": sidebar,
        "google_analytics_id": config["google_analytics_id"],
        "customcss": config["customcss"],
        }

    htmlout = htmltemplate.render(**template_mapping)

    # Write HTML document.
    indexhtmlpath = os.path.join(config["builddir"], "index.html")
    log.info("Write %s.", indexhtmlpath)
    with open(indexhtmlpath, "wb") as f:
        f.write(htmlout.encode("utf-8"))


def err(msg):
    log.error(msg)
    sys.exit(1)


class Converter(object):
    def __init__(self):
        pass


class DocutilsConverter(Converter):
    """
    http://docutils.sourceforge.net/docs/api/publisher.html
    """
    def process(self, doc):
        return self._html_fragment(doc)

    def _html_fragment(self, doc):
        """
        Return 'fragment' part of docutils HTML document. `doc` is unicode RST
        source.

        Largely copied from
        http://docutils.sourceforge.net/docutils/examples.py

        Parameters used below:
        - `source`: A multi-line text string; required.
        - `source_path`: Path to the source file or object. Optional, but useful
          for diagnostic output (system messages).
        - `destination_path`: Path to the file or object which will receive the
          output; optional.  Used for determining relative paths (stylesheets,
          source links, etc.).
        - `input_encoding`: The encoding of `input_string`.  If it is an encoded
          8-bit string, provide the correct encoding.  If it is a Unicode string,
          use "unicode", the default.
        - `doctitle_xform`: Disable the promotion of a lone top-level section
          title to document title (and subsequent section title to document
          subtitle promotion); enabled by default.
        - `initial_header_level`: The initial level for header elements (e.g. 1
          for "<h1>").
        """
        overrides = {
            'input_encoding': "unicode",
            'doctitle_xform': True,
            'initial_header_level': 2
            }
        parts = docutils.core.publish_parts(
            source=doc,
            source_path=None,
            destination_path=None,
            writer_name='html',
            settings_overrides=overrides)
        # "parts['fragment'] contains the document body (not the HTML <body>).
        # In other words, it contains the entire document, less the document
        # title, subtitle, docinfo, header, and footer."
        return parts["fragment"]


class MarkdownConverter(Converter):
    """
    https://pythonhosted.org/Markdown/reference.html
    """
    def process(self, doc):
        return markdown.markdown(
            text=doc,
            output_format="html5"
            )


class BodyFilterError(Exception):
    """Error class for all kind of issues during body filtering."""
    pass


class BodyFilter(object):
    """A filter for modifying the HTML code as returned by
    rst2html or markdown.
    """
    def __init__(self):
        pass

    def process(self, body):
        """_process must be implemented by children."""
        if not body:
            raise BodyFilterError("body is empty: %s" % body)
        log.debug("Body is about to be filtered by %s.", self.__class__.__name__)
        log.debug("Prefilter body length: %s", len(body))
        b = self._process(body)
        log.debug("Filter done. Postfilter body length: %s", len(b))
        return b


class DocutilsTitleFilter(BodyFilter):
    """From the first line, remove <h1 class="title">xxx</h1> in case of RST,
    and <h1>xxx</h1> in case of markdown.

    This program adds its own title. Hence, if docutils also adds a
    title, this filter removes it. Yes, in general we should not use
    RegEx for filtering HTML. In this case, however, it's not *any*
    HTML, it is *the* HTML as generated by docutils, and it is the
    first line and the first tag in the document. So we really do not
    anticipate the entire universe of HTML, and that's why RegEx is
    fine.
    """
    def _process(self, body):
        bodylines = body.splitlines()
        first = bodylines[0]
        if not "h1" in first:
            log.info("No h1 in first line of body. Skip.")
            return body
        match = re.search('<h1 class="title">.*</h1>', first)
        if not match:
            raise BodyFilterError("First line contains h1, but does not match pattern.")
        log.info('First line contains docutils title (<h1 class="title">...</h1>). Remove.')
        return "\n".join(bodylines[1:])


class MarkdownTitleFilter(BodyFilter):
    """From the first line, remove <h1>xxx</h1> in case of markdown.

    The idea is to remove the heading of highest hierarchy level. It is expected
    to be the document title which is added by this beautiful-readme anyway.

    In case of docutils, this issue is solved differently: the title detection
    is done by docutils itself and we don't request the title to be contained in
    the HTML output.

    TODO/expected problem: if original README does not have a clear title, i.e.
    of headings in the original README are all on the same hierarchy level or
    if the first heading shares its hierarchy level with another heading, then
    this filter does not make sense, probably.
    """
    def _process(self, body):
        bodylines = body.splitlines()
        first = bodylines[0]
        if not "h1" in first:
            log.info("No h1 in first line of body. Skip.")
            return body
        match = re.search('<h1>.*</h1>', first)
        if not match:
            raise BodyFilterError(
                "First line contains h1, but does not match pattern.")
        log.info('First line contains title (<h1>...</h1>). Remove.')
        return "\n".join(bodylines[1:])


def heading_to_label(heading):
    """Generate anchor id ("label") for heading.

    `heading` is the text between opening and closing h1 tag.
    """
    log.debug("Convert heading '%r' to anchor id.", heading)
    # First, decode HTML entities.
    h = htmlparser.HTMLParser().unescape(heading)
    log.debug("Unescaped heading: %r", h)
    # Then, split at whitespace. Then get rid of all
    # non-alphanumeric chars in each token.
    # Then reconnect tokens with "-".
    # Prepend "brtoc-" to ensure unique ids (any random string woud do).
    cleantokens = (re.sub('[^0-9a-zA-Z]+', '', s).lower() for s in h.split())
    return "brtoc-" + "-".join(t for t in cleantokens if t)


def auto_toc_from_h2(body):
    label_heading_dict = OrderedDict()
    def replace_heading(matchobj):
        heading = matchobj.group(1)
        label = heading_to_label(heading)
        log.info("Found heading: %r", heading)
        rpl = '<h2 id="%s">%s</h2>' % (label, heading)
        log.info("Replacing with: %r", rpl)
        # Save correspondence for later.
        label_heading_dict[label] = heading
        return rpl

    log.info("Scanning body for <h2>*</h2>, replacing on the fly.")
    body = re.sub("<h2>(.*)</h2>", replace_heading, body)

    # Validation of anchors: should be unique!
    # First check within the newly created labels.
    labels = label_heading_dict.keys()
    if len(set(labels)) != len(labels):
        log.error("Duplicate headline. Must be unique, abort.")
        sys.exit(1)

    listitems = []
    for label, heading in label_heading_dict.items():
        listitems.append('<li><a href="#%s">%s</a></li>' % (label, heading))
    # Produce some indentation.
    listhtml = "  " + "\n  ".join(listitems)
    log.debug("Generated the following toc list:\n%s", listhtml)
    # Add class "brcontents" (br namespace stands for beautiful-readme).
    prefix = ('<div class="sidebar-module brcontents">\n'
        '  <h4>Contents</h4>\n'
        '  <ol class="list-unstyled">')
    suffix = '  </ol>\n</div>'
    toc = "\n".join([prefix, listhtml, suffix])
    return body, toc


def parse_options():
    desc = "Create a simple mobile-friendly static website from your README."
    parser = argparse.ArgumentParser(
        prog="beautiful-readme",
        description=desc,
        epilog="Version %s" % __version__,
        add_help=False
        )
    parser.add_argument("-h", "--help", action="help",
        help="Show help message and exit."
        )
    parser.add_argument("--version", action="version",
        version=__version__, help="Show version information and exit."
        )
    parser.add_argument("-c", "--configfile", action="store",
        default="brconfig.py",
        help="Path to configuration file."
        )
    parser.add_argument("readmefile", action="store",
        metavar="README",
        help=("Path to a README file (reStructuredText or Markdown). Expected "
            "encoding: UTF-8.")
        )
    global cmdlineopts
    cmdlineopts = parser.parse_args()


def exec_config_file(cfgfilepath):
    # http://stackoverflow.com/a/6357418/145400
    # http://stackoverflow.com/a/8226090/145400
    # https://bitbucket.org/birkenfeld/sphinx/src/1.2.2/sphinx/util/pycompat.py
    if not os.path.isfile(cfgfilepath):
        err("Cannot access configuration file: %s." % cfgfilepath)
    global config
    if sys.version < '3':
        execfile(cfgfilepath, config)
    else:
        exec(
            compile(open(cfgfilepath, "rb").read(), cfgfilepath, 'exec'),
            config
            )


if __name__ == "__main__":
    main()


