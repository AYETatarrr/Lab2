import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

rcParams['font.family'] = 'DejaVu Sans'

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

laptop_models = list(list(laptop_specs.values())[0].keys())
spec_categories = list(laptop_specs.keys())

normalized_data_matrix = []
for model in laptop_models:
    model_values = [laptop_specs[spec][model] for spec in spec_categories]
    normalized_data_matrix.append(model_values)


def normalize_to_reference(data_matrix):
    reference_values = data_matrix[0]
    normalized = []
    for row in data_matrix:
        normalized_row = [value / ref_value for value, ref_value in zip(row, reference_values)]
        normalized.append(normalized_row)
    return normalized


def calculate_quality_scores(normalized_matrix):
    quality_scores = []
    for normalized_row in normalized_matrix:
        avg_score = sum(normalized_row) / len(normalized_row)
        quality_scores.append(round(avg_score, 2))
    return quality_scores


normalized_data = normalize_to_reference(normalized_data_matrix)
quality_scores = calculate_quality_scores(normalized_data)

print("=" * 60)
print("ОТЧЕТ О КАЧЕСТВЕ НОУТБУКА")
print("=" * 60)

print("\n📊 СЧЕТ КАЧЕСТВА (Q-score)")
print("-" * 60)
for model, score in zip(laptop_models, quality_scores):
    if score >= 1.0:
        indicator = "Идеально"
    elif score >= 0.9:
        indicator = "Хорошо"
    elif score >= 0.8:
        indicator = "Средне"
    else:
        indicator = "Ниже среднего"

    print(f"{model:20} : {score:5.2f}  {indicator}")

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

print("\nСредний показатель за категорию:")
print("-" * 60)
category_averages = []
for j in range(len(spec_categories)):
    avg = sum(normalized_data[i][j] for i in range(len(laptop_models))) / len(laptop_models)
    category_averages.append(avg)
    print(f"{spec_categories[j]:25} : {avg:6.3f}x")

print("\n" + "=" * 60)

# ============= ГЕНЕРАЦИЯ ДИАГРАММ =============

# Диаграмма 1: Гистограмма Q-score для всех ноутбуков
fig, ax = plt.subplots(figsize=(12, 6))

# Создаем цвета на основе значений Q-score
colors = []
for score in quality_scores:
    if score >= 1.0:
        colors.append('#2ecc71')  # зеленый - отлично
    elif score >= 0.9:
        colors.append('#3498db')  # синий - хорошо
    elif score >= 0.8:
        colors.append('#f39c12')  # оранжевый - средне
    else:
        colors.append('#e74c3c')  # красный - плохо

bars = ax.bar(laptop_models, quality_scores, color=colors, edgecolor='black', linewidth=1.5)

# Добавляем значения на столбцы
for bar, score in zip(bars, quality_scores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2., height + 0.01,
            f'{score:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Настройка графика
ax.set_ylabel('Q-score (качество)', fontsize=12, fontweight='bold')
ax.set_title('Сравнение качества ноутбуков\n(относительно ASUS ROG Strix)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_ylim(0, max(quality_scores) + 0.15)
ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=2, alpha=0.7, label='Эталон (ASUS ROG Strix)')
ax.legend(loc='upper right')
ax.grid(axis='y', alpha=0.3)

# Поворачиваем подписи для лучшей читаемости
plt.xticks(rotation=15, ha='right')
plt.tight_layout()

# Сохраняем диаграмму
plt.savefig('quality_scores_chart.png', dpi=300, bbox_inches='tight')
print("\n Диаграмма 1 сохранена как 'quality_scores_chart.png'")
plt.show()

# Диаграмма 2: Тепловая карта нормализованных характеристик
fig, ax = plt.subplots(figsize=(12, 8))

# Подготовка данных для тепловой карты
data_array = np.array(normalized_data)
# Транспонируем для удобства отображения (характеристики по вертикали, модели по горизонтали)
data_for_heatmap = data_array.T

# Создаем тепловую карту
im = ax.imshow(data_for_heatmap, cmap='RdYlGn', aspect='auto', vmin=0.5, vmax=2.0)

# Настройка осей
ax.set_xticks(np.arange(len(laptop_models)))
ax.set_yticks(np.arange(len(spec_categories)))
ax.set_xticklabels(laptop_models, rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(spec_categories, fontsize=10)

# Добавляем значения в ячейки
for i in range(len(spec_categories)):
    for j in range(len(laptop_models)):
        value = data_for_heatmap[i, j]
        # Выбираем цвет текста в зависимости от фона
        text_color = 'white' if value < 0.85 or value > 1.6 else 'black'
        ax.text(j, i, f'{value:.2f}x', ha='center', va='center',
                color=text_color, fontsize=9, fontweight='bold')

# Добавляем цветовую шкалу
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Нормализованное значение (относительно эталона)', fontsize=10, fontweight='bold')

# Настройка заголовка и внешнего вида
ax.set_title('Тепловая карта характеристик ноутбуков\n(зеленый = выше эталона, красный = ниже эталона)',
             fontsize=14, fontweight='bold', pad=20)

# Добавляем аннотации для веса (обратная шкала)
ax.text(0, -1.5, 'Примечание: для веса (Weight) ↑↑ означает легче (лучше)',
        fontsize=9, style='italic', ha='left')

plt.tight_layout()

# Сохраняем диаграмму
plt.savefig('heatmap_normalized_specs.png', dpi=300, bbox_inches='tight')
print(" Диаграмма 2 сохранена как 'heatmap_normalized_specs.png'")
plt.show()

# Диаграмма 3 (дополнительная): Радарная диаграмма для сравнения профилей
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

# Количество характеристик
N = len(spec_categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Замыкаем круг

# Добавляем веса с обратной нормализацией (меньше вес = лучше)
spec_categories_with_note = [cat + ('*' if cat == 'Weight (kg)' else '') for cat in spec_categories]

for i, model in enumerate(laptop_models):
    values = normalized_data[i]
    # Для веса инвертируем значение (чем меньше вес, тем лучше)
    values_with_inv = values.copy()
    weight_idx = spec_categories.index('Weight (kg)')
    values_with_inv[weight_idx] = 1 / values_with_inv[weight_idx] if values_with_inv[weight_idx] > 0 else 1
    values_with_inv += values_with_inv[:1]  # Замыкаем круг

    ax.plot(angles, values_with_inv, 'o-', linewidth=2, label=model, markersize=6)
    ax.fill(angles, values_with_inv, alpha=0.1)

# Настройка радиальной диаграммы
ax.set_xticks(angles[:-1])
ax.set_xticklabels(spec_categories_with_note, fontsize=10)
ax.set_ylim(0, 2.2)
ax.set_yticks([0.5, 1.0, 1.5, 2.0])
ax.set_yticklabels(['0.5x', '1.0x', '1.5x', '2.0x'], fontsize=9)
ax.grid(True)
ax.set_title('Радарная диаграмма характеристик\n(относительно эталона ASUS ROG Strix)',
             fontsize=14, fontweight='bold', pad=20)

# Добавляем легенду
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=9)

# Добавляем примечание
plt.figtext(0.5, -0.05, '* для веса отображено обратное значение (чем выше, тем лучше)',
            ha='center', fontsize=9, style='italic')

plt.tight_layout()
plt.savefig('radar_chart.png', dpi=300, bbox_inches='tight')
print(" Диаграмма 3 (радарная) сохранена как 'radar_chart.png'")
plt.show()

print("\n" + "=" * 60)
print(" ВСЕ ДИАГРАММЫ УСПЕШНО СОЗДАНЫ!")
print("=" * 60)
print("Созданные файлы:")
print("  1. quality_scores_chart.png - Гистограмма Q-score")
print("  2. heatmap_normalized_specs.png - Тепловая карта характеристик")
print("  3. radar_chart.png - Радарная диаграмма для сравнения профилей")
print("=" * 60)