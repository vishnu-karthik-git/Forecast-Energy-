#  Price Forecasting and Battery Scheduling Project

## Project Overview

This project focuses on forecasting day-ahead electricity prices and using these forecasts to optimize the scheduling of a battery energy storage system (BESS). The workflow follows a complete data-driven decision-making pipeline, from data collection to profit evaluation.

---

## Tasks Completed

### 1. **Data Collection & Preparation**

* Selected at least one full year of historical **day-ahead electricity price data**.
* Cleaned and formatted the dataset for model training.
* Gathered additional relevant features *(if applicable)* such as:

  * Load demand
  * Renewable generation
---

### 2. **Day-Ahead Price Forecasting**

* Built a forecasting model using course-approved methods (e.g. Linear Regression ).
* Trained the model on the prepared dataset.

---

### 3. **Model Evaluation**

* Implemented a **validation strategy** (e.g. rolling window / train-test split).
* Evaluated prediction accuracy on a **held-out test set** using error metrics such as:

  * MAE (Mean Absolute Error)
  * RMSE (Root Mean Squared Error)

---

### 4. **Battery Dispatch Optimization**

* Applied the **provided optimizer** to schedule battery charging and discharging.
* Two scenarios were analyzed:

  1. **Forecast-based dispatch** (using the model predictions)
  2. **Perfect-foresight dispatch** (using actual future prices)

---

### 5. **Profit Comparison & Analysis**

* Calculated total operational profit for both scenarios.
* Quantified **profit loss due to forecast error**.
* Assessed the economic impact of forecasting accuracy on storage system performance.


## Conclusion

This project demonstrates how forecast accuracy directly affects energy trading profitability. By comparing forecast-based and perfect-foresight scenarios, we highlight the **value of reliable price prediction** in real-world battery operations.

---
