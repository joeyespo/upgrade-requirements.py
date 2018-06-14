upgrade-requirements.py
=======================
[![Current version on PyPI](https://img.shields.io/pypi/v/upgrade-requirements.svg)](https://pypi.python.org/pypi/upgrade-requirements/)

Upgrade all your outdated `requirements.txt` in a single command.


Motivation
----------

Even though `pip list --outdated` exists, sometimes you just want to
run `pip install --upgrade` to upgrade a package, then persist it to
your `requirements.txt` in one big sweep.


Installation
------------

```bash
$ pip install upgrade-requirements
```


Usage
-----

```bash
$ upgrade-requirements
```

(Or use the shortcut command `upreq`.)

Now's a good time to grab a ☕ while it runs.

After it finishes, run your tests to make sure an individual upgrade didn't
break anything. Then move on to bigger things 🚀

#### Found a problem with an upgraded version?

No worries!

1. Revert individual entries in `requirements.txt` with the help of git
2. Run `pip install -r requirements.txt` to downgrade to working versions
3. Commit the upgraded-and-tweaked `requirements.txt` like normal and carry on 🎉

#### More usages
```bash
$ upgrade-requirements -h
```

```
usage: upgrade-requirements [-h] [-r REQUIREMENTS]

optional arguments:
  -h, --help            show this help message and exit
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        specify the location of the requirements.txt file
```


Room for improvement
--------------------

- This only work with pinned (`==`) packages at the moment. The intention is to
  get it to work more generally. This can be broken down into three sub-tasks:

  - Get it to ignore non-pinned requirements instead of fail
  - Get it to work with other specifiers, e.g. `>=` (how would this work?)
  - Handle all types of requirement entries

Feel free to open an issue or PR with ideas.
