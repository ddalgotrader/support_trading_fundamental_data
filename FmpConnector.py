import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class FmpConnector():
    
    '''
    Descritpion
    ============================================
    
    Python module downloading data from https://site.financialmodelingprep.com/ and converting
    to pandas df format
    
    Attributes
    ============================================
    
    apikey - apikey from https://site.financialmodelingprep.com/ account
    
    Methods
    ============================================
    
    get_company_info - return info about given company from chosen category
    
    get_financial_data - return financial data, statements for given company from given period
    
    get_instruments - return all available instruments of given type
    
    get_daily_prices - return daily prices of given instrument from whole available time period
    
    get_market_news - return news for given instrument from given period of time
    
    get_sentiment - return historical social sentiment for given stock company
    
    draw_chart - return plotly figure with chart for defined kind
    
    '''
    
    def __init__(self, apikey):
        
        self.apikey=apikey
        test_endpoint=f'https://financialmodelingprep.com/api/v3/profile/AAPL?apikey={self.apikey}'
        response=requests.get(test_endpoint)
        if response.status_code==200:
            print('Connected')
        
        else:
            print(response.json())
       
    def __repr__(self):
        
        return 'FmpConnector module'
    
    def get_company_info(self, symbol, limit=10, info_type='company_profile'):
        
        '''
        Description
        ============================================
        Return info about given company from chosen category
        
        Parameters
        ============================================
        *symbol -> str
        info_type -> str{company_profile, company_rating, historical_rating, recommendations}, default: company_profile
        limit -> number - required only for historical_rating and recommendations info type, default: 10
        
        Returns
        ============================================
        pandas dataframe
        
        '''
        
        company_info_dict={'company_profile':f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={self.apikey}',
                          'company_rating':f'https://financialmodelingprep.com/api/v3/rating/{symbol}?apikey={self.apikey}',
                          'historical_rating':f'https://financialmodelingprep.com/api/v3/historical-rating/{symbol}?limit={limit}&apikey={self.apikey}',
                        'recommendations':f'https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/{symbol}?limit={limit}&apikey={self.apikey}'}
        
        data=None
        df=pd.DataFrame()
        try:
            endpoint=company_info_dict[info_type]
            data=requests.get(endpoint).json()
            
        
        except KeyError:
            print(f"'{info_type}' is not valid info_type - choose info type from possible options [company_profile, company_rating, historical_rating, recommendations]")
            
        try:
            if info_type not in ['historical_rating', 'recommendations']:
                df=pd.DataFrame.from_dict(data).T
                df=df.rename(columns={0:'info'})
            else:
                df=pd.DataFrame.from_dict(data)
        except ValueError:
            print(data)
        
        return df
    
    def get_financial_data(self, symbol, report_type='balance_statement', period='annual', limit=10, as_reported=False):
        '''
        Description
        ============================================
        Return financial data, statements for given company from given period
        
        Parameters
        ============================================
        *symbol -> str
        report_type -> str{balance_statement, income_statement, cashflow_statement, full_statement}, default: balance_statement
        period -> str{annual, quarter}, default: annual
        limit -> number, default: 10
        as_reported -> boolean{True, False}, default: False
        
        
        Returns
        ============================================
        pandas dataframe
        
        '''
        
        report_type_dict={'balance_statement':[f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?period={period}&limit={limit}&apikey={self.apikey}',
                                              f'https://financialmodelingprep.com/api/v3/balance-sheet-statement-as-reported/{symbol}?period={period}&limit={limit}&apikey={self.apikey}'],
                         'income_statement':[f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period={period}&limit={limit}&apikey={self.apikey}',
                                            f'https://financialmodelingprep.com/api/v3/income-statement-as-reported/{symbol}?period={period}&limit={limit}&apikey={self.apikey}'],
                         'cashflow_statement':[f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?period={period}&limit={limit}&apikey={self.apikey}',
                                              f'https://financialmodelingprep.com/api/v3/cash-flow-statement-as-reported/{symbol}?period={period}&limit={limit}&apikey={self.apikey}'],
                         'full_statement':[f'https://financialmodelingprep.com/api/v3/financial-statement-full-as-reported/{symbol}?period={period}&limit={limit}&apikey={self.apikey}']}
        
        if period not in ['annual', 'quarter']:
            print(f"'{period}' is not valid option for period - choose from possible options [annual, quarter]")
            return 0
        
        
        
        data=None
        df=pd.DataFrame()
        try:
            endpoint=report_type_dict[report_type][0]
            if (as_reported==True) & (report_type!='full_statement'):
                endpoint=report_type_dict[report_type][1]
            data=requests.get(endpoint).json()
            
        
        except KeyError:
            print(f"'{report_type}' is not valid report_type - choose info type from possible options [balance_statement, income_statement, cashflow_statement, full_statement]")
        
        try:
            
            df=pd.DataFrame.from_dict(data)
            df=df.rename(columns={0:'info'})
           
        except ValueError:
            print(data)
        
        return df
           
    def get_instruments(self, asset_type):
        '''
        Description
        ============================================
        Return all available instruments of given type
        
        Parameters
        ============================================
        *asset_type -> str{'forex','stock','crypto','commodities'}
        
        Returns
        ============================================
        pandas dataframe
        
        '''
        
        
        asset_type_dict={'forex':f'https://financialmodelingprep.com/api/v3/symbol/available-forex-currency-pairs?apikey={self.apikey}',
                        'stock':f'https://financialmodelingprep.com/api/v3/stock/list?apikey={self.apikey}',
                         'commodities':f'https://financialmodelingprep.com/api/v3/symbol/available-commodities?apikey={self.apikey}',
                         'crypto':f'https://financialmodelingprep.com/api/v3/symbol/available-cryptocurrencies?apikey={self.apikey}'}
        
        data=None
        df=pd.DataFrame
        try:
            
            endpoint=asset_type_dict[asset_type]
            data=requests.get(endpoint).json()
            
        
        except KeyError:
            print(f"'{asset_type}' is not valid asset_type - choose info type from possible options [forex, stock, crypto, commodities]")
        
        try:
            df=pd.DataFrame.from_dict(data)
        except ValueError:
            print(data)
        
        return df
        
        
    def get_daily_prices(self, symbol):
        
        '''
        Description
        ============================================
        Return all available daily prices for given instrument
        
        Parameters
        ============================================
        
        *symbol -> str - symbol of given instrument
        
        Returns
        ============================================
        pandas dataframe
        
        '''
            
        endpoint=f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={self.apikey}'
        data=requests.get(endpoint).json()
        df=pd.DataFrame()
        try:
            df=pd.DataFrame.from_dict(data['historical'])
        
        except ValueError:
            print(data)
        df.attrs['instrument']=symbol
        df['date']=pd.to_datetime(df['date'])
        df=df.set_index('date')
        return df
    
    def get_market_news(self, market_type, symbol=None, limit=10):
        
        '''
        Description
        ============================================
        Return news for given instrument from given period of time
        
        Parameters
        ============================================
        
        symbols ->  - symbol of given instrument, default: None
        *market_type -> str{'stock','forex','crypto'} 
        limit -> number, default: 10
        
        Returns
        ============================================
        pandas dataframe
        
        '''
        
        market_type_dict={'stock':[f'https://financialmodelingprep.com/api/v3/stock_news?limit={limit}&apikey={self.apikey}',
                                   f'https://financialmodelingprep.com/api/v3/stock_news?tickers={symbol}&limit={limit}&apikey={self.apikey}'],
                          'forex':[f'https://financialmodelingprep.com/api/v4/forex_news?limit={limit}&apikey={self.apikey}',
                                   f'https://financialmodelingprep.com/api/v4/forex_news?symbol={symbol}&limit={limit}&apikey={self.apikey}'],
                          'crypto':[f'https://financialmodelingprep.com/api/v4/crypto_news?limit={limit}&apikey={self.apikey}',
                                    f'https://financialmodelingprep.com/api/v4/crypto_news?symbol={symbol}&limit={limit}&apikey={self.apikey}',]}
        
        
        data=None
        df=pd.DataFrame
        try:
            endpoint=market_type_dict[market_type][0]
            if symbol!=None:
                endpoint=market_type_dict[market_type][1]
            data=requests.get(endpoint).json()
            
        
        except KeyError:
            print(f"'{market_type}' is not valid market_type - choose info type from possible options [stock,forex,crypto]")
        
        try:
            df=pd.DataFrame.from_dict(data)
        except ValueError:
            print(data)
        
        return df
        
    def get_sentiment(self, symbol, limit=10):
        '''
        Description
        ============================================
        Return historical social sentiment for given stock company
        
        Parameters
        ============================================
        *symbol -> str
        limit -> number, default:10
        
        
        Returns
        ============================================
        pandas dataframe
        '''
        
        endpoint=f'https://financialmodelingprep.com/api/v4/historical/social-sentiment?symbol={symbol}&limit={limit}&apikey={self.apikey}'
        data=requests.get(endpoint).json()
        df=pd.DataFrame()
        try:
            df=pd.DataFrame.from_dict(data)
        except ValueError:
            print(data)
        
        return df
        
    def draw_chart(self, df, start=None, end=None, chart_type='candle'):
        '''
        Description
        ============================================
        Return plotly figure with chart for defined kind
        
        Parameters
        ============================================
        *df -> pandas dataframe - required columns to plot candle chart and ohlc chart:{date, open, high, low, close,volume}
                                 required columns to plot line chart:{date, close, volume}
        start -> str in format 'yyyy-MM-dd', default: None
        end -> str in format 'yyyy-MM-dd', default: None
        chart_type -> str{'candle','line','ohlc'}, default: candle
        
        
        Returns
        ============================================
        plotly figure
        '''
        
        if chart_type not in ['candle','line','ohlc']:
            print(f"'{chart_type}' is not valid option for chart_type - choose from possible options ['candle','line','ohlc']")
            return 0
        start_to_plot=df.index[0]
        end_to_plot=df.index[-1]
        
        df_plot=None
        if ((start!=None) & (end==None)):
            df_plot=df.loc[start:]
            start_to_plot=start
        elif ((end!=None) & (start==None)):
            df_plot=df.loc[:end]
            end_to_plot=end
        elif ((end!=None) & (start!=None)):
            df_plot=df.loc[start:end]
            start_to_plot=start
            end_to_plot=end
        else:
            df_plot=df
        
        symbol=df_plot.attrs['instrument']
        interval='daily'
        if 'interval' in list(df_plot.attrs.keys()):
            interval=df_plot.attrs['interval']
        
        title=f'|CHART TYPE: {chart_type} |SYMBOL: {symbol} |INTERVAL: {interval} |START: {start_to_plot} |END: {end_to_plot}'
        figure=make_subplots(rows=2, cols=1, row_heights=[0.8,0.2], shared_xaxes=True,
                        vertical_spacing=0.01)
        figure.update_layout(height=800)
        figure.add_trace(go.Bar(x=df_plot.index,y=df_plot['volume'], name='volume', marker_color='blue'), row=2, col=1)
        
            
            
        if chart_type=='candle':
            
            figure.add_trace(go.Candlestick(x=df_plot.index,
                    open=df_plot['open'],
                    high=df_plot['high'],
                    low=df_plot['low'],
                    close=df_plot['close'],
                    name=df_plot.attrs['instrument']), row=1, col=1)

        elif chart_type=='line':
            
            figure.add_trace(go.Scatter(x=df_plot.index,y=df_plot['close'],name=df_plot.attrs['instrument']), row=1, col=1)
            
        
        elif chart_type=='ohlc':
            
             figure.add_trace(go.Ohlc(x=df_plot.index,
                    open=df_plot['open'],
                    high=df_plot['high'],
                    low=df_plot['low'],
                    close=df_plot['close'],
                    name=df_plot.attrs['instrument']), row=1, col=1)
        figure.update_layout(title=title,xaxis_rangeslider_visible=False)
        figure.update_xaxes(rangebreaks=[dict(bounds=['sat', 'mon'])])
        figure.show()
        
        
        
        
        
    
