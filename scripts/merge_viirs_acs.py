import pandas as pd

# at this point I think we all know what is happening here
light_stats_fp = "data/processed/community_light_stats.csv"
acs_fp = "data/raw/ACS_5_Year_Data_by_Community_Area_20250717.csv"
output_fp = "data/processed/community_light_acs_merged.csv"

# read viirs and ACS files
light_stats = pd.read_csv(light_stats_fp)
acs = pd.read_csv(acs_fp)

# check column names to merge on and apparently I can do this on code, cause opening two files and checking column names isn't cool anymore
print("Columns in light stats:", light_stats.columns)
print("Columns in ACS:", acs.columns)

# since i checked the column names, community col in ACS is 'Community Area' and in light_stats is 'community', so rename
acs = acs.rename(columns={"Community Area": "community"})

# merge on 'community' column
merged = pd.merge(light_stats, acs, on="community", how="left")
print(f"Merged dataset has {merged.shape[0]} rows and {merged.shape[1]} columns")

# save or what else even was the point of all this
merged.to_csv(output_fp, index=False)
print("Merged data saved to:", output_fp)
