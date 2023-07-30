#!/usr/bin/env python3

import json
import click
import sys


def find_header_lvls(content):
    header_lvls = []
    for block in content['blocks']:
        if block['t'] == 'Header':
            header_lvls.append(block['c'][0])
        else:
            header_lvls.append(0)
    return header_lvls


def find_dm_tags(content):
    dm_tags = []
    for block in content['blocks']:
        if block['t'] == 'Header':
            c = block['c'][2]
            c = [i['c'] for i in c if 'c' in i]
            dm_tags.append(':dm:' in c)
        else:
            dm_tags.append(False)
    return dm_tags


def find_next_header(header_lvls, idx):
    """Find the next header at equivalent or higher level to specified header.

    That is, if you were fold the specified header and its subheaders, what
    would be the next visible section

    """
    idx_header = header_lvls[idx]
    if idx_header == 0:
        raise ValueError("Header level must be >= 1, but got 0!")
    for i in header_lvls[idx+1:]:
        if i >= idx_header:
            break
        # if we're at the end of the list, the logic doesn't quite work, so we
        # also need to skip there
        elif idx+1+i == len(header_lvls)-1:
            i += 1
    return idx+1+i


@click.command()
@click.option("--action", help="Whether to just strip :dm: from the header text ('remove tag') or to hide the corresponding section and all its subsections ('hide section')",
              default='hide section', show_default=True)
def main(action='hide section'):

    """Parse json to remove :dm: tag and send back to stdout

    Accepts input from stdin (i.e., piping), so the intended use case is:

    > pandoc file.md -t json | python filter_dm.py | pandoc -f json -t gfm -o filtered.md

    """
    if action not in ['hide section', 'remove tag']:
        raise ValueError(f"action must be either 'hide section' or 'remove tag', but got {action}")
    original = json.load(sys.stdin)
    header_lvls = find_header_lvls(original)
    dm_tags = find_dm_tags(original)
    filtered = {k: v for k, v in original.items() if k != 'blocks'}
    filtered['blocks'] = []
    skip_to = 0
    for i, (bl, dm) in enumerate(zip(original['blocks'], dm_tags)):
        if dm:
            skip_to = find_next_header(header_lvls, i)
        if skip_to <= i:
            filtered['blocks'].append(bl)
    click.echo(json.dumps(filtered))


if __name__ == '__main__':
    main()
