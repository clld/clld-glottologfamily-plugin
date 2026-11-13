# Releasing clld-glottologfamily-plugin

- Do platform test via tox:
  ```shell
  tox -r
  ```

- Make sure ruff passes:
  ```shell
  ruff check src
  ```

- Update the version number, by removing the trailing `.dev0` in:
  - `pyproject.toml`
  - `src/clld_glottologfamily_plugin/__init__.py`

- Create the release commit:
```shell
git commit -a -m "release <VERSION>"
```

- Create a release tag:
```
git tag -a v<VERSION> -m"<VERSION> release"
```

- Release to PyPI:
```shell
python setup.py clean --all
rm dist/*
python -m build -n
twine upload dist/*
```

- Push to github:
```shell
git push origin
git push --tags
```

- Increment version number and append `.dev0` to the version number for the new development cycle:
  - `src/clld_glottologfamily_plugin/__init__.py`
  - `pyproject.toml`

- Commit/push the version change:
```shell
git commit -a -m "bump version for development"
git push origin
```
