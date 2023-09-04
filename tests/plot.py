import matplotlib.pyplot as plt
import cartopy

def plot_rotation_unit_vectors(x_from, y_from, ux, uy, ccrs_from, ccrs_to, ev=5):
    """Plot two views of the unit vectors. First in the 'to' crs, then in the 'from' crs."""
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(projection=ccrs_to))
    ax.coastlines()
    ax.quiver(x_from[::ev,::ev], y_from[::ev,::ev], ux[::ev,::ev,0], ux[::ev,::ev,1],
          angles='xy', label='ux', color='C0', transform=ccrs_from)
    ax.quiver(x_from[::ev,::ev], y_from[::ev,::ev], uy[::ev,::ev,0], uy[::ev,::ev,1],
          angles='xy', label='uy', color='C1', transform=ccrs_from)
    ax.legend()
    ax.set_title("Rotation unit vectors in the 'to' crs")
    plt.show()

    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(projection=ccrs_from))
    ax.coastlines()
    ax.quiver(x_from[::ev,::ev], y_from[::ev,::ev], ux[::ev,::ev,0], ux[::ev,::ev,1],
          angles='xy', label='ux', color='C0')
    ax.quiver(x_from[::ev,::ev], y_from[::ev,::ev], uy[::ev,::ev,0], uy[::ev,::ev,1],
          angles='xy', label='uy', color='C1')
    ax.legend()
    ax.set_title("Rotation unit vectors in the 'from' crs")
    plt.show()

def plot_vector_components(vec_x, vec_y, rot_x, rot_y, ccrs_from):
    """Plot maps of the x and y components before and after rotation."""
    import cmocean
    cmap = cmocean.cm.balance
    vmin,vmax = np.percentile(np.ma.masked_invalid(vec_x).compressed(),(1,99))

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(9,9), sharex=True, sharey=True,
                           subplot_kw=dict(projection=ccrs_from))
    ax[0,0].coastlines()
    ax[0,0].imshow(vec_x,transform=ccrs_from, extent=ccrs_from.bounds, origin='upper',
               cmap=cmap, vmin=vmin, vmax=vmax)
    ax[0,0].set_title('original X component')
    ax[0,1].coastlines()
    ax[0,1].imshow(vec_y,transform=ccrs_from, extent=ccrs_from.bounds, origin='upper',
               cmap=cmap, vmin=vmin, vmax=vmax)
    ax[0,1].set_title('original Y component')

    ax[1,0].coastlines()
    ax[1,0].imshow(rot_x,transform=ccrs_from, extent=ccrs_from.bounds, origin='upper',
               cmap=cmap, vmin=vmin, vmax=vmax)
    ax[1,0].set_title('rotated X component')
    ax[1,1].coastlines()
    ax[1,1].imshow(rot_y,transform=ccrs_from, extent=ccrs_from.bounds, origin='upper',
               cmap=cmap, vmin=vmin, vmax=vmax)
    ax[1,1].set_title('rotated Y component')
    plt.show()

def plot_vectors(x_from, y_from, vec_x, vec_y, rot_x, rot_y, crs_from, crs_to, ccrs_from, ccrs_to, ev=2):
    """Plot vectors before and after rotation."""
    # Plot the vectors before rotation and in the 'from' crs.
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(projection=ccrs_from))
    ax.coastlines()
    ax.quiver(x_from[::ev,::ev], y_from[::ev,::ev], vec_x[::ev,::ev], vec_y[::ev,::ev],
              angles='xy', scale_units='xy', scale=0.1)
    ax.set_title("Vectors before rotation in the 'from' crs")
    plt.show()

    # define the transform from one crs to the other
    transformer = pyproj.Transformer.from_crs(crs_from, crs_to)

    # transform x_from, y_from from the "from" crs to the "to" crs.
    x_to, y_to = transformer.transform(x_from, y_from)

    # Plot the vectors after rotation in the 'to' crs
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(projection=ccrs_to))
    ax.coastlines()
    ax.quiver(x_to[::ev,::ev], y_to[::ev,::ev], rot_x[::ev,::ev], rot_y[::ev,::ev],
              angles='xy', scale_units='xy', scale=0.1)
    ax.set_title("Vectors after rotation in the 'to' crs")
    plt.show()
