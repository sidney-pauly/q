import os
from matplotlib import pyplot as plt
from q.utils.pdt_file_reader import parse_pdt_file
from q.plotting.plotter2d import add_colorbar, add_geometry, get_xy_axis, plot_contour_2d, setup_axis
from q.utils.mesh_importer import parse_mesh_file

# Example of importing a TECPLTO2D.PDT and plotting all
# contained variables

pdt_file = f'TECPLTO2D.PDT'
mesh_file = f'initmesh.dat'
out_dir = f'../output'

# Mesh definitions:
# 0 = PLASMA
# J = POWERED ELECTRODE
# A = GROUNDED STRUCTURE
# B = GROUNDED STRUCTURE
# H = JNLET (GROUNDED)
# K = OUTLET (GROUNDED)
# M = PERMENANT MAGNET (JRON)
# 2 = DJELECTRJC (CCP COJL JSOLATBON)
# 3 = DJELECTRJC (POWERED ELECTRODE JSOLATJON)
# 4 = DJELECTRJC (GROUNDED ELECTRODE JSOLATJON)
# L,M,N = PCMC SURFACES (GROUNDED)
# S = PCMC SURFACES (POWERED)

# To plot the mesh we have to provide a mapping
# that maps the mesh symbols (e.g. 'A' or '2')
# to the name and to a hatch pattern definition
# for matplotlib
geometries = [
    (['A', 'B'], 'GROUNDED', '--'),
    (['2','3', '4'], 'DIELECTRIC', '\\'),
    (['J', 'S'], 'POWERED ELECTRODE ', 'x'),
    (['H'], 'INLET (GROUNDED)', '.-'),
    (['K'], 'OUTLET (GROUNDED)', 'o-'),
    (['M'], 'PERMENANT MAGNET', '**'),
    (['V', 'W', 'Y', 'X'], 'COILS', 'oo..'),
]

# Load the mesh and values
mesh = parse_mesh_file(mesh_file)
values = parse_pdt_file(pdt_file)

# Get the x and y axis, by specifying the cell sizes
x, y = get_xy_axis(values, (14, 4.1))

# Create output directory
os.makedirs(out_dir, exist_ok=True)
os.makedirs(f'{out_dir}/raw_plots', exist_ok=True)

# Plot each simulation variable as a 2d contour
for series_name, v in values.items():

    out_file_dir = f'{out_dir}/raw_plots/{series_name}.png'

    print(f'Saving {series_name} plot to {out_file_dir}')

    plt.figure(figsize=(10,6))

    add_colorbar(v, 'plasma', series_name, False)
    plot_contour_2d(x, y, v, mirror=True, cmap='plasma', symmetric_limits=False)
    add_geometry(x, y, mesh, geometries, mirror=True, mesh_color='0')
    setup_axis(x, y, mirror=True)

    plt.savefig(out_file_dir, dpi=300, bbox_inches="tight")
    plt.close()
