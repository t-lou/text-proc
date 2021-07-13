def handler_strip(strings: tuple) -> tuple:
    return tuple(string.strip() for string in strings)


def handler_remove_duplicate(strings: tuple) -> tuple:
    return tuple(sorted(set(strings), key=strings.index))


def handler_neighboring_duplicate(strings: tuple) -> tuple:
    return (strings[0],) + tuple(
        el for i, el in enumerate(strings[1:]) if el != strings[i])


def handler_upper(strings: tuple) -> tuple:
    return tuple(h.upper() for h in strings)


def handler_lower(strings: tuple) -> tuple:
    return tuple(h.lower() for h in strings)


def handler_reverse(strings: tuple) -> tuple:
    return tuple(h[::-1] for h in strings)


def handler_nonempty(strings: tuple) -> tuple:
    return tuple(h for h in strings if bool(h))


def handler_dec2hex(strings: tuple) -> tuple:
    return tuple(hex(int(h))[2:] for h in strings)


def handler_hex2dec(strings: tuple) -> tuple:
    return tuple(str(int(h, base=16)) for h in strings)


def handler_ascii2hex(strings: tuple) -> tuple:
    return tuple(''.join([hex(ord(c))[2:] for c in h]) for h in strings)


def handler_hex2ascii(strings: tuple) -> tuple:
    return tuple(''.join([
        chr(int(h[i:min(len(h), i + 2)], base=16)) for i in range(0, len(h), 2)
    ]) for h in strings)


def handler_zero_padding_left(strings: tuple) -> tuple:
    return tuple(h if len(h) % 2 == 0 else '0' + h for h in strings)


def handler_zero_padding_right(strings: tuple) -> tuple:
    return tuple(h if len(h) % 2 == 0 else h + '0' for h in strings)
