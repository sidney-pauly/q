import os

from q.utils.mesh import generate_materials_mapping
from q.utils.nam_file_reader import read_nam


def test_mesh_generator():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = read_nam(f'{dir_path}/test_data/icp.nam')

    mapping = generate_materials_mapping(config)

    assert len(mapping) == 11
