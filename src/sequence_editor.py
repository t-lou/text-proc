import typing


def transform(strings: tuple, callback: typing.Callable[[str], str]) -> tuple:
    return tuple(callback(string) if bool(string) else '' for string in strings)


def handler_strip(strings: tuple) -> tuple:
    return transform(strings, lambda s: s.strip())


def handler_remove_duplicate(strings: tuple) -> tuple:
    return tuple(sorted(set(strings), key=strings.index))


def handler_neighboring_duplicate(strings: tuple) -> tuple:
    return (strings[0],) + tuple(
        el for i, el in enumerate(strings[1:]) if el != strings[i])


def handler_upper(strings: tuple) -> tuple:
    return transform(strings, lambda s: s.upper())


def handler_lower(strings: tuple) -> tuple:
    return transform(strings, lambda s: s.lower())


def handler_reverse(strings: tuple) -> tuple:
    return transform(strings, lambda s: s[::-1])


def handler_nonempty(strings: tuple) -> tuple:
    return tuple(h for h in strings if bool(h))


def handler_dec2hex(strings: tuple) -> tuple:
    return transform(strings, lambda s: hex(int(s))[2:])


def handler_hex2dec(strings: tuple) -> tuple:
    return transform(strings, lambda s: str(int(s, base=16)))


def handler_ascii2hex(strings: tuple) -> tuple:
    return transform(strings, lambda s: ''.join([hex(ord(c))[2:] for c in s]))


def handler_hex2ascii(strings: tuple) -> tuple:
    cb = lambda s: ''.join([
        chr(int(s[i:min(len(s), i + 2)], base=16)) for i in range(0, len(s), 2)
    ])
    return transform(strings, cb)


def handler_zero_padding_left(strings: tuple) -> tuple:
    return transform(strings, lambda s: s if len(s) % 2 == 0 else '0' + s)


def handler_zero_padding_right(strings: tuple) -> tuple:
    return transform(strings, lambda s: s if len(s) % 2 == 0 else s + '0')
