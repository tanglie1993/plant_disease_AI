import matplotlib.pyplot as plt
import pandas as pd
import re

# Define the file path
file_path = 'data.txt'

# Read the file and join lines correctly
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Combine lines to handle multiline fields
data = ' '.join([line.strip() for line in lines])

# Extract subject categories using regex, ensuring to exclude WE fields
subject_categories = re.findall(r'WC ([\w\s,;&]+)', data)
for c in subject_categories:
	print(c)
	if c.find('WE ')> 0:
		print(data)

# Flatten the list and split multiple categories
subject_categories_flat = [category.strip() for sublist in subject_categories for category in re.split(r';\s*', sublist)]

# Filter out non-subject category entries that might be included mistakenly
subject_categories_flat = [category for category in subject_categories_flat if category and ' ' not in category]

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(subject_categories_flat, columns=['Category'])

# Count the number of occurrences of each category
category_counts = df['Category'].value_counts().head(10)

# Print the top 10 category counts
print("Top 10 Most Frequent Subject Categories:")
print(category_counts)

# Plot the bar chart for top 10 categories
plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar')
plt.title('Top 10 Most Frequent Subject Categories')
plt.xlabel('Subject Category')
plt.ylabel('Number of Publications')
plt.grid(True)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Show the plot
plt.show()
