import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import defaultdict

# Define the file path
file_path = 'data.txt'

# Read the file and split into individual records
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read().strip().split('\nER\n')

# Initialize a dictionary to store country citations
country_citations = defaultdict(list)

# Process each record
for record in data:
    # Extract the C1 section
    c1_section = re.search(r'C1\s(.*?)(?=\n[A-Z0-9]|$)', record, re.DOTALL)
    if c1_section:
        c1_text = c1_section.group(1)
        lines = c1_text.strip().split('\n')
        section_countries = set()
        for line in lines:
            parts = line.split(',')
            country = parts[-1].strip()[:-1]
            if country.endswith('USA'):
                country = 'USA'
            section_countries.add(country)

        # Extract the TC section
        tc_section = re.search(r'TC\s(\d+)', record)
        if tc_section:
            citations = int(tc_section.group(1))
            for country in section_countries:
                if citations > 40 and country.find('India') >= 0:
                    print(record)
                country_citations[country].append(citations)

# Calculate the H-index for each country
def calculate_h_index(citations):
    citations.sort(reverse=True)
    h_index = 0
    for i, citation in enumerate(citations):
        if citation >= i + 1:
            h_index = i + 1
        else:
            break
    return h_index

country_h_index = {country: calculate_h_index(citations) for country, citations in country_citations.items()}

# Convert to DataFrame for easier manipulation
df = pd.DataFrame.from_dict(country_h_index, orient='index', columns=['H-index']).reset_index()
df.columns = ['Country', 'H-index']
df = df.sort_values(by='H-index', ascending=False).head(10)  # Keep only top 10 results

# Print the number of publications by country
print("Top 10 Countries by H-index:")
print(df)

# Plot the bar chart
plt.figure(figsize=(14, 8))
plt.bar(df['Country'], df['H-index'], color='skyblue')
plt.title('Top 10 Countries by H-index')
plt.xlabel('Country')
plt.ylabel('H-index')
plt.xticks(rotation=90)
plt.tight_layout()

# Show the plot
plt.show()
