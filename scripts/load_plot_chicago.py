import geopandas as gpd
import matplotlib.pyplot as plt

# lets check if the file I downloaded actually works
community_fp = "data/raw/Chicago community areas/geo_export_96e5a6e4-c68a-42a0-8240-ba5d802894f5.shp" 
community_gdf = gpd.read_file(community_fp)

# check CRS and shape info for later use 
print("CRS:", community_gdf.crs)
print("Shape:", community_gdf.shape)
print(community_gdf.head())

# plot because I cannot visualize in my head
community_gdf.plot(edgecolor="black", facecolor="none", figsize=(10, 10))
plt.title("Chicago Community Areas (77)")
plt.axis("off")
plt.show()
