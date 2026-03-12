from typing import Iterable, Iterator
import numpy as np
import re
from q.utils.file_read_helpers import read_while_endswith, skip_until

ZONE_REGEX = re.compile(r'(\w+)\s*=\s*((\w+)|"[\w\s=\-\^\$,]+|\([\w\s=\-\^\$,]+\))')



def read_pdt(path: str):

    with open(path, 'r') as f:
        return parse_pdt(f)

def parse_pdt(lines: Iterator[str]):

    raw_values = None

    try:

        line = skip_until(lines, 'VARIABLES=')
        line = line.replace('VARIABLES=', '')
        vars_str = line + read_while_endswith(lines, ',')
        vars = parse_vars(vars_str)

        zone_info = _read_until_zone(lines)

        zone_infos = [zone_info]
        raw_values = dict((v, list[np.ndarray]()) for v in vars)

        frame = 0
        while True:

            shape = get_shape_form_zone_info(zone_infos[-1])
            blacklist = set(get_blacklist_form_zone_info(zone_infos[-1]))

            k = 0
            for v in vars:
                k += 1

                if k in blacklist:
                    continue

                if len(shape) == 1:
                    cur_arr = np.zeros(shape, dtype=float)
                    i = 0
                    while i < shape[0]:
                        l = next(lines)
                        for x in l.strip().split(' '):
                            if x != '':
                                cur_arr[i] = float(x)
                                i+=1
                elif len(shape) == 2:  
                    cur_arr = np.zeros((shape[1], shape[0]), dtype=float)
                    i = 0
                    j = 0
                    while j < shape[1]:
                        l = next(lines)
                        for x in l.strip().split(' '):
                            if x != '':
                                cur_arr[j, i] = float(x)
                                i+=1
                                if i >= shape[0]:
                                    i = 0
                                    j +=1
                else:
                    raise NotImplementedError()
                        
                raw_values[v].append(cur_arr)

            zone_infos.append(_read_until_zone(lines))
            frame += 1

    except StopIteration:

        if raw_values is None:
            raise Exception('Error reading from file: EOF reached before full info could be read')

        # Stack values where needed
        return dict((x[0], x[1][0] if len(x[1]) < 2 else np.stack(x[1])) for x in raw_values.items())
    
        
def _read_until_zone(lines):
    line = skip_until(lines, 'ZONE', max_lines=100000)
    line = line.replace('ZONE', '')
    zone_info_str = line.rstrip() + read_while_endswith(lines, ',')
    zone_info = parse_zone_info(zone_info_str)
    return zone_info

def parse_vars(vars_str: str):
    return [v for v in (x.replace('"', '').strip() for x in vars_str.split(',')) if v != '']

def parse_zone_info(zone_info: str):
    return dict((x[0], x[1]) for x in  ZONE_REGEX.findall(zone_info))
  
def get_shape_form_zone_info(zone_info: dict):

    cols = list()

    if 'I' in zone_info:
        cols.append(int(zone_info['I']))
    if 'J' in zone_info:
        cols.append(int(zone_info['J']))

    return tuple(cols)

def get_blacklist_form_zone_info(zone_info: dict):

    if 'D' not in zone_info:
        return list()
    
    return list(int(x) for x in zone_info['D'][1:-1].split(',')) # Remove brackets, split by "," and parse