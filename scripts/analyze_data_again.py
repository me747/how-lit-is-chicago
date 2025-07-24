import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# reusing the same code from analyze_data.py again just added few more features 
# last time i think
df = pd.read_csv("data/processed/community_light_acs_complaints_buildings.csv")
df = df.rename(columns={"Total Population": "population"})

# to estimate median income
income_brackets = {
    "Under $25,000": 12500,
    "$25,000 to $49,999": 37500,
    "$50,000 to $74,999": 62500,
    "$75,000 to $125,000": 100000,
    "$125,000 +": 150000
}

total_income = 0
for col, midpoint in income_brackets.items():
    total_income += df[col] * midpoint

df["median_income"] = total_income / df["population"]

# I wanna calculate population density, so need to get area first from the shapefile for each community area
gdf = gpd.read_file("data/raw/Chicago community areas/geo_export_96e5a6e4-c68a-42a0-8240-ba5d802894f5.shp")
gdf["community"] = gdf["community"].str.upper()
gdf = gdf.to_crs(epsg=3395)
gdf["area_km2"] = gdf["geometry"].area / 1e6

df = df.merge(gdf[["community", "area_km2"]], on="community", how="left") # add the area_km2 col to my dataframe
df["density"] = df["population"] / df["area_km2"] # calculate population density

# trying this feature engineering thing again, calculate footprint per capita and per km^2
df["footprint_per_capita"] = df["total_building_footprint_m2"] / df["population"]
df["footprint_per_km2"] = df["total_building_footprint_m2"] / df["area_km2"]

# main features to analyze
features = ["mean_radiance", "sum_radiance", "min_radiance", "max_radiance", "std_radiance","population", "density", "median_income",
            "total_building_footprint_m2", "footprint_per_capita", "footprint_per_km2"]

df_clean = df[features].dropna()

# correlation matrix
corr_matrix = df_clean.corr()

# gpt this to show entire output in the terminal window, apparently this increases the windows size
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.float_format", lambda x: f"{x: .6f}")
print("\n Correlation Matrix")
print(corr_matrix)

# heatmap of the correlation matrix
os.makedirs("figures", exist_ok=True)
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Correlation Heatmap: VIIRS & Urban Features")
plt.tight_layout()
plt.savefig("figures/correlation_matrix_with_buildings.png", dpi=300)
plt.show()
plt.close()
print("Correlation matrix heatmap saved to: figures/correlation_matrix_with_buildings.png")
