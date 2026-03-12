
import numpy as np

def parse_mesh_file(path):

    with open(path, 'r') as f:

        for i in range(0, 100):

            line = f.readline()

            if '*' in line:
                break

        skip = True

        mesh_lines = list[str]()

        while True:

            line = f.readline()

            do_break = not skip and line.strip().startswith('#')
            skip = False

            line = line.replace('#', '').strip()

            mesh_lines.append(line)

            if do_break:
                break

        i_size = len(mesh_lines[0])
        j_size = len(mesh_lines)

        np_arr = np.full((j_size, i_size), '')

        j = 0
        for l in mesh_lines:
            i = 0
            for c in l:
                np_arr[j_size-j-1, i] = c
                i += 1
            j += 1

        return np_arr
