import geopandas as gpd
import pandas as pd
import os

# lets load the community area shapefile again to extract building footprint per community area
gdf_comm = gpd.read_file("data/raw/Chicago community areas/geo_export_96e5a6e4-c68a-42a0-8240-ba5d802894f5.shp")
gdf_comm = gdf_comm.to_crs(epsg=3395)  # project to meters 
gdf_comm = gdf_comm[["area_numbe", "geometry"]]  # keeping only the needed cols
gdf_comm = gdf_comm.rename(columns={"area_numbe": "area_num"}) # rename this because OCD

# loading the building footprints shape file
gdf_buildings = gpd.read_file("data/raw/Chicago Building Footprints\geo_export_452a88c6-d194-47df-96cd-5b24e0978971.shp")
gdf_buildings = gdf_buildings.to_crs(epsg=3395) # projecting to meters again for consistency 

# calculate building area in m^2
gdf_buildings["building_area"] = gdf_buildings.geometry.area

# spatial join to assign each building to a community area
gdf_joined = gpd.sjoin(gdf_buildings, gdf_comm, how="inner", predicate="within")

# to calculate total building area per commmunity 
community_num = gdf_joined["area_num"].unique()
footprint = []

for i in community_num:
    subset = gdf_joined[gdf_joined["area_num"] == i]
    total_area = subset["building_area"].sum()
    footprint.append({"area_num": i, "total_building_footprint_m2": total_area})

footprint_df = pd.DataFrame(footprint)

# load the merged dataset with the complaints
df_main = pd.read_csv("data/processed/community_light_acs_complaints_merged.csv")

# merge on area_num
df_merged = df_main.merge(footprint_df, on="area_num", how="left")

# save, this might be the last feature I add I cant look at any more rows or cols
output_path = "data/processed/community_light_acs_complaints_buildings.csv"
df_merged.to_csv(output_path, index=False)
print(f"Merged dataset saved to {output_path}")
