# Beautiful-readme #

Beautiful-readme converts a single readme file into a simple and modern [Bootstrap](http://getbootstrap.com/)-powered static website. Simplicity ([KISS](http://en.wikipedia.org/wiki/KISS_principle)) and clarity are the major design goals of beautiful-readme. For more feature-rich solutions, I recommend having a look at [Sphinx](http://sphinx-doc.org/) and [Beautiful docs](http://beautifuldocs.com/).

## Demo ##
[Here](http://gehrcke.de/beautiful-readme) (built from *this* readme) and
[here](http://gehrcke.de/timegaps) (built from a readme for another project).


## Usage example ##
Input:

- A small configuration file (default name: `brconfig.py`).
- A readme file (reStructuredText or Markdown), e.g. `README.rst`.

Execute `$ beautiful-readme README.rst` and a static website is created in the
`_build` directory.


## Features ##
- [reStructuredText](http://en.wikipedia.org/wiki/ReStructuredText) and [Markdown](http://en.wikipedia.org/wiki/Markdown) support.
- Modern and reliable HTML5 output (based on the [Bootstrap blog template](http://getbootstrap.com/examples/blog/)).
- Mobile-friendly responsive layout with professional appearance.
- Google Analytics snippet support (optional).
- Custom CSS injection (optional).
- Custom sidebar HTML code injection (optional).


## Installation ##
Beautiful-readme releases are hosted [on PyPI](https://pypi.python.org/pypi/beautiful-readme). Installation with pip is recommended:

```
$ pip install beautiful-readme
```



## Author & License
Beautiful-readme is written and maintained by [Jan-Philip Gehrcke](http://gehrcke.de>). It is licensed under an MIT license (see LICENSE file).


## Changelog ##
#### Version 0.1.0 (Month dd, YYYY) ####
- Initial release.



