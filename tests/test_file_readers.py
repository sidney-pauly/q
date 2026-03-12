
import os
from q.utils.nam_file_reader import read_nam
from q.utils.pdt_file_reader import read_pdt

def test_read_nam():

    dir_path = os.path.dirname(os.path.realpath(__file__))

    data = read_nam(f'{dir_path}/test_data/icp.nam')

    assert len(data) == 21
    assert 'MATERIAL' in data
    assert len(data['MATERIAL']['CMETAL']) == 5
    assert isinstance(data['MATERIAL']['IMETALS'], int)
    assert isinstance(data['MATERIAL']['VRFM'][0], float) 

def test_read_movie_icp_1d():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data = read_pdt(f'{dir_path}/test_data/movie_icp_1d.pdt')

def test_read_movie_icp():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data = read_pdt(f'{dir_path}/test_data/movie_icp.pdt')

    print('x')
