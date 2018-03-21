# -*- coding: utf-8 -*-

"""em: the technicolor cli emoji keyboard™

Usage:
  em <name>... [--no-copy]
  em -s <name>...

Options:
  -s            Search for emoji.
  -h --help     Show this screen.
  --no-copy     Does not copy emoji to clipboard.

Examples:

  $ em sparkle cake sparkles
  $ em heart

  $ em -s food

Notes:
  - If all names provided map to emojis, the resulting emojis will be
    automatically added to your clipboard.
  - ✨ 🍰 ✨  (sparkles cake sparkles)
"""

from __future__ import print_function

import argparse
import fnmatch
import itertools
import json
import os
import sys
from collections import defaultdict

import xerox

EMOJI_PATH = os.path.join(os.path.dirname(__file__), 'emojis.json')

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-s', dest='search')
parser.add_argument('-h', '--help', dest='help', action='store_true')
parser.add_argument('--no-copy', dest='nocopy', action='store_true')


def parse_emojis(filename=EMOJI_PATH):
    return json.load(open(filename))


def translate(lookup, code):
    output = []
    if code[0] == ':' and code[-1] == ':':
        code = code[1:-1]

    output.append(lookup.get(code, {'char': None})['char'])

    return output


def do_list(lookup, term):
    """Matches term glob against short-name."""

    space = lookup.keys()
    matches = fnmatch.filter(space, term)

    return [(m, translate(lookup, m)) for m in matches]


def do_find(lookup, term):
    """Matches term glob against short-name, keywords and categories."""

    space = defaultdict(list)

    for name in lookup.keys():
        space[name].append(name)

    try:
        iter_lookup = lookup.iteritems()  # Python 2
    except AttributeError:
        iter_lookup = lookup.items()  # Python 3

    for name, definition in iter_lookup:
        for keyword in definition['keywords']:
            space[keyword].append(name)
        space[definition['category']].append(name)
        space[name].append(name)

    matches = fnmatch.filter(space.keys(), '*' + term + '*')

    results = set()
    for match in matches:
        results.update(space[match])

    return [(r, translate(lookup, r)) for r in results]


def script_name():
    return os.path.basename(sys.argv[0])


def usage():
    print("""Usage:
  {0} <name>... [--no-copy]
  {0} -s <name>...""".format(script_name()))


def cli():
    # CLI argument parsing.
    args, emotes = parser.parse_known_args()

    if len(sys.argv) == 1:
        usage()
        return 0

    if args.help:
        print(__doc__)
        return 0

    # Cleanup input names, to humanize things.
    names = []
    for name in emotes:
        # Replace -/ /. with _.
        if name != '-1':
            name = name.replace('-', '_')
            name = name.replace(' ', '_')
            name = name.replace('.', '_')

        # Over-write original name.
        names.append(name)

    # Marker for if the given emoji isn't found.
    missing = False

    # Grab the lookup dictionary.
    lookup = parse_emojis()

    # Search mode.
    if args.search:

        # Lookup the search term.
        found = do_find(lookup, args.search)

        # print them to the screen.
        for (n, v) in found:
            # Some registered emoji have no value.
            try:
                print(u'{}  {}'.format(' '.join(v), n))
            # Sometimes, an emoji will have no value.
            except TypeError:
                pass

        return 0

    # Process the results.
    results = (translate(lookup, name) for name in names)
    results = list(itertools.chain.from_iterable(results))

    if None in results:
        no_copy = True
        missing = True
        results = (r for r in results if r)

    # Prepare the result strings.
    print_results = ' '.join(results)
    results = ''.join(results)

    # Copy the results (and say so!) to the clipboard.
    if not args.nocopy and not missing:
        xerox.copy(results)
        print(u'Copied! {}'.format(print_results))

    # Script-kiddies.
    else:
        print(print_results)

    return int(missing)

if __name__ == '__main__':
    sys.exit(cli())
