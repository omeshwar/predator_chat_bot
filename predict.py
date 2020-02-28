#from alpha_vantage.timeseries import TimeSeries
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
#apikey='4EWAGGPCYI53F188'
#ts = TimeSeries(key=apikey, output_format='csv')

#data, meta_data =data, meta_data =ts.get_daily(symbol='NSE:ONGC') #ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full') 

data = pd.read_csv('sbifull.csv')

date = data['timestamp']
data = data[['close','volume','high','low','open']] 

# A variable for predicting 'n' days out into the future
forecast_out = 5 #'n=30' days
#Create another column (the target ) shifted 'n' units up
data['Prediction'] = data[['high']].shift(-forecast_out)
#print the new data set


X = np.array(data.drop(['Prediction'],1))

#Remove the last '30' rows
X = X[:-forecast_out]
print(X)

y = np.array(data['Prediction'])
# Get all of the y values except the last '30' rows
y = y[:-forecast_out]


x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.001)

svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1) 
svr_rbf.fit(x_train, y_train)

svm_confidence = svr_rbf.score(x_test, y_test)
print("svm confidence: ", svm_confidence)

lr = LinearRegression()
# Train the model
lr.fit(x_train, y_train)

lr_confidence = lr.score(x_test, y_test)
print("lr confidence: ", lr_confidence)

x_forecast = np.array(data.drop(['Prediction'],1))[:forecast_out]
print(x_forecast)

lr_prediction = lr.predict(x_forecast)
print(lr_prediction)# Print support vector regressor model predictions for the next '30' days
svm_prediction = svr_rbf.predict(x_forecast)
print(svm_prediction)