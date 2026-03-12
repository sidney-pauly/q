import math
from typing import Any, Iterable, Iterator
import re
from q.utils.file_read_helpers import skip_util_startswith

DATA_IN_REGEX = re.compile(r'\$DATAIN_([\w]+)')
ENTRY_REGEX = re.compile(r'(\w+)\s*=(.*)')
VALUE_REGEX = re.compile(r'\"[\w\.\-]*\"|\'[\w\.\-]*\'|[\w\.\-]+')

def _read_until_end(lines: Iterator[str]):

    while True:
        line = next(lines).strip()
        line = line.split('!')[0] # remove comments
        if line.startswith('$END'):
            break
        yield line

def _parse_value(v_str: str):

    v_str = v_str.strip()

    if v_str.startswith("'"):
        return v_str.replace("'", '')
    if v_str.startswith('"'):
        return v_str.replace('"', '')
    
    try:
        as_num = float(v_str)
    except:
        return v_str

    if math.isnan(as_num):
        return v_str

    # check if its an int
    if 'e' not in v_str and 'E' not in v_str and '.' not in v_str:
        as_num = int(v_str)

    return as_num


def read_nam(path: str):
    with open(path) as f:
        return parse_nam(f)

def parse_nam(lines: Iterator[str]):

    data = dict[str, dict[str, Any]]()

    try:

        while True:
            data_in = skip_util_startswith(lines, '$DATAIN', 10000)
            
            data_in_match = DATA_IN_REGEX.search(data_in)                
            section_name = data_in_match.groups()[0] if data_in_match is not None else ''

            cur_section = dict[str, Any]()

            for l in _read_until_end(lines):
                match = ENTRY_REGEX.search(l)
                if match is None:
                    continue

                g = match.groups()

                values = VALUE_REGEX.findall(g[1])

                if len(values) > 1:
                    cur_section[g[0]] = tuple(_parse_value(v) for v in values)
                elif len(values) > 0:
                    cur_section[g[0]] = _parse_value(values[0])
                else:
                    cur_section[g[0]] = None

            data[section_name] = cur_section
                    
    except StopIteration:

        return data