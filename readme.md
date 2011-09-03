# `tvnamer`

`tvnamer` is a utility which to rename files from `some.show.s01e03.blah.abc.avi` to `Some Show - [01x03] - The Episode Name.avi` (by retrieving the episode name using data from [`tvdb_api`](http://github.com/dbr/tvdb_api))

## To install

You can easily install `tvnamer` via `easy_install`

    sudo easy_install tvnamer

This installs the `tvnamer` command-line tool (and the `tvdb_api` module as a requirement)

If you wish to install the latest (non-stable) development version from source, download the latest version of the code, either from <http://github.com/dbr/tvnamer/tarball/master> or by running:

    git clone git://github.com/dbr/tvnamer.git

..then `cd` into the directory, and run:

    sudo python setup.py install

Example terminal session (you can skip the `curl` line if you have already downloaded and extracted [the above link](http://github.com/dbr/tvnamer/tarball/master)):

    $ cd Downloads/
    $ curl -L http://github.com/dbr/tvnamer/tarball/master | gunzip - | tar -x -
    $ ls
    dbr-tvnamer-ce3ac8d/
    $ cd dbr-tvnamer-ce3ac8d/
    $ sudo python setup.py install
    Password:
    [...]
    Finished processing dependencies for tvnamer==2.0

## Improvements over v1

tvnamer v2 is a near-complete rewrite of the tvnamer released as part of `tvdb_api`. There are many improvements thanks to the improved code structure, but the most important are:

- Support for anime filenames, such as `[Shinsen-Subs] Beet - 19 [24DAB497].mkv`
- Support for multi-episode files, such as `scrubs.s01e23e24.avi`
- Custom configuration options (via a JSON config file) and improved command line argument handling
- Better support for Unicode filenames
- Support for moving files to specific location after renaming (`/media/tv/{series name}/season {seasonnumber}/` for example)

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

`--series-id` will allow you to use a specific ID from theTVdb. This can help with name detection issues.

## Configs

One of the largest improvements in tvnamer v2 is the ability to have custom configuration. This allows you to customise behaviour without modifying the code (as was necessary with tvnamer v1).

To write the default JSON configuration file, which is a good starting point for your modifications, simply run:

    tvnamer --save=./mytvnamerconfig.json

To use your custom configuration, you must either specify the location using `tvnamer --config=/path/to/mytvnamerconfig.json` or place the file at `~/.tvnamer.json` (a file named `.tvnamer.json` in your home directory)

**Important:** If tvnamer's default settings change and your saved config contains the old settings, you may experience strange behaviour or bugs (the config may contain a buggy `filename_patterns` regex, for example). It is recommended you remove config options you are not altering (particularly `filename_patterns`). If you experience any strangeness, try disabling your custom configuration (moving it away from `~/.tvnamer.json`)

If for example you wish to change the default language used to retrieve data, change the option `language` to another two-letter language code, such as `fr` for French. Your config file would look like:

    {
        "language": "fr"
    }

If `search_all_languages` is true, tvnamer will return multilingual search results. If false, it will return results only in the preferred language.

For an always up-to-date description of all config options, see the comments in [`config_defaults.py`](http://github.com/dbr/tvnamer/blob/master/tvnamer/config_defaults.py)

# Custom output filenames

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

The preferred way to replace spaces with another character is to use the custom replacements feature. For example, to replace spaces with `.` you would use the config:

    {
        "output_filename_replacements": [
            {"is_regex": true,
            "match": "[ ]",
            "replacement": "."}
        ]
    }


You can also remove spaces in characters by adding a space to the option `custom_filename_character_blacklist` and changing the option `replace_blacklisted_characters_with` to `.`

`normalize_unicode_filenames` attempts to replace Unicode characters with their unaccented ASCII equivalent (`å` becomes `a` etc). Any untranslatable characters are removed.

`selectfirst` and `always_rename` mirror the command line arguments `--selectfirst` and `--always` - one automatically selects the first series search result, the other always renames files. Setting both to True is equivalent to `--batch`. `recursive` also mirrors the command line argument

# Custom filename parsing pattern

`tvnamer` comes with a set of patterns to parse a majority of common (and many uncommon) TV episode file names. If these don't parse your files, you can write custom patterns.

The patterns are regular expressions, compiled with the [`re.VERBOSE` flag](http://docs.python.org/library/re.html#re.VERBOSE). Each pattern must contain several named groups.

Named groups are like regular groups, but the group starts with `?P<thegroupname>`. For example:

    (?P<seriesname>.+?)

All patterns must contain a named group `seriesname` - this is of course the name of the show the filename contains.

Optionally you can parse a season number using the group `seasonnumber`. If this group is not specified, it will search for the episode(s) in season 1 (following the [thetvdb.com][tvdb] convention)

You must also match an episode number group. For simple, single episode files use the group `episodenumber`

If you wish to match multiple episodes in one file, there two options:

- `episodenumber1` `episodenumber2` etc - match any number of episode numbers (can be non-consecutive), or..
- Two groups, `episodenumberstart` and `episodenumberend` - you match the first and last numbers in the filename. If the start number is 2, and the end number is 5, the file contains episodes [2, 3, 4, 5].
