from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import numpy as np
from datetime import datetime
import os
import joblib
from django.conf import settings
import pandas as pd

# Load model and mappings (do this once)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'crop_price_model.pkl')
MAPPINGS_PATH = os.path.join(settings.BASE_DIR, 'feature_mappings.pkl')

try:
    regr = joblib.load(MODEL_PATH)
    mappings = joblib.load(MAPPINGS_PATH)
except:
    regr = None
    mappings = None

# Load the trained model (you'll need to save your model first)
# regr = joblib.load('crop_price_model.pkl')

def get_season(month):
    """Convert month to season"""
    season_map = {
        1: 4, 2: 4,  # winter -> pre winter (based on your code)
        3: 3, 4: 3,  # spring
        5: 2, 6: 2,  # summer
        7: 0, 8: 0,  # monsoon
        9: 1, 10: 1, # autumn
        11: 4, 12: 4 # pre winter
    }
    return season_map.get(month, 0)

def index(request):
    """Main page with prediction form"""
    context = {
        'commodities': [
            'Rice', 'Wheat', 'Onion', 'Potato', 'Tomato', 
            'Sugar', 'Cotton', 'Maize', 'Soybean', 'Groundnut'
        ],
        'states': [
            'Karnataka', 'Maharashtra', 'Tamil Nadu', 'Andhra Pradesh',
            'Telangana', 'Gujarat', 'Rajasthan', 'Madhya Pradesh'
        ]
    }
    return render(request, 'prediction/index.html', context)

def get_districts(request):
    """AJAX endpoint to get districts based on state"""
    state = request.GET.get('state', '')
    
    # Sample district data - replace with your actual data
    districts_data = {
        'Karnataka': ['Bangalore', 'Mysore', 'Mangalore', 'Hubli', 'Belgaum'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem'],
        'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool'],
        'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar', 'Khammam'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar'],
        'Rajasthan': ['Jaipur', 'Jodhpur', 'Kota', 'Udaipur', 'Ajmer'],
        'Madhya Pradesh': ['Bhopal', 'Indore', 'Gwalior', 'Jabalpur', 'Ujjain']
    }
    
    districts = districts_data.get(state, [])
    return JsonResponse({'districts': districts})

def get_markets(request):
    """AJAX endpoint to get markets based on district"""
    district = request.GET.get('district', '')
    
    # Sample market data - replace with your actual data
    markets = [
        f'{district} Main Market',
        f'{district} Wholesale Market',
        f'{district} APMC Market',
        f'{district} Retail Market'
    ]
    
    return JsonResponse({'markets': markets})

@csrf_exempt
def predict_price(request):
    if request.method == 'POST':
        try:
            # Get form data
            commodity = request.POST.get('commodity')
            state = request.POST.get('state')
            district = request.POST.get('district')
            market = request.POST.get('market')
            image = request.FILES.get('commodity_image')
            
            # Get current date info
            current_date = datetime.now()
            month = current_date.month
            day_of_week = current_date.weekday()
            
            # Get month name
            month_names = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"]
            month_name = month_names[month - 1]
            
            # Get season
            if month_name in ["January", "February"]:
                season_name = "winter"
            elif month_name in ["March", "April"]:
                season_name = "spring"
            elif month_name in ["May", "June"]:
                season_name = "summer"
            elif month_name in ["July", "August"]:
                season_name = "monsoon"
            elif month_name in ["September", "October"]:
                season_name = "autumn"
            else:
                season_name = "pre winter"
            
            # Encode using saved mappings
            commodity_encoded = mappings['commodity'].get(commodity, 0)
            state_encoded = mappings['state'].get(state, 0)
            district_encoded = mappings['district'].get(district, 0)
            market_encoded = mappings['market'].get(market, 0)
            month_encoded = mappings['month'].get(month_name, 0)
            season_encoded = mappings['season'].get(season_name, 0)
            
            # Prepare input
            user_input = [[
                commodity_encoded,
                state_encoded,
                district_encoded,
                market_encoded,
                month_encoded,
                season_encoded,
                day_of_week
            ]]
            
            # Make prediction
            if regr is not None:
                predicted_price = regr.predict(user_input)[0]
            else:
                predicted_price = np.random.randint(1000, 5000)
            
            # Save to database (optional)
            from .models import PricePrediction
            prediction = PricePrediction.objects.create(
                commodity=commodity,
                state=state,
                district=district,
                market=market,
                predicted_price=predicted_price,
                commodity_image=image
            )
            
            return JsonResponse({
                'success': True,
                'predicted_price': round(predicted_price, 2),
                'commodity': commodity,
                'location': f"{district}, {state}",
                'market': market,
                'date': current_date.strftime('%Y-%m-%d')
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_unique_values():
    """Load unique values from CSV"""
    try:
        df = pd.read_csv('agridata.csv')
        return {
            'commodities': sorted(df['commodity_name'].unique().tolist()),
            'states': sorted(df['state'].unique().tolist()),
            'districts': sorted(df['district'].unique().tolist()),
            'markets': sorted(df['market'].unique().tolist())
        }
    except:
        return {
            'commodities': ['Rice', 'Wheat', 'Onion'],
            'states': ['Karnataka', 'Maharashtra'],
            'districts': [],
            'markets': []
        }

def index(request):
    data = get_unique_values()
    context = {
        'commodities': data['commodities'],
        'states': data['states']
    }
    return render(request, 'prediction/index.html', context)

def get_districts(request):
    state = request.GET.get('state', '')
    try:
        df = pd.read_csv('agridata.csv')
        districts = sorted(df[df['state'] == state]['district'].unique().tolist())
        return JsonResponse({'districts': districts})
    except:
        return JsonResponse({'districts': []})

def get_markets(request):
    district = request.GET.get('district', '')
    try:
        df = pd.read_csv('agridata.csv')
        markets = sorted(df[df['district'] == district]['market'].unique().tolist())
        return JsonResponse({'markets': markets})
    except:
        return JsonResponse({'markets': []})