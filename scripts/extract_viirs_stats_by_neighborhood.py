import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping
import numpy as np
import pandas as pd

# load more file paths
raster_file = "data/processed/viirs_chicago_clipped.tif"
community_file = "data/raw/Chicago community areas/geo_export_96e5a6e4-c68a-42a0-8240-ba5d802894f5.shp"
output_file = "data/processed/community_light_stats.csv"

communities = gpd.read_file(community_file)

# to make sure CRS matches
communities = communities.to_crs(epsg=4326)
raster = rasterio.open(raster_file)
results = []

# apparently adding these random print statements makes it easier to debug 
print("Starting calculation for light statistics for each community area...")

for index, row in communities.iterrows():
    geometry = [mapping(row["geometry"])]

    # mas the viirs raster with the current community polygon
    out_image, out_transform = mask(raster, geometry, crop=True, nodata=0)

    # get pixel values inside the polygon (assuming single band raster)
    data = out_image[0]

    # remove zeros which represent no data
    data = data[data > 0]

    # if theres data calculate stats 
    if len(data) > 0:
        mean_val = np.mean(data)
        sum_val = np.sum(data)
        min_val = np.min(data)
        max_val = np.max(data)
        std_val = np.std(data)
    else:
        mean_val = 0
        sum_val = 0
        min_val = 0
        max_val = 0
        std_val = 0

    results.append({
        "community": row["community"],
        "area_num": row["area_numbe"],
        "mean_radiance": mean_val,
        "sum_radiance": sum_val,
        "min_radiance": min_val,
        "max_radiance": max_val,
        "std_radiance": std_val
    })

# adding another random print statement 
print("Done calculating stats! Saving to CSV")
df = pd.DataFrame(results)
df.to_csv(output_file, index=False)
print("Done! Results saved to", output_file) # so I know where the file was saved
