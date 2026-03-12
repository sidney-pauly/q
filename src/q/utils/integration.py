import math
import numpy as np

def integrate_cylindrical_volume(r, z, v):

    dH = z[1, 0] - z[0, 0]
    dA = np.pow(r[:, 1:], 2) - np.pow(r[:, :-1], 2)

    volume_elements = math.pi * dH * dA * v[:, :-1]

    return np.sum(volume_elements)

def integrate_element_wise(r, z, v):
    dA = np.pow(r[z, 1:], 2) - np.pow(r[z, :-1], 2)
    area_elements = math.pi * dA * v[z, :-1]
    return area_elements

def integrate_disk(r, z, v):

    area_elements = integrate_element_wise(r, z, v)

    return np.sum(area_elements)