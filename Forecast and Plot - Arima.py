print("\n⏳ Importing libraries⏳\n")
import pandas as pd #handles data
import matplotlib.pyplot as plt #does the plotting
from statsmodels.tsa.arima.model import ARIMA # does the forecasting

#Loading data and cleaning it
print("\n✅ Loading CSV file✅\n")
df = pd.read_csv(r"D:\Coding\btc_prices.csv", parse_dates=['Dates']) # Reads the csv file
df['Prices'] = pd.to_numeric(df['Prices'].astype(str).str.replace(',', '').str.replace('-', ''), errors='coerce') # Remove , and - from prices 
df = df.dropna(subset=['Dates', 'Prices']).sort_values('Dates').reset_index(drop=True) # Handles empty slots

print("\n⏳ Training Arima model⏳\n")
train = df.tail(120).set_index('Dates')
model = ARIMA(train['Prices'], order=(25, 2, 20)).fit() #order = (20,2,23) was good too but this one looked better :)

#Forecasting
print("\n⏳ Forecasting⏳\n")
forecast = model.forecast(steps=20)

#Plotting
future_dates = pd.date_range(train.index[-1] + pd.Timedelta(days=1), periods=20)
plt.figure(figsize=(12, 6))
plt.plot(train.index, train['Prices'], label='Historical (Last 120 Days)')
plt.plot(future_dates, forecast, 'r--', label='Forecast (Next 20 Days)')
plt.title('Bitcoin Price Forecast Using ARIMA')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
df.to_csv("cleaned_data.csv", index=False)