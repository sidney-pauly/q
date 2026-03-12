
from typing import Literal
from matplotlib.colorizer import Colorizer
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt
from q.plotting.plotter2d import add_colorbar, plot_contour_2d

def rotate_uv(u, v, rot90):
    u = np.rot90(u, rot90)
    v = np.rot90(v, rot90)

    mod = rot90 % 4 

    if mod == 1:
        old_u = u
        u = v
        v = old_u
    elif mod == 2:
        u = -u
    elif mod == 3:
        old_u = u
        u = -v
        v = -old_u
    return u,v

def plot_vector_arrows(x, y, u, v, scale_arrows_by_value=False, arrow_scale: float = 1,  mirror: Literal[False, 'x', 'y']=False, rot90: int = 0, arrow_frequency=1, arrow_color='0', cmap='plamsa', cmap_label=None, colorbar=True, vmin: float | None = None, vmax: float | None = None, colorbar_format = '%.2e', colorbar_params=dict()):

    u, v = rotate_uv(u, v, rot90)
    l = np.sqrt(u**2 + v**2)
    u, v = scale_arrows(x, y, u, v, scale_arrows_by_value, arrow_scale, arrow_frequency, l, vmax)   
    m = arrow_frequency

    if colorbar:
        add_colorbar(l, cmap, cmap_label, False, vmin=vmin, vmax=vmax, label_format=colorbar_format, cbar_parameters=colorbar_params)

    colorizer = Colorizer(cmap, Normalize(vmin or min(np.min(u), np.min(v)), vmax or max(np.max(u), np.max(v))))

    main_arrows = plt.quiver(x[::m], y[::m], u[::m, ::m], v[::m, ::m], l[::m, ::m],  scale_units='x', units='xy', scale=2, cmap=colorizer, width=0.03)
    if mirror == 'y':
        mirrored_arrows = plt.quiver(-x[::m], y[::m], -u[::m, ::m], v[::m, ::m], l[::m, ::m], scale_units='x', units='xy', scale=2, cmap=colorizer, width=0.03)
        return main_arrows, mirrored_arrows
    elif mirror == 'x':
        mirrored_arrows = plt.quiver(x[::m], -y[::m], u[::m, ::m], -v[::m, ::m], l[::m, ::m], scale_units='x', units='xy', scale=2, cmap=colorizer, width=0.03)
        return main_arrows, mirrored_arrows
    
    return main_arrows

def plot_vector_arrows_and_contour(x, y, u, v, scale_arrows_by_value=False, arrow_scale: float = 1,  mirror: Literal[False, 'x', 'y']=False, rot90: int = 0, arrow_frequency=1, arrow_color='0', cmap='plamsa', cmap_label=None, colorbar=True, vmin: float | None = None, vmax: float | None = None, colorbar_format = '%.2e', colorbar_params=dict()):

    u, v = rotate_uv(u, v, rot90)
    l = np.sqrt(u**2 + v**2)
    u, v = scale_arrows(x, y, u, v, scale_arrows_by_value, arrow_scale, arrow_frequency, l, vmax)   
    m = arrow_frequency

    if colorbar:
        add_colorbar(l, cmap, cmap_label, False, vmin=vmin, vmax=vmax, label_format=colorbar_format,cbar_parameters=colorbar_params)

    contour = plot_contour_2d(x, y, l, mirror=mirror, cmap=cmap, symmetric_limits=False, vmin=vmin, vmax=vmax)

    main_arrows = plt.quiver(x[::m], y[::m], u[::m, ::m], v[::m, ::m], scale_units='x', units='xy', scale=2, color=arrow_color, width=0.03, zorder=3)

    if mirror == 'y':
        mirrored_arrows = plt.quiver(-x[::m], y[::m], -u[::m, ::m], v[::m, ::m], scale_units='x', units='xy', scale=2, color=arrow_color, width=0.03, zorder=3)
        return contour, main_arrows, mirrored_arrows
    elif mirror == 'x':
        mirrored_arrows = plt.quiver(x[::m], -y[::m], u[::m, ::m], -v[::m, ::m], scale_units='x', units='xy', scale=2, color=arrow_color, width=0.03, zorder=3)
        return contour, main_arrows, mirrored_arrows

    return contour, main_arrows


def plot_streamlines(x, y, u, v, mirror: Literal[False, 'x', 'y']=False, rot90: int = 0, streamline_color='0', cmap='plamsa', cmap_label=None, colorbar=True, vmin: float | None = None, vmax: float | None = None, colorbar_format = '%.2e', colorbar_params=dict()):

    u, v = rotate_uv(u, v, rot90)
    l = np.sqrt(u**2 + v**2)

    if colorbar:
        add_colorbar(l, cmap, cmap_label, False, vmin=vmin, vmax=vmax, label_format = colorbar_format,cbar_parameters=colorbar_params)

    if x[0] > x[-1]:
        x = np.flip(x)
        u = np.flip(u)

    if y[0] > y[-1]:
        y = np.flip(y)
        v = np.flip(v)

    if mirror == 'y':
        xx = np.concatenate((np.flip(-x), x))
        uu = np.concatenate((np.flip(-u, 1), u), axis=1)
        vv = np.concatenate((np.flip(v, 1), v), axis=1)
        ll = np.concatenate((np.flip(l, 1), l), axis=1)

        xx = np.delete(xx, len(x)-1, 0)
        uu = np.delete(uu, len(x)-1, 1)
        vv = np.delete(vv, len(x)-1, 1)
        ll = np.delete(ll, len(x)-1, 1)

        contour = plot_contour_2d(x, y, l, mirror=mirror, cmap='plasma', symmetric_limits=False)
        streamlines = plt.streamplot(xx, y, uu, vv, color=streamline_color, cmap='plasma', density=2)

    else:
        xx = x
        uu = -u
        vv = -v


        contour = plot_contour_2d(xx, y, l, mirror=mirror, cmap='plasma', symmetric_limits=False)
        streamlines = plt.streamplot(xx, y, uu, vv, color=streamline_color, cmap='plasma', density=2)

    return contour, streamlines

def scale_arrows(x, y, u, v, scale_arrows_by_value, arrow_scale, arrow_frequency, l, vmax: float | None = None):
    
    max_magnitude = vmax or max(np.max(u), np.max(v))

    if scale_arrows_by_value:
        u = u*((x[1]-x[0])/max_magnitude)
        v = v*((y[1]-y[0])/max_magnitude)

        log_factor = 50
        u = np.sign(u) * np.log(np.abs(u)*log_factor+1)/np.log(log_factor+1)
        v = np.sign(v) * np.log(np.abs(v)*log_factor+1)/np.log(log_factor+1)

    else:
            # dd = max(x[1]-x[0], y[1]-y[0])
        dd = x[1]-x[0]

        u = (u/l)*dd*arrow_frequency*2
        v = (v/l)*dd*arrow_frequency*2 

    u = u * arrow_scale
    v = v * arrow_scale
    return u,v

        