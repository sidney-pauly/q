import numpy as np
from q.hpem_data_frame import HPEM_DataFrame, Reaction
from q.utils.reactions import read_reactions_dat_file
from q.utils.integration import integrate_cylindrical_volume
import matplotlib.pyplot as plt
from q.utils.reaction_rates import calculate_rate_coefficient, collision_rate

DIR = f''
FORMULA = 'H1+NH>H2V0+N' # Example Hydrogen reaction

icp_file = f'{DIR}/icp.dat' # Path of the icp.dat file
 
species, parsed_reactions = read_reactions_dat_file(icp_file) # import all species and reactions
df = HPEM_DataFrame.from_folder(DIR) # Import data

# Find the reaction from the list of all reactions using its formula
h1_react = next(r for r in parsed_reactions if r.to_formula() == FORMULA) 

if df.data_2d is None or df.cycle_data_2d is None:
    raise Exception()

# Calculate the rate coefficient using the reaction data, the temperature in each cell as well as the
# collision rate of the reactants in that cell
h1_reaction_rate = calculate_rate_coefficient(h1_react, df.data_2d['TG-AVE']) * collision_rate(h1_react, df.data_2d)

# Integrate over the cylindrical volume (if using cylindrical coordinates)
h1_per_second_total = integrate_cylindrical_volume(df.data_2d['R (cm)'], df.data_2d['Z (cm)'], h1_reaction_rate)

print(f'In total the reaction rate of {h1_react.to_formula()} is {h1_per_second_total:.2e} s^-1')