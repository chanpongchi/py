
import webbrowser
import os, time
import pandas as pd
import yahoo_finance_pynterface as yahoo
import datetime as dt
from datetime import datetime, timedelta
import subprocess
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objs import *
import pandas_datareader as web



pd.set_option('display.max_columns', None)
pd.set_option('display.width', 600)
pd.set_option('display.max_rows', None)
#INPUT STOCK
#id="0388.HK"
id="GC=F"
stockslv="SI=F"
#baseid=input("INPUT INDEX :     ")
#baseid="^HSI"

#DATE
#days="2008-01-01"
days=input("Date from  :     ")
webbrowser.open("https://goldprice.org/zh-hant", new=2)


end=(dt.datetime.now() + dt.timedelta(1)).strftime("%Y-%m-%d")
stock =id
today=end


#GET STOCK DATA
#yahoo.Get.Info()
#datab = yahoo.Get.Prices(stock,period=[days,end])
datab = web.DataReader(stock, data_source='yahoo', start = days, end = end) #name為股票代號名稱 start、end為資料下載期間


datab.index = pd.to_datetime(datab.index).strftime("%Y-%m-%d")
datab.index=pd.to_datetime(datab.index)
datab= datab.replace(0, np.nan)
datab=datab.dropna()
df=datab

datab["std"]=round(datab["Close"].rolling(30,min_periods=1).std(),2)
datab["mean"]=round(datab["Close"].rolling(30,min_periods=1).mean(),2)
datab["addstd"]=datab["mean"]+datab["std"]+datab["std"]
datab["lessstd"]=datab["mean"]-datab["std"]-datab["std"]
datab=datab.dropna()

returns_df_d=datab["Close"].pct_change(periods=1)
#returns_df_d=stockmthtable
returns_df_m = pd.DataFrame((returns_df_d + 1).resample('M').prod() - 1)
returns_df_m['Month'] = returns_df_m.index.month
returns_df_m.columns=[stock,'Month']
monthly_table = returns_df_m[[stock,'Month']].pivot_table(returns_df_m[[stock,'Month']], index=returns_df_m.index, columns='Month', aggfunc=np.sum).resample('A')
monthly_table = monthly_table.aggregate('sum')
monthly_table.columns = monthly_table.columns.droplevel()
#replace full date in index column with just the correspnding year
monthly_table.index = monthly_table.index.year
monthly_table['YTD'] = ((monthly_table + 1).prod(axis=1) - 1)
monthly_table = round(monthly_table * 100,3)
#Replace integer column headings with MMM format
monthly_table.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','YTD']
print("-----------------------------------------------------------------------------------------------")
print(stock + "  Monthly return")
print(monthly_table)

gldtable=datab

datab = web.DataReader(stockslv, data_source='yahoo', start = days, end = end) #name為股票代號名稱 start、end為資料下載期間

#datab = yahoo.Get.Prices(stockslv,period=[days,end])
datab.index = pd.to_datetime(datab.index).strftime("%Y-%m-%d")
datab.index=pd.to_datetime(datab.index)
datab= datab.replace(0, np.nan)
datab=datab.dropna()
df=datab

datab["std"]=round(datab["Close"].rolling(30,min_periods=1).std(),2)
datab["mean"]=round(datab["Close"].rolling(30,min_periods=1).mean(),2)
datab["addstd"]=datab["mean"]+datab["std"]+datab["std"]
datab["lessstd"]=datab["mean"]-datab["std"]-datab["std"]
datab=datab.dropna()

returns_df_d=datab["Close"].pct_change(periods=1)
#returns_df_d=stockmthtable
returns_df_m = pd.DataFrame((returns_df_d + 1).resample('M').prod() - 1)
returns_df_m['Month'] = returns_df_m.index.month
returns_df_m.columns=[stock,'Month']
monthly_table = returns_df_m[[stock,'Month']].pivot_table(returns_df_m[[stock,'Month']], index=returns_df_m.index, columns='Month', aggfunc=np.sum).resample('A')
monthly_table = monthly_table.aggregate('sum')
monthly_table.columns = monthly_table.columns.droplevel()
#replace full date in index column with just the correspnding year
monthly_table.index = monthly_table.index.year
monthly_table['YTD'] = ((monthly_table + 1).prod(axis=1) - 1)
monthly_table = round(monthly_table * 100,3)
#Replace integer column headings with MMM format
monthly_table.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','YTD']
print("-----------------------------------------------------------------------------------------------")
print(stock + "  Monthly return")
print(monthly_table)
slvtable=datab

gldtable['silver']=slvtable['Close'].copy()
gldtable['gsratio']=gldtable['Close']/gldtable['silver']

slvtable['gold']=gldtable['Close'].copy()
slvtable['gsratio']=slvtable['gold']/slvtable['Close']

gldtable=gldtable.dropna()
slvtable=slvtable.dropna()

#fig.show() gold
from plotly.subplots import make_subplots

fig = make_subplots(specs=[[{"secondary_y": True}]])

#fig = px.line(df, x=df.index, y='Close', title='<b>Gold Price</b>')

fig.add_trace(
    go.Scatter(x=gldtable.index, y=gldtable['Close'],name='GC=F Close',line = dict(color='red', width=4)),secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=gldtable.index, y=gldtable['mean'], name='Mean',line = dict(color='royalblue', width=2)),secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=gldtable.index, y=gldtable['addstd'], name='+2 std',line = dict(color='royalblue', width=3, dash='dot')),secondary_y=True,
)
fig.add_trace(
    go.Scatter(x=gldtable.index, y=gldtable['lessstd'], name='-2 std',line = dict(color='royalblue', width=3, dash='dot')),secondary_y=True,
)
fig.add_trace(
    go.Scatter(x=gldtable.index, y=gldtable['gsratio'], name='Gld/Slv Ratio',line = dict(color='green', width=2)),secondary_y=False,
)



# Set x-axis title

#fig.update_layout(template='plotly_white')
fig.update_layout(title='<b>FUTURE GOLD PRICE CHART</b>',showlegend=True)


fig.update_yaxes(title_text='Price', color='red', secondary_y=True)
fig.update_yaxes(title_text='Gold/Silver Ratio', color='green', secondary_y=False)


fig.update_xaxes(
    title_text="Date",
    color='#7f7f7f',
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(count=3, label="3y", step="year", stepmode="backward"),
            dict(count=5, label="5y", step="year", stepmode="backward"),            
            dict(step="all")
        ])
    )
)

fig.update_layout(template='plotly_white')
#fig.update_layout(template='xgridoff')                  
#fig.update_layout(plot_bgcolor='rgb(255,250,250)')
fig.show()


#fig.show() silver
from plotly.subplots import make_subplots

fig = make_subplots(specs=[[{"secondary_y": True}]])

#fig = px.line(df, x=df.index, y='Close', title='<b>Gold Price</b>')

fig.add_trace(
    go.Scatter(x=slvtable.index, y=slvtable['Close'],name='SI=F Close',line = dict(color='red', width=4)),secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=slvtable.index, y=slvtable['mean'], name='Mean',line = dict(color='royalblue', width=2)),secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=slvtable.index, y=slvtable['addstd'], name='+2 std',line = dict(color='royalblue', width=3, dash='dot')),secondary_y=True,
)
fig.add_trace(
    go.Scatter(x=slvtable.index, y=slvtable['lessstd'], name='-2 std',line = dict(color='royalblue', width=3, dash='dot')),secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=slvtable.index, y=slvtable['gsratio'], name='Gld/Slv Ratio',line = dict(color='green', width=2)),secondary_y=False,
)

# Set x-axis title

#fig.update_layout(template='plotly_white')
fig.update_layout(title='<b>FUTURE SILVER PRICE CHART</b>',showlegend=True)


fig.update_yaxes(title_text='Price', color='red', secondary_y=True)
fig.update_yaxes(title_text='Gold/Silver Ratio', color='green', secondary_y=False)


fig.update_xaxes(
    title_text="Date",
    color='#7f7f7f',
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(count=3, label="3y", step="year", stepmode="backward"),            
            dict(count=5, label="5y", step="year", stepmode="backward"),            
            dict(step="all")
        ])
    )
)

fig.update_layout(template='plotly_white')
#fig.update_layout(template='xgridoff')                  
#fig.update_layout(plot_bgcolor='rgb(255,250,250)')
fig.show()





stock ="GDX"


#GET STOCK DATA
#yahoo.Get.Info()
#datab = yahoo.Get.Prices(stock,period=[days,end])
datab = web.DataReader(stock, data_source='yahoo', start = days, end = end) #name為股票代號名稱 start、end為資料下載期間

datab.index = pd.to_datetime(datab.index).strftime("%Y-%m-%d")
datab.index=pd.to_datetime(datab.index)
datab= datab.replace(0, np.nan)
datab=datab.dropna()
df=datab

datab["std"]=round(datab["Close"].rolling(30,min_periods=1).std(),2)
datab["mean"]=round(datab["Close"].rolling(30,min_periods=1).mean(),2)
datab["addstd"]=datab["mean"]+datab["std"]+datab["std"]
datab["lessstd"]=datab["mean"]-datab["std"]-datab["std"]
datab=datab.dropna()

returns_df_d=datab["Close"].pct_change(periods=1)
#returns_df_d=stockmthtable
returns_df_m = pd.DataFrame((returns_df_d + 1).resample('M').prod() - 1)
returns_df_m['Month'] = returns_df_m.index.month
returns_df_m.columns=[stock,'Month']
monthly_table = returns_df_m[[stock,'Month']].pivot_table(returns_df_m[[stock,'Month']], index=returns_df_m.index, columns='Month', aggfunc=np.sum).resample('A')
monthly_table = monthly_table.aggregate('sum')
monthly_table.columns = monthly_table.columns.droplevel()
#replace full date in index column with just the correspnding year
monthly_table.index = monthly_table.index.year
monthly_table['YTD'] = ((monthly_table + 1).prod(axis=1) - 1)
monthly_table = round(monthly_table * 100,3)
#Replace integer column headings with MMM format
monthly_table.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','YTD']
print("-----------------------------------------------------------------------------------------------")
print(stock + "  Monthly return")
print(monthly_table)


#fig = px.line(x=datab.index, y=df['Adj Close'])
# Set x-axis title
#fig.update_xaxes(title_text="Date")

# Set y-axes titles
#fig.update_yaxes(title_text="<b>Gold Price</b>", secondary_y=False)
#fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)



#fig.show()
from plotly.subplots import make_subplots

fig = make_subplots(specs=[[{"secondary_y": True}]])

#fig = px.line(df, x=df.index, y='Close', title='<b>Gold Price</b>')

fig.add_trace(
    go.Scatter(x=df.index, y=df['Close'],name='GDX Close',line = dict(color='red', width=4)),secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=df.index, y=df['mean'], name='Mean',line = dict(color='royalblue', width=2)),secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=df.index, y=df['addstd'], name='+2 std',line = dict(color='royalblue', width=3, dash='dot')),secondary_y=True,
)
fig.add_trace(
    go.Scatter(x=df.index, y=df['lessstd'], name='-2 std',line = dict(color='royalblue', width=3, dash='dot')),secondary_y=True,
)

# Set x-axis title

#fig.update_layout(template='plotly_white')
fig.update_layout(title='<b>GDX PRICE CHART</b>',showlegend=True)


fig.update_yaxes(title_text='Price', color='red', secondary_y=True)
#fig.update_yaxes(title_text='Volume', color='royalblue', secondary_y=False)


fig.update_xaxes(
    title_text="Date",
    color='#7f7f7f',
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(count=3, label="3y", step="year", stepmode="backward"),             
            dict(count=5, label="5y", step="year", stepmode="backward"),            
            dict(step="all")
        ])
    )
)

fig.update_layout(template='plotly_white')
#fig.update_layout(template='xgridoff')                  
#fig.update_layout(plot_bgcolor='rgb(255,250,250)')
fig.show()

