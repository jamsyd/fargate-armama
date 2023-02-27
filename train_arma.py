def trainModel(ticker,payload):

    import os
    import sys


    import numpy as np
    import pandas as pd

    import yfinance as yf
    import awswrangler as wr

    from datetime import datetime
    from statsmodels.tsa.arima.model import ARIMA

    cacheForecasts = {

        'pointForecast':[],
        'positionType':[],
        'product_name':[ticker]*payload['forecastHorizon'],
        'strategy_name':['arma_ma']*payload['forecastHorizon'],
        'forecastDay':[i for i in range(1,1+payload['forecastHorizon'])],
        'forecastDiff':[],
        'maDiff':[],
        'percDiff':[],
        'retScore':[],

    }
    # reading in the dataframe
    ticker = yf.Ticker(ticker)
    dataframe = ticker.history(period="5y")

    # calculating the log difference
    diff = np.log(dataframe[payload['column']]).diff(1)

    # training a single model
    mod = ARIMA(diff[-252:], order=payload['order'])
    res = mod.fit()

    # generating forecasts
    fcast = res.forecast(payload['forecastHorizon'])
    fcast = (np.exp(fcast.reset_index()['predicted_mean']) - 1).cumsum() + 1
    rescaled_fcast = fcast*dataframe[payload['column']].iloc[-1]

    # store the results
    cacheForecasts['pointForecast'] = rescaled_fcast.to_list()

    # diffs
    ma_diff = dataframe[payload['column']].rolling(50).mean().diff(1).reset_index()[payload['column']].iloc[-1]
    po_diff = (rescaled_fcast.iloc[-1] - dataframe[payload['column']].iloc[-1])

    perc_return = 100*po_diff/dataframe[payload['column']].iloc[-payload['forecastHorizon']]
    ret_score   = np.abs(po_diff/np.std(np.exp(np.log(dataframe[payload['column']]).diff(1))))


    if (po_diff) > 0 and (ma_diff > 0):
        for i in range(1,1+payload['forecastHorizon']):
            cacheForecasts['positionType'].append('long')

    elif (po_diff <= 0) and (ma_diff <= 0):
        for i in range(1,1+payload['forecastHorizon']):
            cacheForecasts['positionType'].append('short')

    else:
        for i in range(1,1+payload['forecastHorizon']):
            cacheForecasts['positionType'].append('no_position')

    for i in range(1,1+payload['forecastHorizon']):
        cacheForecasts['forecastDiff'].append(po_diff)
        cacheForecasts['maDiff'].append(ma_diff)
        cacheForecasts['percDiff'].append(perc_return)
        cacheForecasts['retScore'].append(ret_score)

    wr.s3.to_csv(
        df=pd.DataFrame(cacheForecasts),
        path=f's3://jamsyd-arma-ma/forecasts/{ticker}.csv',
    )
