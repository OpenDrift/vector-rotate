import pyresample as pr
import xarray as xr
from .plot import *

def test_osi_sea_ice():
# the OSI SAF sea-ice drift CDR v1 is on EASE2 polar grids
    f = 'https://thredds.met.no/thredds/dodsC/osisaf/met.no/reprocessed/ice/drift_455m_files/merged/2020/03/ice_drift_nh_ease2-750_cdr-v1p0_24h-202003151200.nc'
    ds = xr.open_dataset(f)
    adef, _ = pr.utils.load_cf_area(ds)
    crs_from = adef.crs
    x_from, y_from = np.meshgrid(adef.projection_x_coords, adef.projection_y_coords)
    ccrs_from = adef.to_cartopy_crs()
    vec_x = ds['dX'][0].data * 1000.
    vec_y = ds['dY'][0].data * 1000.

# define target crs: a Plate Carree (WGS84) (lat/lon)
    crs_to_epsg = '32663'
    crs_to = pyproj.CRS(crs_to_epsg)
    ccrs_to = cartopy.crs.epsg(crs_to_epsg)

# rotate vector components
    ux, uy = get_rotation_unit_vectors(x_from, y_from, crs_from, crs_to)
    rot_x, rot_y = apply_vector_rotation(vec_x, vec_y, ux, uy)

# plot
    plot_rotation_unit_vectors(x_from, y_from, ux, uy, ccrs_from, ccrs_to)
    plot_vector_components(vec_x, vec_y, rot_x, rot_y, ccrs_from)
    plot_vectors(x_from, y_from, vec_x, vec_y, rot_x, rot_y, crs_from, crs_to, ccrs_from, ccrs_to,)
