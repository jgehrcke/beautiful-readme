# Beautiful-readme #

Beautiful-readme converts a single-file README into a simple and modern [Bootstrap](http://getbootstrap.com/)-powered static website.

## Demo ##
[Here](http://gehrcke.de/beautiful-readme) (built from *this* README).

## Input ##
- A small configuration file `conf.py` in the current working directory.
- A README file (reStructuredText or Markdown), e.g. `README.rst`.

## Usage example ##
```
$ beautiful-readme README.rst
```

## Output ##
A static website, according to the [KISS principle](http://en.wikipedia.org/wiki/KISS_principle).

## Features ##
- [reStructuredText](http://en.wikipedia.org/wiki/ReStructuredText) and [Markdown](http://en.wikipedia.org/wiki/Markdown) support.
- Modern and reliable HTML5 output ([Bootstrap blog template](http://getbootstrap.com/examples/blog/)-based).
- Mobile-friendly responsive layout with professional appearance.
- Google Analytics snippet support (optional).
- Custom CSS injection (optional).
- Custom sidebar HTML code injection (optional).



Major design goals of beautiful-readme: simplicity, clarity. For more feature-rich solutions, have a look at [Sphinx](http://sphinx-doc.org/) and [Beautiful docs](http://beautifuldocs.com/). Beautiful-readme is written and maintained by [Jan-Philip Gehrcke](http://gehrcke.de>). It is licensed under an MIT license (see LICENSE file).