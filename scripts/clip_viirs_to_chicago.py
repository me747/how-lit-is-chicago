import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping
import geopandas as gpd
import matplotlib.pyplot as plt

# load more file paths to work on
viirs_raster_fp = "data/raw/Global VIIRS 2024\VNL_npp_2024_global_vcmslcfg_v2_c202502261200.average_masked.dat.tif"
community_fp = "data/raw/Chicago community areas/geo_export_96e5a6e4-c68a-42a0-8240-ba5d802894f5.shp" 
community_gdf = gpd.read_file(community_fp)
output_clipped_fp = "data/processed/viirs_chicago_clipped.tif"

# make Chicago boundary, unify polygon of all community areas (I dont wanna download more files)
chicago_boundary = [mapping(community_gdf.unary_union)]

# clipping raster to the city boundary
with rasterio.open(viirs_raster_fp) as src:
    out_image, out_transform = mask(src, chicago_boundary, crop=True, nodata=0)
    out_meta = src.meta.copy()

# apparently need to update metadata as well (whatever that means)
out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform,
    "nodata": 0
})

# almost done save!
with rasterio.open(output_clipped_fp, "w", **out_meta) as dest:
    dest.write(out_image)

print("Clipped raster saved at:", output_clipped_fp)

# apparently weren't done before but now almost, lets plot
fig, ax = plt.subplots(figsize=(10, 10))
img = ax.imshow(
    out_image[0],
    cmap="inferno",
    extent=[out_transform[2], out_transform[2] + out_transform[0] * out_image.shape[2],
            out_transform[5] + out_transform[4] * out_image.shape[1], out_transform[5]],
    vmin=0,
    vmax=out_image.max()
)
community_gdf.boundary.plot(ax=ax, edgecolor="cyan", linewidth=1)
plt.colorbar(img, ax=ax, label="Radiance")
ax.set_title("VIIRS Nighttime Lights - Clipped to Chicago", fontsize=14)
ax.set_axis_off()

# save the plot (to show my work)
plot_fp = "figures/viirs_chicago_overlay.png"
plt.savefig(plot_fp, dpi=300, bbox_inches="tight")
print(f"Plot saved at: {plot_fp}")
plt.show()
