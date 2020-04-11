# Change log

# unreleased
- Fix `--dry-run` in `--batch` mode
  ([PR #173](https://github.com/dbr/tvnamer/pull/173))
- Files are now moved using `shutil.move` instead of custom logic around `os.rename`, which should make things more robust in situations with unusual partition setups (e.g Docker environments)
  ([PR #161](https://github.com/dbr/tvnamer/pull/161))

# `2.5` - 2018-08-25
- Began keeping a changelog
- Added `--force-rename` and `--force-move` arguments
  ([PR #133](https://github.com/dbr/tvnamer/pull/133))
- Added `skip_behavior` option
  ([PR #111](https://github.com/dbr/tvnamer/pull/111))
- Added `--dry-run` argument
  ([PR #130](https://github.com/dbr/tvnamer/pull/130))
- Fix `normalize_unicode_filenames` in Python 3
  ([Issue #134](https://github.com/dbr/tvnamer/issues/134))
- Dropped support for Python 2.6. `tvnamer==2.4` is last version to
  support Python 2.6
- Added support for Python 3.6 and 3.7
- Fix search by air-date when episode had special episodes aired on same day
  ([PR #97](https://github.com/dbr/tvnamer/pull/97))
