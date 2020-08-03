# `tvnamer` release procedure

1. Ensure CHANGELOG is up to date
2. Ensure tests are passing (CI and run again locally)
3. Verify settings in `setup.py` (e.g supported Python versions)
4. Bump version in `tvnamer/__init__.py`
5. Bump version/release date in CHANGELOG
6. Push changes to git
7. `python setup.py sdist upload`
8. Tag change, `git tag -a 0.0etc`
9. Push tag, `git push --tags`
10. Verify https://pypi.org/project/tvnamer/
11. Verify via virtual env

        mkvirtualenv tvnamertest
        pip install tvdb_api
        touch scrubs.s01e01.avi
        tvnamer scrubs.s01e01.avi
        ls Scrubs*
        deactivate
        rmvirtualenv tvnamertest
