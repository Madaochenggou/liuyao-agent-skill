"""Deterministic interfaces around a secure source of randomness."""
from dataclasses import dataclass
import secrets

VALUES = (6, 7, 8, 9)
COINS = ((0,0,0),(0,0,1),(0,1,0),(1,0,0),(0,1,1),(1,0,1),(1,1,0),(1,1,1))

def cast_single_line(source=None):
    bits = tuple(secrets.randbelow(2) if source is None else int(source()) for _ in range(3))
    value = 6 + sum(bits)
    return {'value': value, 'yin': value in (6,8), 'moving': value in (6,9), 'coins': list(bits)}

def cast_hexagram(method='coin', lines=None, raw_coins=None):
    if method == 'coin':
        out = [cast_single_line() for _ in range(6)]
    elif method in ('specified','manual'):
        out = parse_lines(lines, raw_coins=raw_coins)
    else: raise ValueError('method must be coin, manual, or specified')
    return {'method': method, 'algorithm_version': '1.0', 'lines': out, 'raw_lines': [x['value'] for x in out], 'raw_coins': [x['coins'] for x in out]}

def parse_lines(lines, raw_coins=None):
    if not isinstance(lines, (list,tuple)) or len(lines) != 6: raise ValueError('lines must contain exactly six values, 初爻到上爻')
    if any(type(x) is not int or x not in VALUES for x in lines): raise ValueError('each line must be integer 6, 7, 8, or 9')
    if raw_coins is not None and len(raw_coins) != 6: raise ValueError('raw_coins must contain six entries')
    return [{'value': v, 'yin': v in (6,8), 'moving': v in (6,9), 'coins': list(raw_coins[i]) if raw_coins else None} for i,v in enumerate(lines)]
