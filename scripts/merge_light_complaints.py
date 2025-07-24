import pandas as pd

df_311 = pd.read_csv("data/raw/311_Service_Requests_-_Street_Lights_-_All_Out_-_Historical_20250722.csv")

# count complaints by community area number
complaint_count = {}
for area in df_311["Community Area"]:
    if area in complaint_count:
        complaint_count[area] += 1
    else:
        complaint_count[area] = 1

# convert the dictionary to a DataFrame
complaint_count = pd.DataFrame({
    "Community Area": list(complaint_count.keys()),
    "complaint_count": list(complaint_count.values())
})

# lets load the previously merged dataset with the light and acs stats
main_df = pd.read_csv("data/processed/community_light_acs_merged.csv")

# merge complaint counts on 311's "Community Area" and main_df's "area_num"
merged_df = main_df.merge(complaint_count, left_on="area_num", right_on="Community Area", how="left")

# Step 5: Fill missing complaint counts with 0 and drop duplicate 'Community Area' column after merge
merged_df["complaint_count"] = merged_df["complaint_count"].fillna(0).astype(int)
merged_df = merged_df.drop(columns=["Community Area"])

# Step 6: Save the merged dataset
output_path = "data/processed/community_light_acs_complaints_merged.csv"
merged_df.to_csv(output_path, index=False)
print(f"Merged dataset saved to: {output_path}")
