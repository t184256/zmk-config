#!/usr/bin/env python
"""Generate czech.dtsi / russian.dtsi / ..."""

import sys


def nibbletokey(nibble):
    return f'N{nibble}' if nibble in '1234567890' else f' {nibble.upper()}'


def genseq(char):
    return [nibbletokey(n) for n in f'{ord(char):04x}']


def genline(name, char_lower, char_upper):
    # TODO: 0 and non0 variants
    return (f'U8('
            f'{name}, '
            f'{', '.join(genseq(char_lower) + genseq(char_upper))})'
            f'  // {char_lower} / {char_upper}')


if __name__ == '__main__':
    print('#include "unicode.dtsi"')
    print()
    for line in sys.stdin.readlines():
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        match line.split():
            case [name, char_lower, char_higher]:
                print(genline(name, char_lower, char_higher))
            case [name, char_lower]:
                print(genline(name, char_lower, char_lower.upper()))
            case _:
                raise RuntimeError(f'malformed line `{line}`')
