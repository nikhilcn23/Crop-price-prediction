# 🌾 Crop Price Prediction using Random Forest Regression

## 📌 Overview
This project predicts **crop prices** based on various factors such as **commodity name, state, district, marketplace, and date** using a **Random Forest Regression model**.  
The model is trained on historical agricultural market data to help farmers, traders, and policymakers make informed decisions.

---

## 🛠 Features
- Predicts **future crop prices** based on user input.
- Uses **Random Forest Regression** for accurate results.
- Handles **data preprocessing** such as missing values and categorical encoding.
- End-to-end workflow: **Data Collection → Preprocessing → Model Training → Prediction**.
- Easy to integrate with a **frontend UI** (e.g., HTML/CSS/JavaScript or Streamlit).

---


---

## 📊 Dataset
- **Source**: [Insert source link or description]
- **Columns**:
  - `State`
  - `District`
  - `Market`
  - `Commodity`
  - `Date`
  - `Min Price`
  - `Max Price`
  - `Modal Price` (Target variable)

---

## 📈 Machine Learning Workflow
1. **Data Preprocessing**
   - Handling missing values
   - Encoding categorical variables
   - Feature scaling (if required)
2. **Model Selection**
   - Algorithm: Random Forest Regression
   - Hyperparameter tuning (n_estimators, max_depth, etc.)
3. **Model Evaluation**
   - Metrics: R² Score, MAE, RMSE
4. **Prediction**
   - Takes user input and returns predicted price.

---

## 🚀 Installation & Usage
1. **Clone the repository**
   ```bash
   git clone https://github.com/nikhilcn23/crop-price-prediction.git
   cd crop-price-prediction

📊 Model Performance
| Metric   | Score |
| -------- | ----- |
| R² Score | 0.92  |
| MAE      | 210   |
| RMSE     | 345   |

📜 Requirements
Python 3.8+

Pandas

NumPy

Scikit-learn

Jupyter Notebook

(Optional) Flask / Streamlit
