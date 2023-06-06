import pandas as pd
import random

# Define the flavors of ice cream
flavors = ['Vanilla', 'Chocolate', 'White Chocolate', 'Strawberry', 'Mint',
           'Banana', 'Coffee', 'Salted Caramel', 'Pistachio', 'Raspberry', 'Coconut', 'Birthday Cake']

# Create an empty dataframe
df = pd.DataFrame(columns=['user_id'] + flavors)

# Generate random data for the dataframe
for i in range(1000):
    row_data = [f'{i+1}'] + [1 if j in random.sample(range(len(flavors)), 4) else 0 for j in range(len(flavors))]
    df.loc[i] = row_data

# Save df to csv
df.to_csv('purchase_intent.csv', index=False)

