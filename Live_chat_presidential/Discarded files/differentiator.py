import json

# Load both JSON files
with open('./wfaa_DK.json', 'r') as file1:
    data1 = json.load(file1)

with open('./wfaa_merged.json', 'r') as file2:
    data2 = json.load(file2)

# Convert lists of dictionaries to sets of tuples for easier comparison
set1 = set((item['timestamp'], item['author'], item['message']) for item in data1)
set2 = set((item['timestamp'], item['author'], item['message']) for item in data2)

# Find differences
only_in_file1 = set1 - set2  # Items in wfaa_DK.json but not in wfaa_merged.json
only_in_file2 = set2 - set1  # Items in wfaa_merged.json but not in wfaa_DK.json

# Display the differences
print("Entries only in wfaa_DK.json:")
for entry in only_in_file1:
    print(entry)

print("\nEntries only in wfaa_merged.json:")
for entry in only_in_file2:
    print(entry)
