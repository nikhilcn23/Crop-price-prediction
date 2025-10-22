# 🌾 Crop Price Prediction System

A Django-based web application that predicts agricultural commodity prices using Machine Learning (Random Forest Regression). The system helps farmers, traders, and agricultural businesses make informed decisions by providing accurate price predictions based on location, commodity type, and seasonal factors.

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Model Training](#model-training)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Price Prediction**: Accurate crop price predictions using Random Forest Regression
- **Interactive UI**: User-friendly web interface with modern design
- **Location-Based**: Cascading dropdowns for State → District → Market selection
- **Image Upload**: Optional commodity image upload feature
- **Real-time Predictions**: Instant price predictions based on current date and location
- **Prediction History**: Store and track all predictions in database
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Data Visualization**: Built-in analytics and charts for price trends

## 🛠 Technologies Used

### Backend
- **Python 3.8+**
- **Django 4.x** - Web framework
- **scikit-learn** - Machine learning library
- **pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **joblib** - Model serialization

### Frontend
- **HTML5/CSS3**
- **JavaScript (Vanilla)**
- **Bootstrap** (implied in design)

### Machine Learning
- **Random Forest Regressor** - Prediction model
- **Feature Engineering** - Date, season, and location encoding
- **IQR Method** - Outlier detection and removal

### Database
- **SQLite** (Development)
- **PostgreSQL/MySQL** (Production ready)

## 💻 System Requirements

- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 500MB free space
- **OS**: Windows, macOS, or Linux

## 📥 Installation

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd crop_price_project

# Or download and extract ZIP file
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install django
pip install pandas numpy scikit-learn joblib pillow matplotlib seaborn
```

### Step 4: Project Setup

```bash
# Create Django project (if not exists)
django-admin startproject crop_price_project
cd crop_price_project

# Create Django app
python manage.py startapp prediction
```

### Step 5: Configure Settings

Edit `crop_price_project/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prediction',  # Add your app
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
```

### Step 6: Add Required Files

Place these files in the project root:
- `agridata.csv` - Your agricultural data
- `train_model.py` - Model training script
- Copy code from artifacts to:
  - `prediction/views.py`
  - `prediction/models.py`
  - `prediction/urls.py`
  - `prediction/templates/prediction/index.html`

### Step 7: Train the Model

```bash
python train_model.py
```

This will create:
- `crop_price_model.pkl` - Trained model
- `feature_mappings.pkl` - Feature encodings

### Step 8: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 9: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 10: Run the Application

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

## 📁 Project Structure

```
crop_price_project/
│
├── crop_price_project/          # Main project directory
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── prediction/                  # Django app
│   ├── migrations/              # Database migrations
│   ├── templates/
│   │   └── prediction/
│   │       └── index.html       # Main page template
│   ├── __init__.py
│   ├── admin.py                 # Admin configuration
│   ├── apps.py
│   ├── models.py                # Database models
│   ├── views.py                 # View logic
│   ├── urls.py                  # App URL routing
│   └── tests.py
│
├── media/                       # Uploaded images
│   └── commodity_images/
│
├── venv/                        # Virtual environment
│
├── agridata.csv                 # Training data
├── crop_price_model.pkl         # Trained ML model
├── feature_mappings.pkl         # Feature encodings
├── train_model.py               # Model training script
├── manage.py                    # Django management script
└── README.md                    # This file
```

## 🎯 Usage

### Making a Prediction

1. **Select Commodity**: Choose from available agricultural commodities (Rice, Wheat, Onion, etc.)

2. **Select Location**: 
   - Choose State
   - Select District (auto-populated based on state)
   - Pick Market/Taluk (auto-populated based on district)

3. **Upload Image** (Optional): Add a photo of the commodity

4. **Get Prediction**: Click "Predict Price" button

5. **View Results**: See predicted price with location and date details

### Accessing Admin Panel

1. Navigate to: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Manage predictions and data

## 🧠 Model Training

### Data Preprocessing

The model training involves several steps:

1. **Data Cleaning**: Remove null values and duplicates
2. **Date Processing**: Extract month and day of week
3. **Season Mapping**: Convert months to seasons
   - Winter: January, February
   - Spring: March, April
   - Summer: May, June
   - Monsoon: July, August
   - Autumn: September, October
   - Pre-winter: November, December
4. **Outlier Removal**: Using IQR (Interquartile Range) method
5. **Feature Encoding**: Convert categorical variables to numerical
6. **Model Training**: Random Forest Regressor with 100 estimators

### Model Performance

The model achieves good R² scores on test data, indicating reliable predictions.

### Retraining the Model

If you want to retrain with new data:

```bash
# Update agridata.csv with new data
python train_model.py
```

### Model Features

The model uses 7 features:
- Commodity name (encoded)
- State (encoded)
- District (encoded)
- Market (encoded)
- Month (encoded)
- Season (encoded)
- Day of week (0-6)

## 📸 Screenshots

### Home Page
Modern interface with gradient design and intuitive form controls.

### Prediction Result
Clear display of predicted price with location details.

### Cascading Dropdowns
Smart selection where districts and markets update based on state/district selection.

## 🔧 Troubleshooting

### Issue: Model file not found
```
Error: crop_price_model.pkl not found
```
**Solution**: Run `python train_model.py` to generate model files.

### Issue: Districts not loading
```
Districts dropdown shows "First Select State"
```
**Solution**: 
- Ensure `agridata.csv` is in project root
- Check if CSV has correct column names
- Verify state name matches exactly with CSV data

### Issue: Import errors
```
ModuleNotFoundError: No module named 'sklearn'
```
**Solution**: Install missing packages
```bash
pip install scikit-learn pandas numpy
```

### Issue: Static files not loading
**Solution**: Run collectstatic command
```bash
python manage.py collectstatic
```

### Issue: Database errors
**Solution**: Delete db.sqlite3 and run migrations again
```bash
python manage.py migrate --run-syncdb
```

### Issue: Port already in use
```
Error: That port is already in use
```
**Solution**: Use a different port
```bash
python manage.py runserver 8080
```

## 🚀 Deployment

### For Production Deployment:

1. **Update Settings**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Use Production Database**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Static Files**
   ```bash
   pip install whitenoise
   python manage.py collectstatic
   ```

4. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn crop_price_project.wsgi:application
   ```

5. **Set Up Nginx** as reverse proxy

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch 
3. Commit your changes 
4. Push to the branch 
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Multi-language support
- [ ] Export predictions to PDF/Excel
- [ ] Price trend charts and analytics
- [ ] Email notifications for price alerts
- [ ] User authentication and profiles
- [ ] Mobile application
- [ ] Real-time market price integration
- [ ] Weather data integration
- [ ] Bulk prediction upload via CSV

## Screenshots

### Homepage
![Homepage](screenshots/homepage.png)

### Prediction Result
![Prediction Resultt](screenshots/prediction resultt.png)


## 👥 Authors

- Nikhil C N

## 🙏 Acknowledgments

- Agricultural data sources
- Django community
- scikit-learn documentation
- Open source contributors


## 📊 Data Source

The agricultural price data (`agridata.csv`) should contain:
- `commodity_name`: Name of the crop
- `state`: State name
- `district`: District name
- `market`: Market/Mandi name
- `modal_price`: Price in local currency
- `date`: Date of price (YYYY-MM-DD format)

---

**Made with ❤️ for the Agricultural Community**
