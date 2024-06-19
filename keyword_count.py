import re
from collections import Counter

# Function to extract keywords from DE and ID fields
def extract_keywords(data):
    de_pattern = re.compile(r'DE (.+?)(?=\n[A-Z]{2} |$)', re.DOTALL)
    id_pattern = re.compile(r'ID (.+?)(?=\n[A-Z]{2} |$)', re.DOTALL)

    de_matches = de_pattern.findall(data)
    id_matches = id_pattern.findall(data)

    keywords = []
    for match in de_matches + id_matches:
        # Remove newline characters and split by ';'
        keywords.extend(match.replace('\n', ' ').split(';'))
    # Clean up keywords
    keywords = [re.sub(r'\s+', ' ', keyword.strip().lower()) for keyword in keywords if keyword.strip()]
    return keywords

# Manually curated list to combine similar terms
curated_keywords = {
    'CNN': ['convolutional neural network', 'convolutional neural networks', 'convolution neural network', 'convolutional neural network (cnn)', 'cnn'],
    'plant disease': ['plant diseases', 'diseases', 'disease', 'disease detection', 'plant-disease'],
    'plant disease detection': ['plant-disease detection'],
    'plant': ['plants'],
	'leaf': ['leaves'],
	'leaf disease': ['leaf diseases'],
	'deep learning': ['deep    learning'],
    'neural network': ['neural networks', 'neural-network', 'neural-networks'],
    'SVM': ['support vector machine', 'support vector machines', 'svm']
    # Add more mappings as needed
}

# Create a mapping from similar terms to the curated term
term_mapping = {}
for standard_term, synonyms in curated_keywords.items():
    for synonym in synonyms:
        term_mapping[synonym] = standard_term

# Read the file
with open('data.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Extract keywords
keywords = extract_keywords(data)

# Replace similar terms with the standardized ones
standardized_keywords = [term_mapping.get(keyword, keyword) for keyword in keywords]

# Calculate the frequency of each keyword
keyword_freq = Counter(standardized_keywords)

# Get the highest frequency keywords
most_common_keywords = keyword_freq.most_common(100)  # Adjust the number as needed

# Write the highest frequency keywords to a local file
with open('top_keywords.txt', 'w', encoding='utf-8') as file:
    for keyword, freq in most_common_keywords:
        file.write(f"{keyword}: {freq}\n")

print("Top 100 high-frequency keywords have been written to top_keywords.txt.")

