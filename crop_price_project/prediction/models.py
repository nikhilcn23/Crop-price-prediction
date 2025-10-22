from django.db import models

class CommodityPrice(models.Model):
    commodity_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    market = models.CharField(max_length=200)
    modal_price = models.FloatField()
    date = models.DateField()
    month_column = models.CharField(max_length=20)
    season_names = models.CharField(max_length=20)
    day = models.IntegerField()
    
    class Meta:
        db_table = 'commodity_prices'
        
    def __str__(self):
        return f"{self.commodity_name} - {self.district} - {self.date}"


class PricePrediction(models.Model):
    commodity = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    market = models.CharField(max_length=200)
    predicted_price = models.FloatField()
    commodity_image = models.ImageField(upload_to='commodity_images/', blank=True, null=True)
    prediction_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'price_predictions'
        ordering = ['-prediction_date']
        
    def __str__(self):
        return f"{self.commodity} - {self.predicted_price} - {self.prediction_date}"


# ========================================
# save_model.py - Run this to save your trained model
# ========================================
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load and prepare your data
df = pd.read_csv('agridata.csv')
data2 = df.copy()
data2 = data2.dropna()
data2 = data2.head(100000)

# Process date column
month_dict = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
              7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

month_column = []
for date_str in data2["date"]:
    month_num = int(date_str.split('-')[1])
    month_column.append(month_dict[month_num])

data2["month_column"] = month_column

# Create season column
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
    elif month in ["November", "December"]:
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

# Save mapping dictionaries before encoding
commodity_mapping = {val: idx for idx, val in enumerate(data2['commodity_name'].unique())}
state_mapping = {val: idx for idx, val in enumerate(data2['state'].unique())}
district_mapping = {val: idx for idx, val in enumerate(data2['district'].unique())}
market_mapping = {val: idx for idx, val in enumerate(data2['market'].unique())}
month_mapping = {val: idx for idx, val in enumerate(data2['month_column'].unique())}
season_mapping = {val: idx for idx, val in enumerate(data2['season_names'].unique())}

# Encode categorical variables
for col, mapping in [('commodity_name', commodity_mapping), 
                      ('state', state_mapping),
                      ('district', district_mapping),
                      ('market', market_mapping),
                      ('month_column', month_mapping),
                      ('season_names', season_mapping)]:
    data2[col] = data2[col].map(mapping)

# Prepare features and labels
features = data2[['commodity_name', 'state', 'district', 'market', 'month_column', 'season_names', 'day']]
labels = data2['modal_price']

# Train model
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features, labels, test_size=0.2, random_state=2)
regr = RandomForestRegressor(max_depth=1000, random_state=0, n_estimators=100)
regr.fit(Xtrain, Ytrain)

# Save model and mappings
joblib.dump(regr, 'crop_price_model.pkl')
joblib.dump({
    'commodity': commodity_mapping,
    'state': state_mapping,
    'district': district_mapping,
    'market': market_mapping,
    'month': month_mapping,
    'season': season_mapping
}, 'feature_mappings.pkl')

print("Model and mappings saved successfully!")
print(f"Model R2 Score: {regr.score(Xtest, Ytest)}")
"""