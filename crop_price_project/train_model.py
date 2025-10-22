import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv('agridata.csv')
data2 = df.copy()
data2 = data2.dropna()
data2 = data2.head(100000)

# Process dates
month_dict = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
              7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

month_column = []
for date_str in data2["date"]:
    month_num = int(date_str.split('-')[1])
    month_column.append(month_dict[month_num])
data2["month_column"] = month_column

# Create seasons
season_names = []
for month in data2["month_column"]:
    if month in ["January", "February"]:
        season_names.append("winter")
    elif month in ["March", "April"]:
        season_names.append("spring")
    elif month in ["May", "June"]:
        season_names.append("summer")
    elif month in ["July", "August"]:
        season_names.append("monsoon")
    elif month in ["September", "October"]:
        season_names.append("autumn")
    else:
        season_names.append("pre winter")
data2["season_names"] = season_names

# Get day of week
day_of_week = []
for date_str in data2["date"]:
    df_temp = pd.Timestamp(date_str)
    day_of_week.append(df_temp.dayofweek)
data2["day"] = day_of_week
data2 = data2.drop('date', axis=1)

# Remove outliers
Q1 = np.percentile(data2['modal_price'], 25, interpolation="midpoint")
Q3 = np.percentile(data2['modal_price'], 75, interpolation="midpoint")
IQR = Q3 - Q1
upper = np.where(data2['modal_price'] >= (Q3 + 1.5 * IQR))
lower = np.where(data2['modal_price'] <= (Q1 - 1.5 * IQR))
data2.drop(upper[0], inplace=True)
data2.drop(lower[0], inplace=True)

# IMPORTANT: Save mappings BEFORE encoding
commodity_mapping = {val: idx for idx, val in enumerate(sorted(data2['commodity_name'].unique()))}
state_mapping = {val: idx for idx, val in enumerate(sorted(data2['state'].unique()))}
district_mapping = {val: idx for idx, val in enumerate(sorted(data2['district'].unique()))}
market_mapping = {val: idx for idx, val in enumerate(sorted(data2['market'].unique()))}
month_mapping = {val: idx for idx, val in enumerate(sorted(data2['month_column'].unique()))}
season_mapping = {val: idx for idx, val in enumerate(sorted(data2['season_names'].unique()))}

# Encode
data2['commodity_name'] = data2['commodity_name'].map(commodity_mapping)
data2['state'] = data2['state'].map(state_mapping)
data2['district'] = data2['district'].map(district_mapping)
data2['market'] = data2['market'].map(market_mapping)
data2['month_column'] = data2['month_column'].map(month_mapping)
data2['season_names'] = data2['season_names'].map(season_mapping)

# Train model
features = data2[['commodity_name', 'state', 'district', 'market', 'month_column', 'season_names', 'day']]
labels = data2['modal_price']
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features, labels, test_size=0.2, random_state=2)

regr = RandomForestRegressor(max_depth=1000, random_state=0, n_estimators=100)
regr.fit(Xtrain, Ytrain)

# Save everything
joblib.dump(regr, 'crop_price_model.pkl')
joblib.dump({
    'commodity': commodity_mapping,
    'state': state_mapping,
    'district': district_mapping,
    'market': market_mapping,
    'month': month_mapping,
    'season': season_mapping
}, 'feature_mappings.pkl')

print("✅ Model saved successfully!")
print(f"📊 Model R2 Score: {regr.score(Xtest, Ytest):.4f}")
print(f"📝 Total samples: {len(data2)}")