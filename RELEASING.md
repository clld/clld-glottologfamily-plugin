Releasing clld-glottologfamily-plugin
=====================================

- Do platform test via tox:

  $ tox -r

  Make sure statement coverage is at 100%::

- Change setup.py version to the new version number.

- Bump version number:

  $ git commit -a -m"bumbed version number"

- Create a release tag:

  $ git tag -a v0.2 -m"first version to be released on pypi"

- Push to github:

  $ git push origin
  $ git push --tags

- Make sure your system Python has ``setuptools-git`` installed and release to
  PyPI::

  $ ./pypi.sh <release number>
