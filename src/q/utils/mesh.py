from typing import Any, Iterable
import numpy as np

def convert_to_mesh_mask(mesh: np.ndarray, mask: None | list[str] = None, mask_positive: float = 1, mask_negative: float = float('nan')):
    '''
    Returns a 2d numpy array with all values that are in the mask as 1 and all
    other values as 'nan' (or other mask values if specified). The default mask is
    '0' (meaning all mesh values reading
    '0' become 1).

    This can for example be used to be multiplied with a results array, so that
    only values within the vacuum chamber remain
    '''

    if mask is None:
        mask = ['0']

    return np.array([[mask_positive if y in mask else mask_negative for y in x] for x in mesh])

def map_mesh(mesh: np.ndarray, map: dict[str, Any], default: Any =0):
    '''
    Maps mesh values to different mesh values
    '''

    return np.array([[map[y] if y in map else default for y in x] for x in mesh])

def generate_materials_mapping(hpem_config: dict[str, dict[str, Any]], inlet_overwrite: list[str] | None=None):
    '''
    Generates an appropriate plotting configuration
    out of the materials defined in the HPEM config file
    '''

    def as_list(val):
        if isinstance(val, Iterable):
            return val
        return [val]

    if 'MATERIAL' not in hpem_config:
        raise Exception('No materials configured: could not find MATERIAL section in config')
    
    materials = hpem_config['MATERIAL']
    
    metals          = (as_list(materials['CMETAL'])      if 'CMETAL'     in materials else None) or tuple()
    metals_voltage  = (as_list(materials['VRFM'])        if 'VRFM'       in materials else None) or tuple()
    # metals_freq = materials['FREQM'] if 'FREQM' in materials else ()

    wafers          = (as_list(materials['CWAFER'])      if 'CWAFER'     in materials else None) or tuple()

    dielectric      = (set(as_list(materials['CDIE']))   if 'CDIE'       in materials else None) or set()

    coils           = (as_list(materials['CCOIL'])       if 'CCOIL'      in materials else None) or tuple()

    inlets          = (as_list(materials['CINLET'])      if 'CINLET'     in materials else None) or tuple()
    outlets         = (as_list(materials['COUTLET'])     if 'COUTLET'    in materials else None) or tuple()

    magnets         = (as_list(materials['CMAGM'])       if 'CMAGM'      in materials else None) or tuple()

    metals_voltage_lookup = dict((m, metals_voltage[i]) for i, m in enumerate(metals))

    if inlet_overwrite is not None:
        inlets = [*inlets, *inlet_overwrite]

    res = list[tuple[list[str], str, str]]()
    used = set()

    if len(coils) > 0:
        res.append(([str(x) for x in coils], 'COILS', 'oo..'))
        used.update(coils)
    
    if len(magnets) > 0:
        res.append(([str(x) for x in magnets], 'PERMANENT MAGNET', '**'))
        used.update(magnets)

    if len(wafers) > 0:
        res.append(([str(x) for x in wafers], 'WAFER', 'x*x*'))
        used.update(wafers)

    grounded_inlets     = [i for i in inlets if i in metals_voltage_lookup and metals_voltage_lookup[i] == 0]
    powered_inlets      = [i for i in inlets if i in metals_voltage_lookup and metals_voltage_lookup[i] >  0]
    dielectric_inlets   = [i for i in inlets if i in dielectric]

    grounded_outlets     = [o for o in outlets if o in metals_voltage_lookup and metals_voltage_lookup[o] == 0]
    powered_outlets      = [o for o in outlets if o in metals_voltage_lookup and metals_voltage_lookup[o] >  0]
    dielectric_outlets   = [o for o in outlets if o in dielectric]

    if len(grounded_inlets) > 0:
        res.append(([str(x) for x in grounded_inlets], 'INLET (GROUNDED)', '.+'))
    if len(powered_inlets) > 0:
        res.append(([str(x) for x in powered_inlets], 'INLET (POWERED)', '.x'))
    if len(dielectric_inlets) > 0:
        res.append(([str(x) for x in dielectric_inlets], 'INLET (DIELECTRIC)', '.\\'))

    if len(grounded_outlets) > 0:
        res.append(([str(x) for x in grounded_outlets], 'OUTLET (GROUNDED)', 'o+'))
    if len(powered_outlets) > 0:
        res.append(([str(x) for x in powered_outlets], 'OUTLET (POWERED)', 'ox'))
    if len(dielectric_outlets) > 0:
        res.append(([str(x) for x in dielectric_outlets], 'OUTLET (DIELECTRIC)', 'o\\'))

    used.update(grounded_inlets, powered_inlets, dielectric_inlets, grounded_outlets, powered_outlets, dielectric_outlets)

    unused_dielectric = [d for d in dielectric if d not in used]

    if len(unused_dielectric) > 0:
        res.append(([str(x) for x in unused_dielectric], 'DIELECTRIC', '\\'))

    grounded    = [m for m in metals if m not in used and metals_voltage_lookup[m] == 0]
    powered     = [m for m in metals if m not in used and metals_voltage_lookup[m] >  0]

    if len(grounded) > 0:
        res.append(([str(x) for x in grounded], 'GROUNDED', '+'))
    if len(powered) > 0:
        res.append(([str(x) for x in powered],  'POWERED', 'x'))

    return res
