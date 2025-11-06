import pandas as pd

data = {
    'Category': ['User satisfaction', 'Product stability', 'Fix reactivity', 'Documentation',
                 'Policy adherence', 'FAT practices', 'UAT practices', 'Static quality',
                 'Unit coverage', 'Automation practices'],
    '2022': [0.68, 0.48, 0.79, 0.98, 1.00, 0.57, 0.00, 0.62, 0.37, 0.97],
    '2023': [0.48, 0.58, 0.89, 0.88, 0.60, 0.77, 0.40, 0.82, 0.17, 0.07],
    '2024': [0.18, 0.58, 0.79, 0.78, 0.80, 0.67, 0.20, 0.42, 0.77, 0.47],
    '2025': [0.28, 0.68, 0.84, 0.90, 0.70, 0.47, 0.10, 0.62, 0.37, 0.97]
}
df = pd.DataFrame(data)

x_axis = df.columns.drop('Category').tolist()
y_axis = df['Category'].tolist()

print(x_axis)
print(y_axis)

for i in x_axis[2::1]:
    value = df[i].tolist()
    print(value)