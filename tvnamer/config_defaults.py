#!/usr/bin/env python

"""Holds default config values
"""

defaults = {
    # Select first series search result
    'select_first': False,

    # Always rename files
    'always_rename': False,

    # Batch (same as select_first and always_rename)
    'batch': False,

    # Fail if error finding show data (thetvdb.com is down etc)
    # Only functions when always_rename is True
    'skip_file_on_error': True,
    
    # Fail if error finding show data (thetvdb.com is down etc)
    # Changes the default behaviour for skip_file_on_error from skip to exit
    'skip_behaviour': 'skip',

    # Forcefully overwrite existing files when renaming or
    # moving. This potentially destroys the old file. Default is False
    'overwrite_destination_on_rename': False,
    'overwrite_destination_on_move': False,

    # Verbose mode (debugging info)
    'verbose': False,

    # Dry-run mode (do nothing)
    'dry_run': False,

    # Recurse more than one level into folders. When False, only
    # desends one level.
    'recursive': False,

    # When non-empty, only look for files with this extension.
    # No leading dot, for example: ['avi', 'mkv', 'mp4']
    'valid_extensions': [],

    # Pattern for splitting filenames into basename and extension.
    # Useful for matching subtitles with language codes, for example
    # "extension_pattern": "(\.(eng|cze))?(\.[a-zA-Z0-9]+)$" will split "foo.eng.srt"
    # into "foo" and ".eng.srt".
    # Note that extensions still pass 'valid_extensions' filter, '.eng.srt' passes
    # when 'srt' is specified in 'valid_extensions'.
    'extension_pattern': '(\.[a-zA-Z0-9]+)$',

    # When non-empty, filter out filenames that match these expressions. Either simple
    # matches or regexs can be used. The following are near enough equivalent:
    # [{"is_regex": true, "match": ".*sample.*"}, {"is_regex": false, "match": "sample"}]
    'filename_blacklist': [],

    # Force Windows safe filenames (always True on Windows)
    'windows_safe_filenames': False,

    # Replace accented unicode characters with ASCII equivalents,
    # removing characters than can't be translated.
    'normalize_unicode_filenames': False,

    # Convert output filenames to lower case (applied after replacements)
    'lowercase_filename': False,

    # Convert output filenames to 'Title Case' (applied after replacements)
    'titlecase_filename': False,

    # Extra characters to consider invalid in output filenames (which are
    # replaced by the character in replace_invalid_characters_with)
    'custom_filename_character_blacklist': '',

    # Replacement characters for invalid filename characters
    'replace_invalid_characters_with': '_',

    # Replacements performed on input file before parsing.
    'input_filename_replacements': [
    ],

    # Replacements performed on files after the new name is generated.
    'output_filename_replacements': [
    ],

    # Replacements are performed on the full path used by move_files feature,
    # including the filename
    'move_files_fullpath_replacements': [
    ],

    # Language to (try) and retrieve episode data in
    'language': 'en',

    # Search in all possible languages
    'search_all_languages': True,

    # Move renamed files to directory?
    'move_files_enable': False,

    # Separate confirmation of moving or copying renamed file?  If
    # False, will move files when renaming. In batch mode, will never
    # prompt.
    'move_files_confirmation': True,

    # If true, convert the variable/dynamic parts of the destination
    # to lower case. Does not affect the static parts; for example,
    # if move_files_destination is set to
    # '/Foo/Bar/%(seriesname)s/Season %(seasonnumber)d'
    # then only the series name will be converted to lower case.
    'move_files_lowercase_destination': False,

    # If True, the destination path includes the destination filename,
    # for example: '/example/tv/%(seriesname)s/season %(seasonnumber)d/%(originalfilename)'
    'move_files_destination_is_filepath': False,

    # Destination to move files to. Trailing slash is not necessary.
    # Use forward slashes, even on Windows. Realtive paths are realtive to
    # the existing file's path (not current working dir). A value of '.' will
    # not move the file anywhere.
    #
    # Use Python's string formatting to add dynamic paths. Available variables:
    # - %(seriesname)s
    # - %(seasonnumber)d
    # - %(episodenumbers)s (Note: this is a string, formatted with config
    #                       variable episode_single and joined with episode_separator)
    'move_files_destination': '.',

    # Same as above, only for date-numbered episodes. The following
    # variables are available:
    # - %(seriesname)s
    # - %(year)s
    # - %(month)s
    # - %(day)s
    'move_files_destination_date': '.',

    # Force the move-files feature to always move the file.
    #
    # If False, when a file is moved between partitions (or from a
    # network volume), the original is left untouched (i.e it is
    # copied).  If True, this will delete the file from the original
    # volume, after the copy has complete.
    'always_move': False,

    # Whenever a file is moved leave a symlink to the new file behind, named
    # after the original file.
    'leave_symlink': False,

    # Allow user to copy files to specified move location without renaming files.
    'move_files_only': False,

    # Patterns to parse input filenames with
    'filename_patterns': [
        # [group] Show - 01-02 [crc]
        '''^\[(?P<group>.+?)\][ ]?               # group name, captured for [#100]
        (?P<seriesname>.*?)[ ]?[-_][ ]?          # show name, padding, spaces?
        (?P<episodenumberstart>\d+)              # first episode number
        ([-_]\d+)*                               # optional repeating episodes
        [-_](?P<episodenumberend>\d+)            # last episode number
        (?=                                      # Optional group for crc value (non-capturing)
          .*                                     # padding
          \[(?P<crc>.+?)\]                       # CRC value
        )?                                       # End optional crc group
        [^\/]*$''',

        # [group] Show - 01 [crc]
        '''^\[(?P<group>.+?)\][ ]?               # group name, captured for [#100]
        (?P<seriesname>.*)                       # show name
        [ ]?[-_][ ]?                             # padding and seperator
        (?P<episodenumber>\d+)                   # episode number
        (?=                                      # Optional group for crc value (non-capturing)
          .*                                     # padding
          \[(?P<crc>.+?)\]                       # CRC value
        )?                                       # End optional crc group
        [^\/]*$''',

        # foo s01e23 s01e24 s01e25 *
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        ([\.\- ]+                                # separator
        [Ss](?P=seasonnumber)                    # s01
        [\.\- ]?                                 # separator
        [Ee][0-9]+)*                             # e24 etc (middle groups)
        ([\.\- ]+                                # separator
        [Ss](?P=seasonnumber)                    # last s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberend>[0-9]+))        # final episode number
        [^\/]*$''',

        # foo.s01e23e24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        ([\.\- ]?                                # separator
        [Ee][0-9]+)*                             # e24e25 etc
        [\.\- ]?[Ee](?P<episodenumberend>[0-9]+) # final episode num
        [^\/]*$''',

        # foo.1x23 1x24 1x25
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # first season number (1)
        [xX](?P<episodenumberstart>[0-9]+)       # first episode (x23)
        ([ \._\-]+                               # separator
        (?P=seasonnumber)                        # more season numbers (1)
        [xX][0-9]+)*                             # more episode numbers (x24)
        ([ \._\-]+                               # separator
        (?P=seasonnumber)                        # last season number (1)
        [xX](?P<episodenumberend>[0-9]+))        # last episode number (x25)
        [^\/]*$''',

        # foo.1x23x24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # 1
        [xX](?P<episodenumberstart>[0-9]+)       # first x23
        ([xX][0-9]+)*                            # x24x25 etc
        [xX](?P<episodenumberend>[0-9]+)         # final episode num
        [^\/]*$''',

        # foo.s01e23-24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        (                                        # -24 etc
             [\-]
             [Ee]?[0-9]+
        )*
             [\-]                                # separator
             [Ee]?(?P<episodenumberend>[0-9]+)   # final episode num
        [\.\- ]                                  # must have a separator (prevents s01e01-720p from being 720 episodes)
        [^\/]*$''',

        # foo.1x23-24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # 1
        [xX](?P<episodenumberstart>[0-9]+)       # first x23
        (                                        # -24 etc
             [\-+][0-9]+
        )*
             [\-+]                               # separator
             (?P<episodenumberend>[0-9]+)        # final episode num
        ([\.\-+ ].*                              # must have a separator (prevents 1x01-720p from being 720 episodes)
        |
        $)''',

        # foo.[1x09-11]*
        '''^(?P<seriesname>.+?)[ \._\-]          # show name and padding
        \[                                       # [
            ?(?P<seasonnumber>[0-9]+)            # season
        [xX]                                     # x
            (?P<episodenumberstart>[0-9]+)       # episode
            ([\-+] [0-9]+)*
        [\-+]                                    # -
            (?P<episodenumberend>[0-9]+)         # episode
        \]                                       # \]
        [^\\/]*$''',

        # foo - [012]
        '''^((?P<seriesname>.+?)[ \._\-])?       # show name and padding
        \[                                       # [ not optional (or too ambigious)
        (?P<episodenumber>[0-9]+)                # episode
        \]                                       # ]
        [^\\/]*$''',
        # foo.s0101, foo.0201
        '''^(?P<seriesname>.+?)[ \._\-]
        [Ss](?P<seasonnumber>[0-9]{2})
        [\.\- ]?
        (?P<episodenumber>[0-9]{2})
        [^0-9]*$''',

        # foo.1x09*
        '''^((?P<seriesname>.+?)[ \._\-])?       # show name and padding
        \[?                                      # [ optional
        (?P<seasonnumber>[0-9]+)                 # season
        [xX]                                     # x
        (?P<episodenumber>[0-9]+)                # episode
        \]?                                      # ] optional
        [^\\/]*$''',

        # foo.s01.e01, foo.s01_e01, "foo.s01 - e01"
        '''^((?P<seriesname>.+?)[ \._\-])?
        \[?
        [Ss](?P<seasonnumber>[0-9]+)[ ]?[\._\- ]?[ ]?
        [Ee]?(?P<episodenumber>[0-9]+)
        \]?
        [^\\/]*$''',

        # foo.2010.01.02.etc
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<year>\d{4})                          # year
        [ \._\-]                                 # separator
        (?P<month>\d{2})                         # month
        [ \._\-]                                 # separator
        (?P<day>\d{2})                           # day
        [^\/]*$''',

        # foo - [01.09]
        '''^((?P<seriesname>.+?))                # show name
        [ \._\-]?                                # padding
        \[                                       # [
        (?P<seasonnumber>[0-9]+?)                # season
        [.]                                      # .
        (?P<episodenumber>[0-9]+?)               # episode
        \]                                       # ]
        [ \._\-]?                                # padding
        [^\\/]*$''',

        # Foo - S2 E 02 - etc
        '''^(?P<seriesname>.+?)[ ]?[ \._\-][ ]?
        [Ss](?P<seasonnumber>[0-9]+)[\.\- ]?
        [Ee]?[ ]?(?P<episodenumber>[0-9]+)
        [^\\/]*$''',

        # Show - Episode 9999 [S 12 - Ep 131] - etc
        '''
        (?P<seriesname>.+)                       # Showname
        [ ]-[ ]                                  # -
        [Ee]pisode[ ]\d+                         # Episode 1234 (ignored)
        [ ]
        \[                                       # [
        [sS][ ]?(?P<seasonnumber>\d+)            # s 12
        ([ ]|[ ]-[ ]|-)                          # space, or -
        ([eE]|[eE]p)[ ]?(?P<episodenumber>\d+)   # e or ep 12
        \]                                       # ]
        .*$                                      # rest of file
        ''',

        # show name 2 of 6 - blah
        '''^(?P<seriesname>.+?)                  # Show name
        [ \._\-]                                 # Padding
        (?P<episodenumber>[0-9]+)                # 2
        of                                       # of
        [ \._\-]?                                # Padding
        \d+                                      # 6
        ([\._ -]|$|[^\\/]*$)                     # More padding, then anything
        ''',

        # Show.Name.Part.1.and.Part.2
        '''^(?i)
        (?P<seriesname>.+?)                        # Show name
        [ \._\-]                                   # Padding
        (?:part|pt)?[\._ -]
        (?P<episodenumberstart>[0-9]+)             # Part 1
        (?:
          [ \._-](?:and|&|to)                        # and
          [ \._-](?:part|pt)?                        # Part 2
          [ \._-](?:[0-9]+))*                        # (middle group, optional, repeating)
        [ \._-](?:and|&|to)                        # and
        [ \._-]?(?:part|pt)?                       # Part 3
        [ \._-](?P<episodenumberend>[0-9]+)        # last episode number, save it
        [\._ -][^\\/]*$                            # More padding, then anything
        ''',

        # Show.Name.Part1
        '''^(?P<seriesname>.+?)                  # Show name\n
        [ \\._\\-]                               # Padding\n
        [Pp]art[ ](?P<episodenumber>[0-9]+)      # Part 1\n
        [\\._ -][^\\/]*$                         # More padding, then anything\n
        ''',

        # show name Season 01 Episode 20
        '''^(?P<seriesname>.+?)[ ]?               # Show name
        [Ss]eason[ ]?(?P<seasonnumber>[0-9]+)[ ]? # Season 1
        [Ee]pisode[ ]?(?P<episodenumber>[0-9]+)   # Episode 20
        [^\\/]*$''',                              # Anything

        # foo.103*
        '''^(?P<seriesname>.+)[ \._\-]
        (?P<seasonnumber>[0-9]{1})
        (?P<episodenumber>[0-9]{2})
        [\._ -][^\\/]*$''',

        # foo.0103*
        '''^(?P<seriesname>.+)[ \._\-]
        (?P<seasonnumber>[0-9]{2})
        (?P<episodenumber>[0-9]{2,3})
        [\._ -][^\\/]*$''',

        # show.name.e123.abc
        '''^(?P<seriesname>.+?)                  # Show name
        [ \._\-]                                 # Padding
        [Ee](?P<episodenumber>[0-9]+)            # E123
        [\._ -][^\\/]*$                          # More padding, then anything
        ''',
    ],

    # Formats for renamed files. Variations for with/without episode,
    # and with/without season number.
    'filename_with_episode':
     '%(seriesname)s - [%(seasonnumber)02dx%(episode)s] - %(episodename)s%(ext)s',
    'filename_without_episode':
     '%(seriesname)s - [%(seasonnumber)02dx%(episode)s]%(ext)s',

    # Seasonless filenames.
    'filename_with_episode_no_season':
      '%(seriesname)s - [%(episode)s] - %(episodename)s%(ext)s',
    'filename_without_episode_no_season':
     '%(seriesname)s - [%(episode)s]%(ext)s',

    # Date based filenames.
    # Series - [2012-01-24] - Ep name.ext
    'filename_with_date_and_episode':
     '%(seriesname)s - [%(episode)s] - %(episodename)s%(ext)s',
    'filename_with_date_without_episode':
     '%(seriesname)s - [%(episode)s]%(ext)s',

    # Anime filenames.
    # [AGroup] Series - 02 - Some Ep Name [CRC1234].ext
    # [AGroup] Series - 02 [CRC1234].ext
    'filename_anime_with_episode':
     '[%(group)s] %(seriesname)s - %(episode)s - %(episodename)s [%(crc)s]%(ext)s',

    'filename_anime_without_episode':
     '[%(group)s] %(seriesname)s - %(episode)s [%(crc)s]%(ext)s',

    # Same, without CRC value
    'filename_anime_with_episode_without_crc':
     '[%(group)s] %(seriesname)s - %(episode)s - %(episodename)s%(ext)s',

    'filename_anime_without_episode_without_crc':
     '[%(group)s] %(seriesname)s - %(episode)s%(ext)s',



    # Used to join multiple episode names together (only when episode names are different)
    'multiep_join_name_with': ', ',

    # Format for multi-episode names (only when episode names are the same)
    # Formats mapping key 'episodename' (used in variables 'filename_with_episode' etc.)
    'multiep_format': '%(epname)s (%(episodemin)s-%(episodemax)s)',

    # Format for numbers (python string format), %02d does 2-digit padding, %d will cause no padding
    'episode_single': '%02d',

    # String to join multiple numbers in mapping key 'episode' (used in variables 'filename_with_episode' etc.)
    'episode_separator': '-',

    # Series ID to use instead of searching if the value is set
    #'series_id': None,

    # Forced Name to use
    #'forced_name': None,

    # replace series names before/after passing to TVDB
    # input replacements are regular expressions for the series as parsed from
    # filenames, for instance adding or removing the year, or expanding abbreviations
    'input_series_replacements': {},

    # output replacements are for transforms of the TVDB series names
    # since these are perfectly predictable, they are simple strings
    # not regular expressions
    'output_series_replacements': {},

    # use dvd episode order of tvdb, instead of aired order
    'order': 'aired',
}
