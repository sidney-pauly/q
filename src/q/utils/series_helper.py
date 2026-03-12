

from typing import Iterable

def get_vector_uv_pairs(values: Iterable[str]):
    v_set = set()

    for v in values:
        if 'Z' in v:
            v_set.add(v)

    pairs = list[tuple[str, str, str]]()

    for v in values:
        if 'R' not in v:
            continue

        i = 0
        for c in v:
            if c == 'R':
                c = v[:i] + 'Z' + (v[i+1:] if i < len(v)-1 else '')
                display_name = v[:i] + (v[i+1:] if i < len(v)-1 else '')
                if c in v_set:
                    pairs.append((v, c, display_name))
            i +=1
    return pairs
