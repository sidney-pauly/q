from dataclasses import dataclass
from typing import Iterable
import re

SPECIES_DEFINITION_REGEX = re.compile(r'^([a-zA-Z0-9_\-\*\^\s]*):([\d\s\-]*);([\d\s\-\+\.Ee]*)&([\d\s\-\+\.Ee]*)\]([\d\s\-]*)\[([\d\s\-\+\.Ee]*)([a-zA-Z0-9_\-\*\^\s\@]*)')
SPECIES_EXTENSION_REGEX = re.compile(r'^([>\s]*):([\d\s]*)&([\d\s\-\+\.Ee]*)\[([\d\s\-\+\.Ee]*)([a-zA-Z0-9_\-\*\^\s\@]*)')
REACTION_REGEX = re.compile(r'^((([a-zA-Z0-9_\-\*\^\s]*)\+?)+)>((([a-zA-Z0-9_\-\*\^\s]*)\+?)+):([\d\s\-\+\.Ee]*);([\d\s\-\+\.Ee]*)(&([\d\s\-\+\.Ee]*)\]([\d\s\-\+\.Ee]*)\[([\d\s\-]*))?(\$([\d\s\-\+\.Ee]*))?')

@dataclass
class Species:

    name: str
    '''
    species name
    Positive ions are denoted as He^ (NOT He+)
    '''

    charge: int
    '''charge (integer, eg., 1,-1,0)'''

    molecular_weight: float
    '''Molecular weight in amu'''

    transport: bool
    '''1 if transport is to be included, 0 for not'''

    default_sticking_coefficients: dict[str, float]
    '''
    sticking coefficient on surfaces. The key here is the name of the
    return species (this will be the same for all incidence species, which is
    specified as such by HPEM)
    '''

    default_return: dict[str, float]
    '''
    The default species returned by a wall collision.
    dictionary of species name mapped to likelihood of that
    species being returned
    '''

    special_sticking_coefficients: dict[int, dict[str, float]]
    '''
    sticking coefficient on surfaces. The key here is the name of the
    return species (this will be the same for all incidence species, which is
    specified as such by HPEM)
    '''

    special_return: dict[int, dict[str, float]]
    '''
    The species returned in a collision with a wall of specific material.
    Outer dictionary indexes by material id, inner
    dictionary maps species name to likelihood of that
    species being returned
    '''

@dataclass
class Reaction:

    reactants: list[str]

    products: list[str]

    arrenhius_coefficient: float
    '''
    Reaction Arrenhius coefficient A (cgs). If the Arrenhius 
    coefficient is 0.0, then the rate coefficient will
    be calculated in the Electron Energy Transport module. 
    This applies only to electron 
    impact reactions. If this is the case, then an appropriate 
    special number  must be entered.
    '''

    arrenhius_exponent: float
    '''
    Exponent "n" in Arrenhius rate coefficient expression.
    '''

    activation_energy: float | None = None
    '''
    Activation energy "E" in Arrenhius rate coefficient expression.
    '''

    exothermicity: float | None = None
    '''
    Exothermicity of reaction (eV). Since separate energy equations
    are solved for each species, the typical "delta-H" of reaction
    is a bit ill defined. The parameter is the exothermic energy
    which is dissipated in translational modes. A positive value
    of the exothermicity in the column will heat the gas. This 
    energy is then partitioned among the reaction products. 
    When entering a value in this column, the full Arrenhius 
    form of the rate coefficient must be used
    '''

    special_number: int | None = None
    '''
    Special number: A special number MUST be entered for every
	reaction.
    '''

    result_electron_energy: float | None = None
    '''
    Reactions that do not involve an electron but produce an 
    electron can contribute energy to the electron swarm.  This
    column is the excess energy of the reaction that goes into
        the electron (eV).
    '''

    def to_formula(self):
        ''' Returns the reaction as a formula with reactants on the left and products on the right'''
        return f'{'+'.join(self.reactants)}>{'+'.join(self.products)}'

def read_reactions_dat_file(path: str):

    with open(path, 'r') as f:

        lines = f.readlines()

    return parse_reactions_dat_file(lines)

def parse_reactions_dat_file(lines_iterable: Iterable[str]):

    all_species = dict[str, Species]()
    cur_species = None

    reactions = list[Reaction]()

    i = 0

    for l in lines_iterable:

        i += 1

        try:
        
            # Comments are denoted by ! and cannot be terminated,
            # hence any string after a ! will be irrelevant for parsing
            comment_split = l.strip().split('!')

            content = comment_split[0]

            if content == '' or ':' not in content:
                continue

            # Rationale: A definition only has one species name before the :
            # a reaction will have multiple and a +, so this should catch this cleanly
            definition_split = content.split(':')[0].strip().split(' ')

            # Decide between species definition and reaction
            if len(definition_split) < 2:

                match = SPECIES_DEFINITION_REGEX.search(content)

                if match is not None:

                    g = [e.strip() for e in match.groups()]

                    cur_species = Species(g[0], int(g[1]), float(g[2]), bool(float(g[4])), {g[6]: float(g[3])}, {g[6]: float(g[5])}, {}, {})

                    all_species[cur_species.name] = cur_species


                # If there is a current species check if this line is an extension to the current specification
                if cur_species is None:
                    continue
                
                match = SPECIES_EXTENSION_REGEX.search(content)

                if match is None:
                    continue

                g = [e.strip() for e in match.groups()]

                # If there is no species information then this is a default wall reflection definition
                if g[1] == '':
                    cur_species.default_sticking_coefficients[g[4]] = float(g[2])
                    cur_species.default_return[g[4]] = float(g[3])
                else:
                    return_species = int(g[1])
                    if return_species not in cur_species.special_return:
                        cur_species.special_return[return_species] = {g[4]: float(g[3])}
                    else:
                        cur_species.special_return[return_species][g[4]] = float(g[3])

                    if return_species not in cur_species.special_sticking_coefficients:
                        cur_species.special_sticking_coefficients[return_species] = {g[4]: float(g[2])}
                    else:
                        cur_species.special_sticking_coefficients[return_species][g[4]] = float(g[2])

            else:

                match = REACTION_REGEX.search(content)

                if match is None:
                    continue

                g = [e.strip() for e in match.groups() if e is not None]

                reactants = [r.strip() for r in g[0].split('+')]
                products  = [r.strip() for r in g[3].split('+')]

                reaction = Reaction(reactants, products, float(g[6]), float(g[7]))
                reactions.append(reaction)

                if len(g) < 9 or g[8] == '':
                    continue

                reaction.activation_energy = float(g[9])
                reaction.exothermicity = float(g[10])
                reaction.special_number = int(g[11])

                if len(g) < 14 or g[13] == '':
                    continue

                reaction.result_electron_energy = float(g[13])

        except Exception as e:
            raise Exception(f'Exception while parsing line {i}') from e

    return all_species, reactions

def filter_reactions(species: Iterable[Species], reactions: Iterable[Reaction], filter_reactants: Iterable[str] | None = None, filter_products: Iterable[str] | None = None):
    '''Filters species and reactions by their inputs and outputs '''

    filter_reactants_set = set(filter_reactants) if filter_reactants is not None else None
    filter_products_set = set(filter_products) if filter_products is not None else None

    reactions = [r for r in reactions if ((filter_reactants_set is None or any(rr in filter_reactants_set for rr in r.reactants)) and (filter_products_set is None or any(rr in filter_products_set for rr in r.products)))]

    # Filter species efficiently through a hash set
    species_names = set()
    species_names.update(*[r.reactants for r in reactions])
    species_names.update(*[r.products for r in reactions])
    species = [s for s in species if s.name in species_names]

    return species, reactions


'''
Class to split molecules into their atoms
'''
class MoleculeAnalyzer():

    '''
    Initializes a new Molecule Analyzer object with a set
    of allowed atom species.
    Species should be given as their base name, e.g. 'H' for hydrogen or
    'AR' for argon
    '''
    def __init__(self, atoms: Iterable[str]) -> None:

        species_condition = '|'.join(atoms)
        species_regex = fr'^((({species_condition})+[0-9]*)+)([SMPDR]+)*(V[0-9]*)*(\-*\+*\^*)(\**)$'
        self.species_re = re.compile(species_regex)
        self.atom_re = re.compile(fr'({species_condition})[0-9]*')

    '''
    Returns a dictionary with the atom name and its count.
    If the molecule contains unrecognized species throws an error
    '''
    def get_atoms_from_molecule_name(self, molecule: str):

        m = self.species_re.search(molecule)
        if m is None:
            raise Exception("PARSE ERROR")
        g = m.groups()
        excitation_stripped = g[0]

        atoms =  [molecule[m.regs[0][0]:m.regs[0][1]] for m in self.atom_re.finditer(excitation_stripped)]
        
        return [(a, 1) if len(a) < 2 else (a[0:1], int(a[1:])) for a in atoms]

def get_molecule_total_size(m: Iterable[tuple[str, int]]):
    return sum(x[1] for x in m)

def atoms_to_molecule(atoms: Iterable[tuple[str, int]]):
    res = ''
    for n, c in atoms:
        res += n
        if c > 1:
            res += str(c)
    return res

def filter_largest_molecules(molecules: Iterable[tuple[str, Iterable[tuple[str, int]]]]):

    biggest = max(get_molecule_total_size(m[1]) for m in molecules) 

    return [m for m in molecules if get_molecule_total_size(m[1]) == biggest]

