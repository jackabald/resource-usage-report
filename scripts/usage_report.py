import pandas as pd
import matplotlib.pyplot as plt
import os

# Define file paths
data_file_path = os.path.join('..', 'data', 'status.csv')
cpu_usage_report_path = os.path.join('..', 'output', 'cpu_usage_report.pdf')
disk_usage_report_path = os.path.join('..', 'output', 'disk_usage_report.pdf')
cpu_usage_summary_path = os.path.join('..', 'output', 'cpu_usage_summary.csv')
disk_usage_summary_path = os.path.join('..', 'output', 'disk_usage_summary.csv')

# Load data, skipping the first line
data = pd.read_csv(data_file_path, skiprows=1)

# Display column names to check for discrepancies
print(data.columns)

# Ensure column names are as expected
expected_columns = ['CPU Usage', 'Disk Usage']

# Renaming columns if necessary (case-insensitive match)
data.columns = [col.strip() for col in data.columns]
col_mapping = {col.lower(): col for col in data.columns}
for expected_col in expected_columns:
    if expected_col.lower() in col_mapping:
        data[expected_col] = data[col_mapping[expected_col.lower()]]
    else:
        raise KeyError(f"Expected column '{expected_col}' not found in the dataset.")

# Preprocess data
data['CPU Usage'] = data['CPU Usage'].str.rstrip('%').astype('float')
data['Disk Usage'] = data['Disk Usage'].str.extract(r'(\d+)%')[0].astype('float')

# Use a subset of data for plotting to avoid rendering issues
data_subset = data.head(1000)  # Adjust number of rows as needed

# Generate summary statistics
cpu_usage_summary = data[['Name', 'CPU Usage']].describe()
disk_usage_summary = data[['Name', 'Disk Usage']].describe()

# Plot CPU usage
plt.figure(figsize=(10, 6))
plt.bar(data_subset['Name'], data_subset['CPU Usage'], color='blue')
plt.xlabel('Machine Name')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage for Each Machine')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(cpu_usage_report_path)
plt.show()

# Plot Disk usage
plt.figure(figsize=(10, 6))
plt.bar(data_subset['Name'], data_subset['Disk Usage'], color='green')
plt.xlabel('Machine Name')
plt.ylabel('Disk Usage (%)')
plt.title('Disk Usage for Each Machine')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(disk_usage_report_path)
plt.show()

# Save summary statistics
cpu_usage_summary.to_csv(cpu_usage_summary_path)
disk_usage_summary.to_csv(disk_usage_summary_path)

# Display summaries
print(cpu_usage_summary)
print(disk_usage_summary)
