import json
import os

import requests

from Entities.Rule import Rule
from utils.casting import bin_to_int


def get_rule(b: str) -> Rule:
    """Parses the Rule ID of the given binary string, assuming that it is located in the leftmost bits."""
    first_byte = b[:8]
    rule_id = first_byte[:3]
    option = 0
    if is_monochar(rule_id, '1'):
        rule_id = first_byte[:6]
        option = 1
        if is_monochar(rule_id, '1'):
            option = 2
            rule_id = first_byte[:8]
    return Rule(bin_to_int(rule_id), option)


def insert_index(ls, pos, elmt):
    while len(ls) < pos:
        ls.append([])
    ls.insert(pos, elmt)


def replace_bit(string, position, value):
    return '%s%s%s' % (string[:position], value, string[position + 1:])


def find(string, character):
    return [i for i, ltr in enumerate(string) if ltr == character]


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, 'big')


def is_monochar(s, char=None):
    if char is not None:
        return len(set(s)) == 1 and s[0] == char
    return len(set(s)) == 1


def contains_different_from(lst, element):
    if len(lst) == 0:
        return False
    if element in lst:
        res = False
        for e in lst:
            if e != element:
                res = True
    else:
        res = True
    return res


def send_ack(request_dict, ack):
    print(f"ack string -> {ack.to_string()}")
    response_dict = {request_dict["device"]: {'downlinkData': ack.to_bytes().hex()}}
    response_json = json.dumps(response_dict)
    print(f"response_json -> {response_json}")
    return response_json


def generate_packet(byte_size):
    if not os.path.isfile(f"Packets/{byte_size}"):
        s = '0'
        i = 0
        while len(s) < byte_size:
            i = (i + 1) % 10
            s += str(i)
        with open(f"Packets/{byte_size}", 'w') as f:
            f.write(s)


def ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return f'{n}{suffix}'


def start_request(url, body):
    try:
        _ = requests.post(url=url,
                          json=body,
                          timeout=0.1)
    except requests.exceptions.ReadTimeout:
        pass
