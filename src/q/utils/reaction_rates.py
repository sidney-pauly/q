import numpy as np
from q.utils.natural_constants import KB
from q.utils.reactions import Reaction
from q.utils.unit_conversions import zero_degrees_centigrade

'''
Calculates the rate coefficient of the reaction given a temperature in Kelvin
'''
def calculate_rate_coefficient(reaction: Reaction, temperature: np.ndarray | float | int):

    return reaction.arrenhius_coefficient * (temperature/zero_degrees_centigrade)**(reaction.arrenhius_exponent) * np.exp(-(reaction.activation_energy or 0)/(temperature))

'''
Calculate teh arbitrary third body density
using the ideal gas law.
Pressure in torr and temperature in Kelvin
'''
def get_third_body_density_via_ideal_gas(pressure: np.ndarray | float | int, temperature:  np.ndarray | float | int):

    return (pressure * 133 * 1e-6) / (KB*temperature) # ideal gas law: n = p/(k_b*T) and convert m^-3 to cm^-3

'''
Returns the collision rate in cm^-2 s^-1 
'''
def collision_rate(reaction: Reaction, data: dict[str, np.ndarray], shape: np._ShapeT | None = None):

    sum = np.full(shape or np.shape(next(iter(data.values()))), 1, dtype=float)

    for r in reaction.reactants:

        # For the arbitrary third body we assume the ideal gas law to get the number of particles per cell
        if r == 'M':
            rr = get_third_body_density_via_ideal_gas(data['PRESSURE'], data['TG-AVE'])
        else:
            rr = data[r]             

        sum *= rr

    return sum