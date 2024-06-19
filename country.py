import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter

# Define the file path
file_path = 'data.txt'

# Read the file
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Extract C1 sections using a regex pattern
c1_sections = re.findall(r'C1\s(.*?)(?=\n[A-Z0-9]|$)', data, re.DOTALL)

# Extract country names from C1 sections
countries = []
for section in c1_sections:
    # Split the section by lines
    lines = section.split('\n')
    section_countries = set()  # Use a set to avoid counting duplicates in the same section
    for line in lines:
        parts = line.split(',')
        country = parts[-1].strip()[:-1]
        if country.endswith('USA'):
            country = 'USA'
        section_countries.add(country)
    countries.extend(section_countries)  # Add the unique countries for this section to the main list

# Count the number of publications by country
country_counts = Counter(countries)

# Convert to DataFrame for easier manipulation
df = pd.DataFrame.from_dict(country_counts, orient='index', columns=['Count']).reset_index()
df.columns = ['Country', 'Count']
df = df.sort_values(by='Count', ascending=False).head(10)  # Keep only top 10 results

# Print the number of publications by country
print("Top 10 Countries by Number of Publications:")
print(df)

# Plot the bar chart
plt.figure(figsize=(14, 8))
plt.bar(df['Country'], df['Count'], color='skyblue')
plt.title('Number of Publications by Country (Top 10)')
plt.xlabel('Country')
plt.ylabel('Number of Publications')
plt.xticks(rotation=90)
plt.tight_layout()

# Show the plot
plt.show()
