import pandas as pd
import numpy as np

def calculate_atr(data, period=14):
    data['H-L'] = data['High'] - data['Low']
    data['H-PC'] = abs(data['High'] - data['Close'].shift(1))
    data['L-PC'] = abs(data['Low'] - data['Close'].shift(1))
    tr = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

# Example data for higher and lower timeframes
higher_timeframe_data = pd.DataFrame({
    'High': [110, 112, 113, 115, 116, 118, 119, 121],
    'Low': [105, 106, 107, 109, 110, 111, 113, 115],
    'Close': [108, 110, 112, 114, 115, 117, 118, 120]
})

lower_timeframe_data = pd.DataFrame({
    'High': [120, 121, 122, 123, 124, 125, 126, 127],
    'Low': [115, 116, 117, 118, 119, 120, 121, 122],
    'Close': [118, 119, 120, 121, 122, 123, 124, 125]
})

# Calculate ATR
higher_timeframe_data['ATR'] = calculate_atr(higher_timeframe_data)
lower_timeframe_data['ATR'] = calculate_atr(lower_timeframe_data)

# Determine trends (simple moving average for trend direction)
higher_timeframe_data['SMA'] = higher_timeframe_data['Close'].rolling(window=3).mean()
lower_timeframe_data['SMA'] = lower_timeframe_data['Close'].rolling(window=3).mean()

higher_trend = 'Up' if higher_timeframe_data['Close'].iloc[-1] > higher_timeframe_data['SMA'].iloc[-1] else 'Down'
lower_trend = 'Up' if lower_timeframe_data['Close'].iloc[-1] > lower_timeframe_data['SMA'].iloc[-1] else 'Down'

# Determine volatility level (simple threshold example)
higher_volatility = 'High' if higher_timeframe_data['ATR'].iloc[-1] > higher_timeframe_data['ATR'].mean() else 'Low'
lower_volatility = 'High' if lower_timeframe_data['ATR'].iloc[-1] > lower_timeframe_data['ATR'].mean() else 'Low'

# Combine information for decision
decision_table = {
    ('Up', 'Low', 'Up', 'Low'): ('Strong Buy/Continue to Hold', 'Green'),
    ('Up', 'High', 'Up', 'High'): ('Buy/Continue to Hold, but with Caution', 'Yellow'),
    ('Up', 'Low', 'Up', 'High'): ('Buy/Continue to Hold, but with Caution', 'Yellow'),
    ('Up', 'High', 'Up', 'Low'): ('Buy/Continue to Hold, but Monitor Closely', 'Yellow'),
    ('Up', 'Low', 'Down', 'Low'): ('Caution (Potential Minor Reversal)', 'Yellow'),
    ('Up', 'High', 'Down', 'High'): ('High Risk, Wait for Clear Signal', 'Yellow'),
    ('Up', 'Low', 'Down', 'High'): ('High Risk, Wait for Clear Signal', 'Yellow'),
    ('Up', 'High', 'Down', 'Low'): ('High Risk, Wait for Clear Signal', 'Yellow'),
    ('Down', 'Low', 'Up', 'Low'): ('Caution (Potential Minor Reversal)', 'Yellow'),
    ('Down', 'High', 'Up', 'High'): ('High Risk, Wait for Clear Signal', 'Yellow'),
    ('Down', 'Low', 'Up', 'High'): ('High Risk, Wait for Clear Signal', 'Yellow'),
    ('Down', 'High', 'Up', 'Low'): ('High Risk, Wait for Clear Signal', 'Yellow'),
    ('Down', 'Low', 'Down', 'Low'): ('Strong Sell/Short', 'Red'),
    ('Down', 'High', 'Down', 'High'): ('Sell/Short, but with Caution', 'Red'),
    ('Down', 'Low', 'Down', 'High'): ('Sell/Short, but with Caution', 'Red'),
    ('Down', 'High', 'Down', 'Low'): ('Sell/Short, but with Caution', 'Red')
}

decision, color = decision_table[(higher_trend, higher_volatility, lower_trend, lower_volatility)]
print(f"Decision: {decision}, Color: {color}")
