laptop_specs = {
    "CPU Speed (GHz)": {
        "ASUS ROG Strix": 2.6,
        "Lenovo Legion 5": 3.0,
        "HP Omen 15": 2.8,
        "MSI GF65": 2.5
    },
    "RAM (GB)": {
        "ASUS ROG Strix": 16,
        "Lenovo Legion 5": 32,
        "HP Omen 15": 16,
        "MSI GF65": 16
    },
    "Storage SSD (GB)": {
        "ASUS ROG Strix": 512,
        "Lenovo Legion 5": 1000,
        "HP Omen 15": 512,
        "MSI GF65": 256
    },
    "VRAM (GB)": {
        "ASUS ROG Strix": 8,
        "Lenovo Legion 5": 6,
        "HP Omen 15": 4,
        "MSI GF65": 6
    },
    "Display (inches)": {
        "ASUS ROG Strix": 15.6,
        "Lenovo Legion 5": 15.6,
        "HP Omen 15": 15.6,
        "MSI GF65": 15.6
    },
    "Weight (kg)": {
        "ASUS ROG Strix": 2.4,
        "Lenovo Legion 5": 2.7,
        "HP Omen 15": 2.3,
        "MSI GF65": 2.1
    }
}

# Extract model names
laptop_models = list(list(laptop_specs.values())[0].keys())
spec_categories = list(laptop_specs.keys())

# Build normalized data matrix
normalized_data_matrix = []
for model in laptop_models:
    model_values = [laptop_specs[spec][model] for spec in spec_categories]
    normalized_data_matrix.append(model_values)

def normalize_to_reference(data_matrix):
    """Normalize data relative to the first model (ASUS ROG Strix)"""
    reference_values = data_matrix[0]
    normalized = []
    for row in data_matrix:
        normalized_row = [value / ref_value for value, ref_value in zip(row, reference_values)]
        normalized.append(normalized_row)
    return normalized

def calculate_quality_scores(normalized_matrix):
    """Calculate average quality score for each laptop"""
    quality_scores = []
    for normalized_row in normalized_matrix:
        avg_score = sum(normalized_row) / len(normalized_row)
        quality_scores.append(round(avg_score, 2))
    return quality_scores

# Execute the analysis
normalized_data = normalize_to_reference(normalized_data_matrix)
quality_scores = calculate_quality_scores(normalized_data)

# Console output
print("=" * 60)
print("ОТЧЕТ О КАЧЕСТВЕ НОУТБУКА")
print("=" * 60)

print("\n📊 СЧЕТ КАЧЕСТВА (Q-score)")
print("-" * 60)
for model, score in zip(laptop_models, quality_scores):
    # Add visual indicators based on score
    if score >= 1.0:
        indicator = "Идеально"
    elif score >= 0.9:
        indicator = "Хорошо"
    elif score >= 0.8:
        indicator = "Средне"
    else:
        indicator = "Ниже среднего"
    
    print(f"{model:20} : {score:5.2f}  {indicator}")

# Find best and worst performers
best_model_idx = quality_scores.index(max(quality_scores))
worst_model_idx = quality_scores.index(min(quality_scores))

print(f"\nЛучший: {laptop_models[best_model_idx]} (Q-score: {quality_scores[best_model_idx]})")
print(f"Худший: {laptop_models[worst_model_idx]} (Q-score: {quality_scores[worst_model_idx]})")

print("\nДЕТАЛИЗИРОВАННЫЙ РАЗБОР")
print("→ - равна эталонной, ↓↓ - ниже эталонной, ↑↑ - выше эталонной")
print("-" * 60)

for i, model in enumerate(laptop_models):
    print(f"\n{model}:")
    for j, category in enumerate(spec_categories):
        value = normalized_data[i][j]
        # Add visual indicator for normalized values
        if value > 1.0:
            arrow = "↑↑"
        elif value == 1.0:
            arrow = "→"
        else:
            arrow = "↓↓"
        print(f"  {category:25} : {value:6.3f}x  {arrow}")

print("\n" + "=" * 60)
print("ИТОГ АНАЛИЗА")
print("=" * 60)

# Calculate average performance per category
print("\nСредний показатель за категорию:")
print("-" * 60)
category_averages = []
for j in range(len(spec_categories)):
    avg = sum(normalized_data[i][j] for i in range(len(laptop_models))) / len(laptop_models)
    category_averages.append(avg)
    print(f"{spec_categories[j]:25} : {avg:6.3f}x")

print("\n" + "=" * 60)