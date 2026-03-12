from typing import Iterator


def skip_until(lines: Iterator[str], search_key: str, max_lines=1000):

    for i in range(0, max_lines):
        line = next(lines)

        if search_key in line:
            return line

    raise Exception(f'Could not find {search_key} in {max_lines} lines of file')
    
def skip_util_startswith(lines: Iterator[str], search_key: str, max_lines=1000):

    for i in range(0, max_lines):
        line = next(lines).strip()

        if line.startswith(search_key):
            return line

    raise Exception(f'Could not find {search_key} in {max_lines} lines of file')

def read_while_endswith(lines: Iterator[str], end: str):

    complete_string = ''

    while True:
        line = next(lines).rstrip()
        complete_string += line
        if not line.endswith(end):
            break

    return complete_string