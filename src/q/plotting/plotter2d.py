import math
from typing import Any, Literal, Union
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib import cm, ticker

from q.utils.mesh import map_mesh


def add_colorbar(z_values, cmap, label, symmetric_limits=False, ax=None, inset: bool=False, vmin: float | None = None, vmax: float | None = None, label_format='%.1e', cbar_parameters:dict=dict()):
    
    ax = ax or plt.gca()
    if inset:
        ax.inset_axes((0.95, 0.1, 0.05, 0.8))
    ax.cla()

    absmax = np.max(np.abs(z_values)) if z_values is not None else 0
    vmin = vmin or (-absmax if symmetric_limits else np.min(z_values))
    vmax = vmax or ( absmax if symmetric_limits else np.max(z_values))

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax)) # pyright: ignore[reportPrivateImportUsage]
    clbr = plt.colorbar(sm, ax=ax, format=label_format, **cbar_parameters)

    clbr.ax.set_ylabel(label)

    return clbr

def _map_mash_for_geometry(mesh: np.ndarray, map: dict[str, Any], default: Any =0):
    '''
    Maps mesh values to different mesh values
    '''
    res = np.zeros(np.shape(mesh), dtype=np.dtypes.ObjectDType)
    xmin = 2**32
    xmax = 0
    ymin = 2**32
    ymax = 0

    found = False

    i = -1
    for x in mesh:
        i += 1
        j = -1
        for y in x:
            j += 1
            if y not in map:
                res[i, j] = default
                continue
            found = True
            res[i, j] = map[y]
            if i < ymin:
                ymin = i
            if i > ymax:
                ymax = i
            if j < xmin:
                xmin = j
            if j > xmax:
                xmax = j
    
    if found:
        return res, xmin, xmax, ymin, ymax
    return None
            

def add_geometry(x, y, mesh, definitions: list[tuple[list[str], str, str]], ax=plt, mesh_color='white', mirror: Literal[False, 'x', 'y']=False, add_legend=True, legend_loc: int = 2, zorder=2.001, rot90:int=0):
    '''
    Adds geometry to the plot based on the ASCII mesh and a definition for what hatch pattern 
    to apply

    :param x: x position of each cell
    :param y: y position of each cell
    :param definitions: list of tuples defining a list of geometry types (first entry), the hatch pattern to apply to those (second entry) and a display name for the legend
    :param ax: plt axis
    :param mesh_color: the colour to draw the hatches in
    :param mirror: if true the mesh is assumed to be rotationally symmetrical and mirrored along y
    '''

    mesh = np.rot90(mesh, rot90)

    # Extract the specified geometry out of hte overall mesh by applying a mask
    fill_val = [1., 0., 0., 0.]
    geometries = list(map_mesh(mesh, dict([(s, fill_val) for s in d[0]]), default=[float('nan'),0., 0., 0.]) for d in definitions)
    
    # Make hatched patches for the legend (duplicate the hatch symbols to increase density)
    circs = [mpatches.Patch(facecolor='gray', hatch=str([f'{s}{s}' for s in d[2]]), label=d[1]) for d in definitions]

    mod = rot90 % 4
    # y correction to draw at center of cells
    if mod == 0:
        x = x + (np.max(x)/len(x))*.5
    elif mod == 1:
        x = x - (np.max(x)/len(x))*.5
        y = y + (np.max(y)/len(y))*.5
    elif mod == 2:
        x = x - (np.max(x)/len(x))*.5
    elif mod == 3:
        x = x + (np.max(x)/len(x))*.5
        y = y - (np.max(y)/len(y))*.5

    # Draw the mesh
    for i in range(0, len(definitions)):

        geometry = geometries[i] 

        ax.pcolor(x, y, geometry, hatch=definitions[i][2], hatch_linewidth=1, edgecolor=mesh_color, linewidths=0, zorder=zorder)
        if mirror == 'x':
            ax.pcolor(x, y*-1, geometry,  hatch=definitions[i][2], hatch_linewidth=1, edgecolor=mesh_color, linewidths=0, zorder=zorder)
        if mirror == 'y':
            ax.pcolor(x*-1, y, geometry,  hatch=definitions[i][2], hatch_linewidth=1, edgecolor=mesh_color, linewidths=0, zorder=zorder)
    
    if add_legend:
        ax.legend(handles = circs, loc=legend_loc)  

    return circs

def get_xy_axis(values, rot90: int = 0):
    '''
    Returns appropriate x and y axis for plotting HPEM results
    
    :param values: Dataframe values from. Expects "R (cm)" and "Z (cm)" numpy arrays
    :param rot90: Rotate the axis by 90deg n times counter clockwise. Always keeps the x or y axis as the symmetry axis and makes the other axis positive. Note: this changes where 0cm is
    '''

    if 'R (cm)' not in values or 'Z (cm)' not in values:
        raise Exception('Could not find dimensions "R (cm)" or "Z (cm)"')

    size_i, size_j = np.shape(values['R (cm)'])

    extend_x = np.max(values['R (cm)'])
    extend_y = np.max(values['Z (cm)'])

    x = np.linspace(0, extend_x, size_j)
    y = np.linspace(0, extend_y, size_i)

    rotations = rot90 % 4
    if rotations == 1:
        old_x = x
        x = np.flip(y)
        y = np.flip(old_x) * -1   
    elif rotations == 2:
        x = np.flip(x)
    elif rotations == 3:
        old_x = x
        x = np.flip(y)
        y = old_x

    return x,y

def setup_axis(x, y, ax=plt,  mirror: Literal[False, 'x', 'y']=False, label:bool=False, unit='cm'):      

    if label:
        ax.xlabel(f'x ({unit})')
        ax.ylabel(f'y ({unit})')
    
    if mirror == 'y':
        abs_max = np.max(np.abs(x))
        ax.xlim(-abs_max, abs_max)
        ax.ylim(y.min(), y.max())
    elif mirror == 'x':
        ax.xlim(x.min(), x.max())
        abs_max = np.max(np.abs(y))
        ax.ylim(-abs_max, abs_max)
    else:
        ax.xlim(x.min(), x.max())
        ax.ylim(y.min(), y.max())

def plot_contour_2d(x, y, z, mirror: Literal[False, 'x', 'y']=False, levels=100, origin='upper', cmap='plasma', ax=plt, symmetric_limits=False, locator: ticker.Locator | None = None,  vmin: float | None = None, vmax: float | None = None):

    vmin = vmin or (-np.max(z) if symmetric_limits else np.min(z))
    vmax = vmax or np.max(z)

    c1 = ax.contourf(x, y, z, levels, origin=origin, locator=locator, cmap=cmap, vmin=vmin, vmax=vmax)
    if mirror == 'y':
        c2 = ax.contourf(-x, y, z, levels, origin=origin, locator=locator, cmap=cmap, vmin=vmin, vmax=vmax)
        return [c1, c2]
    if mirror == 'x':
        c2 = ax.contourf(x, -y, z, levels, origin=origin, locator=locator, cmap=cmap, vmin=vmin, vmax=vmax)
        return [c1, c2]
    return [c1]
