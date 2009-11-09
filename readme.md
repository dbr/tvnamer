# `tvnamer`

`tvnamer` is a utility which uses [`tvdb_api`](http://github.com/dbr/tvdb_api) to rename files from `some.show.s01e03.blah.abc.avi` to `Some Show - [01x03] - The Episode Name.avi` (by retrieving the episode name using `tvdb_api`)

## To install

You can easily install `tvnamer` via `easy_install`

    easy_install tvnamer

This installs the `tvnamer` command-line tool (and the `tvdb_api` module as a requirement)

You may need to use sudo, depending on your setup:

    sudo easy_install tvnamer

## Basic usage

From the command line, simply run:

    tvnamer the.file.s01e01.avi

For example:

    $ tvnamer scrubs.s01e01.avi
    ####################
    # Starting tvnamer
    # Processing 1 files
    # ..got tvdb mirrors
    # Starting to process files
    ####################
    # Processing scrubs (season: 1, episode 1)
    TVDB Search Results:
    1 -> Scrubs # http://thetvdb.com/?tab=series&id=76156
    Automatically selecting only result
    ####################
    Old name: scrubs.s01e01.avi
    New name: Scrubs - [01x01] - My First Day.avi
    Rename?
    ([y]/n/a/q)

Enter `y` then press `return` and the file will be renamed to "Scrubs - [01x01] - My First Day.avi". You can also simply press `return` to select the default option, denoted by the surrounding `[]`

If there are multiple shows with the same (or similar) names, you will be asked to select the correct one - "Lost" is a good example of this:

    $ python tvnamer.py lost.s01e01.avi
    ####################
    # Starting tvnamer
    # Processing 1 files
    # ..got tvdb mirrors
    # Starting to process files
    ####################
    # Processing lost (season: 1, episode 1)
    TVDB Search Results:
    1 -> Lost # http://thetvdb.com/?tab=series&id=73739
    2 -> Lost in Space # http://thetvdb.com/?tab=series&id=72923
    [...]
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

## Advanced usage

There are various flags you can use with `tvnamer`, run..

    tvnamer --help

..to see them, and a short description of each.

The most interesting are most likely `--batch`, `--selectfirst` and `--always`:

`--selectfirst` will select the first series the search found, but will not automatically rename any episodes.

`--always` will ask you select the correct series, then automatically rename all files.

`--batch` will not prompt you for anything. It automatically selects the first series search result, and automatically rename all files. Use carefully!
