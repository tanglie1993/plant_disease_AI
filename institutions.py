import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter

# Define the file path
file_path = 'data.txt'

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Extract institutions
pattern = re.compile(r'C1 (.*?)\n[A-Z]', re.DOTALL)
matches = pattern.findall(data + '\nA')  # Adding '\nA' to capture the last C1 block

# Process institutions
all_institutions = []
for match in matches:
    institutions = set()  # Use a set to avoid counting duplicates in the same record
    lines = match.split('\n')
    for line in lines:
        if ']' in line:
            parts = line.split(']')
            for part in parts:
                print('--------')
                print(part)
                if part.find('[') < 0:
                    institution = part.split(',')[0].strip()
                    if institution:  # Ensure it's not empty
                        print('---institution-----')
                        print(institution)
                        institutions.add(institution)
                
    all_institutions.extend(institutions)

# Count the top contributing institutions
institution_counts = Counter(all_institutions)
top_institutions = institution_counts.most_common(10)

# Convert to DataFrame for easier plotting
df_institutions = pd.DataFrame(top_institutions, columns=['Institution', 'Count'])

# Print the top 10 contributing institutions
print("Top 10 Contributing Institutions:")
print(df_institutions)

# Plot the bar chart
plt.figure(figsize=(12, 6))
plt.barh(df_institutions['Institution'], df_institutions['Count'], color='skyblue')
plt.xlabel('Number of Publications')
plt.title('Top 10 Contributing Institutions')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest value on top
plt.grid(axis='x')

# Show the plot
plt.tight_layout()
plt.show()
