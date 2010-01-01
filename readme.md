# `tvnamer`

`tvnamer` is a utility which uses [`tvdb_api`](http://github.com/dbr/tvdb_api) to rename files from `some.show.s01e03.blah.abc.avi` to `Some Show - [01x03] - The Episode Name.avi` (by retrieving the episode name using `tvdb_api`)

## To install

You can easily install `tvnamer` via `easy_install`

    easy_install tvnamer

This installs the `tvnamer` command-line tool (and the `tvdb_api` module as a requirement)

You may need to use sudo, depending on your setup:

    sudo easy_install tvnamer

## Improvements over v1

tvnamer v2 is a near-complete rewrite of the tvnamer released as part of `tvdb_api`. There are many improvements thanks to the improved code structure, but the most important are:

- Support for anime filenames, such as `[Shinsen-Subs] Beet - 19 [24DAB497].mkv`
- Support for multi-episode files, such as `scrubs.s01e23e24.avi`
- Custom configuration options (via an XML config file)
- Better support for Unicode filenames

## Bugs?

Ideally file a ticket on the [tvnamer Lighthouse ticket site](http://dbr.lighthouseapp.com/projects/36049-tvnamer). Lighthouse is preferred, but alternatively you can leave a ticket on on tvnamer's [Github Issues page](http://github.com/dbr/tvnamer/issues)

Please make tickets for any possible bugs or feature requests, or if you discover a filename format that tvnamer cannot parse (as long as a reasonably common format, and has enough information to be parsed!), or if you are struggling with the a custom configuration (please state your desired filename output, and what problems you are encountering)

## Basic usage

From the command line, simply run:

    tvnamer the.file.s01e01.avi

For example:

    $ tvnamer brass.eye.s01e01.avi
    ####################
    # Starting tvnamer
    # Found 1 episodes
    # Processing brass.eye.s01e01.avi
    TVDB Search Results:
    1 -> Brass Eye [en] # http://thetvdb.com/?tab=series&id=70679&lid=7
    Automatically selecting only result
    ####################
    # Old filename: brass.eye.s01e01.avi
    # New filename: Brass Eye - [01x01] - Animals.avi
    Rename?
    ([y]/n/a/q) 

Enter `y` then press `return` and the file will be renamed to "Brass Eye - [01x01] - Animals.avi". You can also simply press `return` to select the default option, denoted by the surrounding `[]`

If there are multiple shows with the same (or similar) names or languages, you will be asked to select the correct one - "Lost" is a good example of this:

    $ tvnamer lost.s01e01.avi 
    ####################
    # Starting tvnamer
    # Found 1 episodes
    # Processing lost.s01e01.avi
    TVDB Search Results:
    1 -> Lost [en] # http://thetvdb.com/?tab=series&id=73739&lid=7
    2 -> Lost [sv] # http://thetvdb.com/?tab=series&id=73739&lid=8
    3 -> Lost [no] # http://thetvdb.com/?tab=series&id=73739&lid=9
    4 -> Lost [fi] # http://thetvdb.com/?tab=series&id=73739&lid=11
    5 -> Lost [nl] # http://thetvdb.com/?tab=series&id=73739&lid=13
    6 -> Lost [de] # http://thetvdb.com/?tab=series&id=73739&lid=14
    Enter choice (first number, ? for help):    

To select the first result, enter `1` then `return`, to select the second enter `2` and so on. The link after `#` goes to the relevant [thetvdb.com][tvdb] page, which will contain information and images to help you select the correct series.

You can rename multiple files, or an entire directory by using the files or directories as arguments:

    $ tvnamer file1.avi file2.avi etc
    $ tvnamer .
    $ tvnamer /path/to/my/folder/
    $ tvnamer ./folder/1/ ./folder/2/

You can skip a specific file by entering `n` (no). If you enter `a` (always) `tvnamer` will rename the remaining files automatically. The suggested use of this is check the first few episodes are named correctly, then use `a` to rename the rest.

Note, tvnamer will only descend one level into directories unless the `-r` (or `--recursive`) flag is specified. For example, if you have the following directory structure:

    dir1/
        file1.avi
        dir2/
            file2.avi
            file3.avi

..then running `tvnamer dir1/` will only rename `file1.avi`, ignoring `dir2/` and its contents.

If you wish to rename all files (file1, file2 and file3), you would run:

    tvnamer --recursive dir1/

## Command line arguments

There are various flags you can use with `tvnamer`, run..

    tvnamer --help

..to see them, and a short description of each.

The most useful are most likely `--batch`, `--selectfirst` and `--always`:

`--selectfirst` will select the first series the search found, but will not automatically rename any episodes.

`--always` will ask you select the correct series, then automatically rename all files.

`--batch` will not prompt you for anything. It automatically selects the first series search result, and automatically rename all files (identical to using both `--selectfirst` and `--always`). Use carefully!

## Configs

One of the largest improvements in tvnamer v2 is the ability to have custom configuration. This allows you to customise behaviour without modifying the code, as was necessary with tvnamer v1.

To write the default configuration file, which is a good starting point for your modifications, simply run:

    tvnamer --save=./mytvnamerconfig.xml

To use your custom configuration, you must either specify the location using `tvnamer --config=/path/to/mytvnamerconfig.xml` or place the file at `~/.tvnamer.xml` (a file named `.tvnamer.xml` in your home directory)

If for example you wish to change the default language used, change the option `language` to another two-letter language code, such as `fr` for French.

`search_all_languages` makes tvnamer search for the series in all languages, and allows you to select the appropriate one. If this is False, tvnamer will search in the language specified in the option `language`

If you wish to change the output filename format, there are several options you must change:

- One for a file with an episode name (`filename_with_episode`). Example input: `Scrubs.s01e01.my.ep.name.avi`
- One for a file *without* an episode name (`filename_without_episode`). Example input: `AnUnknownShow.s01e01.avi`
- One for a filename with no season number, and an episode name (`filename_with_episode_no_season`). Example input: `Sid.The.Science.Kid.E11.avi`
- One for a filename with no season number, and no episode name (`filename_without_episode_no_season`). Example input: `AnUnknownShow.E24.avi`

This may seem like a lot, but they are mostly the same thing. One for a regular show without and without episode names, and one for a show without the concept of seasons

Say you want the format `Show Name 01x24 Episode Name.avi`, your `filename_with_episode` option would be:

    %(seriesname)s %(seasonno)02dx%(episode)s %(episodename)s%(ext)s

The formatting language used is Python's string formatting feature, which you can read about in the Python documentation, [6.6.2. String Formatting Operations](http://docs.python.org/library/stdtypes.html#string-formatting). Basically it's just `%()s` and the name element you wish to use between `( )`

Note `ext` contains the extension separator symbol, usually `.` - for example `.avi`

Then you need to make a few variants, one without the `episodename` section, and two without the `seasonno` option:

`filename_with_episode_no_season`:

    %(seriesname)s %(seasonno)02dx%(episode)s %(episodename)s%(ext)s

`filename_without_episode`:

    %(seriesname)s %(seasonno)02dx%(episode)s%(ext)s

`filename_without_episode_no_season`:

    %(seriesname)s %(episode)s%(ext)s

There are yet two more options you may want to change, `episode_single` and `episode_separator`

`episode_single` is the Python string formatting pattern used to format the episode number. By default it is `%02d` - this simply turns the number `1` to `01`, and keeps `24` as `24`

If you do not want any padding in your numbers, you could change this to `%d` - this would result in filenames such as `Show - [1x3] - Episode Name.avi` (or `Show 1x3 Episode Name.avi` using your custom name, as described above)

The `episode_separator` option is for multi-episode files. When multiple episodes are detected in one file (such as `Scrubs.s01e01e02.avi`), this string is used to join the episode numbers together. By default it is `-` which results in filenames such as `Scrubs - [01x01-02] - ... .avi`

You could change this to `e`, and by altering the `filename_*` options you could create filenames such as..

    Show - [s01e01e02] - Episode Name.avi

By default, tvnamer will sanitise files for the current operating system - either POSIX-compatible (OS X, Linux, FreeBSD) or Windows. You can force Windows compatible filenames by setting the option `windows_safe_filenames` to True

You can remove spaces in characters by adding a space to the option `custom_filename_character_blacklist` and changing the option `replace_blacklisted_characters_with` to `.`

`normalize_unicode_filenames` attempts to replace Unicode characters with their unaccented ASCII equivalent (`å` becomes `a` etc). Any untranslatable characters are removed.

`selectfirst` and `alwaysrename` mirror the command line arguments `--selectfirst` and `--always` - one automatically selects the first series search result, the other always renames files. Setting both to True is equivalent to `--batch`. `recursive` also mirrors the command line argument