#!/usr/bin/env python3

import json
import click
import sys


def drop_dm_tag(elem, doc):
    if isinstance(elem, Header):
       print(elem.content)


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


@click.command()
def main():
    """Parse json to remove :dm: tag
    """
    original = json.load(sys.stdin)
    header_lvls = find_header_lvls(original)
    dm_tags = find_dm_tags(original)
    click.echo(header_lvls)
    click.echo(dm_tags)
    # click.echo(json.dumps(original))


if __name__ == '__main__':
    main()
