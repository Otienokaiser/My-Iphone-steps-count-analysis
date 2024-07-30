import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Path to your XML file
file_path = 'export.xml'

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Helper function to check if a string can be converted to float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Extract relevant information
records = []

for record in root.findall('Record'):
    record_type = record.get('type')
    value = record.get('value')
    if is_float(value):
        value = float(value)
        unit = record.get('unit')
        start_date = datetime.strptime(record.get('startDate'), '%Y-%m-%d %H:%M:%S %z')
        
        records.append({
            'type': record_type,
            'value': value,
            'unit': unit,
            'start_date': start_date,
        })

df = pd.DataFrame(records)

# Filter step count records
step_counts = df[df['type'] == 'HKQuantityTypeIdentifierStepCount']

# Plot step counts over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=step_counts, x='start_date', y='value')
plt.title('Step Counts Over Time')
plt.xlabel('Date')
plt.ylabel('Step Count')
plt.xticks(rotation=45)
plt.show()
