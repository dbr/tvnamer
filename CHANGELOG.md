# Change log

# unreleased
- Fix `--dry-run` in `--batch` mode
  ([PR #173](https://github.com/dbr/tvnamer/pull/173))
- Config has moved to `~/.config/tvnamer/tvnamer.json` to avoid home-directory clutter (previously located at `~/.tvnamer.json`)
  ([PR #175](https://github.com/dbr/tvnamer/pull/175))
- Files are now moved using `shutil.move` instead of custom logic around `os.rename`, which should make things more robust in situations with unusual partition setups (e.g Docker environments)
  ([PR #161](https://github.com/dbr/tvnamer/pull/161))
- Add command line argument to override language, e.g `tvnamer --lang de [...]`
  ([PR #165](https://github.com/dbr/tvnamer/pull/165))
- Add `tvnamer --version` to display useful debug info
- Can now be run via `python -m tvnamer` as well as the usual `tvnamer` command
- New TheTVDB API key specifically for tvnamer
- Various internal improvements to testing and compatability with later Python 3.x changes
- Dropping explicit support for EOL Python 3.3 and 3.4 (may still work but not tested). 2.7 support remains for now

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
