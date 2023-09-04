import numpy as np
import pyproj

def rotation_unit_vectors(x_from, y_from, crs_from, crs_to):
    """Compute two sets of unit vectors (ux and uy) defining the x and y axes of the rotation.

    Args:
       x_from (2D array): x locations of the grid in the 'from' crs
       y_from (2D array): y locations of the grid in the 'from' crs
       crs_from (pyproj.CRS): pyproj object defining the 'from' crs
       crs_to (pyproj.CRS): pyproj object defining the 'to' crs

    Returns:
       ux (3D array): x and y components of the ux unit vector of the rotation in the 'from' crs.
       vx (3D array): x and y components of the uy unit vector of the rotation in the 'from' crs.

    Notes:
       -  this step is a pre-processing before the actual rotation of the vectors. The vectors to be
          rotated are not input parameters to the routine.
       -  x_from and y_from must be in units that can directly be entered the 'from' crs (e.g. meters
          or degrees) as no unit conversion is performed inside this routine.
    """
    # sanity check on the shape of the input parameters
    if x_from.shape != y_from.shape:
        raise ValueError("x_from and y_from must have the same shape.")
    if len(x_from.shape) != 2:
        raise ValueError("x_from and y_from must be 2D arrays.")

    # define the transform from one crs to the other
    transformer = pyproj.Transformer.from_crs(crs_from, crs_to)

    # transform x_from, y_from from the "from" crs to the "to" crs.
    x_to, y_to = transformer.transform(x_from, y_from)

    # in the "to" crs, compute a small increasing step in 'x' direction.
    #   its length does not matter, we will normalize to unit vectors later
    epsx_to = 0.1
    x2_to = x_to + epsx_to

    # if the "to" crs is geographic, then x is the longitude and we must wrap x2 to [-180;+180]
    if crs_to.is_geographic:
        x2_to = (x2_to + 180) % 360 - 180

    # transform the x_to + epsx_to (ux direction) back into the "from" crs
    x_ux_from, y_ux_from = transformer.transform(
        x2_to, y_to, direction=pyproj.enums.TransformDirection.INVERSE)

    # define the ux vectors in the "from" crs
    ux = np.stack(((x_ux_from - x_from), (y_ux_from - y_from)), axis=2)

    # normalize each vector to be unit vectors
    ux_norm = (ux[:, :, 0]**2 + ux[:, :, 1]**2)**0.5
    ux /= np.repeat(ux_norm[:, :, None], 2, axis=2)

    # define uy which is perpendicular to ux
    uy = ux.copy()
    uy[:, :, 0] = -ux[:, :, 1]
    uy[:, :, 1] = +ux[:, :, 0]

    # done, return
    return ux, uy


def apply_vector_rotation(vec_x, vec_y, ux, uy):
    """Rotate 2D vector fields (vec_x, vec_y) onto axes defined by unit vectors ux and uy

    Args:
       vec_x (2D array): x components of the vectors to be rotated
       vec_y (2D array): y components of the vectors to be rotated
       ux (2D array) : unit vector defining the x-direction of the rotation
       uy (2D array) : unit vector defining the y-direction of the rotation

    Returns:
       rot_x (2D array): x components of the rotated vectors.
       rot_y (2D array): y components of the rotated vectors.

    """
    # sanity check on the shape of the input parameters
    if vec_x.shape != vec_y.shape:
        raise ValueError("vec_x and vec_y must have the same shape.")
    if len(vec_x.shape) != 2:
        raise ValueError("vec_x and vec_y must be 2D arrays.")

    # prepare an (nx,ny,2) array for the input (vec_x,vec_y) vector
    vec = np.stack((vec_x, vec_y), axis=2)

    # use the einsum notation to compute dot products at each (nx,ny) locations
    rot_x = np.einsum('ijk,ijk->ij', vec, ux)
    rot_y = np.einsum('ijk,ijk->ij', vec, uy)

    # done, return
    return rot_x, rot_y


def vector_rotate(crs_from, crs_to, x_pos, y_pos, vec_x, vec_y):
    """
    Rotate 2D vector fields (vec_x, vec_y) at position (x_pos, y_pos) from crs_from to crs_to.

    This function is a shortcut for creating unit vectors with
    `rotation_unit_vectors` and then `apply_vector_rotation` with the unit
    vectors.

    Args:
       x_pos (2D array): x locations of the grid in the 'from' crs
       y_pos (2D array): y locations of the grid in the 'from' crs
       crs_from (pyproj.CRS): pyproj object defining the 'from' crs
       crs_to (pyproj.CRS): pyproj object defining the 'to' crs
       vec_x (2D array): x components of the vectors to be rotated
       vec_y (2D array): y components of the vectors to be rotated

    Returns:
       rot_x (2D array): x components of the rotated vectors.
       rot_y (2D array): y components of the rotated vectors.

    Notes:
       -  x_pos and y_pos must be in units that can directly be entered the 'from' crs (e.g. meters
          or degrees) as no unit conversion is performed inside this routine.
    """
    ux, uy = rotation_unit_vectors(crs_from, crs_to, x_pos, y_pos)
    return apply_vector_rotation(vec_x, vec_y, ux, uy)
