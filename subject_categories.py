import matplotlib.pyplot as plt
import re
from collections import Counter

# Define the file path
file_path = 'data.txt'

# Read the file and join lines correctly
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Combine lines to handle multiline fields
data = ' '.join([line.strip() for line in lines])

# Extract subject categories using regex
subject_categories = re.findall(r'WC ([\w\s,;&]+)', data)

# Flatten the list and split multiple categories, truncate after 'WE' if it appears
subject_categories_flat = []
for sublist in subject_categories:
    for category in re.split(r';\s*', sublist):
        truncated_category = category.split(' WE')[0].strip()  # Truncate after 'WE'
        subject_categories_flat.append(truncated_category)

# Count the occurrences of each category
category_counter = Counter(subject_categories_flat)

# Get the top 10 most common categories
top_10_categories = category_counter.most_common(10)

# Print the top 10 category counts
print("Top 10 Most Frequent Subject Categories:")
for category, count in top_10_categories:
    print(f"{category}: {count}")

# Plot the bar chart for top 10 categories
categories, counts = zip(*top_10_categories)

plt.figure(figsize=(10, 6))
plt.bar(categories, counts)
plt.title('Top 10 Most Frequent Subject Categories')
plt.xlabel('Subject Category')
plt.ylabel('Number of Publications')
plt.grid(True)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Show the plot
plt.show()
