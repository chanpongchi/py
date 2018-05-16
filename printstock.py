from pandas_datareader import data as pdr
from pandas import Series, DataFrame 
import pandas as pd
import fix_yahoo_finance as yf
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
#yf.pdr_override()



def getStock(id,days):  
    stock = str(id)+'.HK'
    today = dt.date.today() 
    datab = yf.download(stock,days, str(today))
    #datab = yf.download(stock,days,daysto)
    d_return=round(datab["Adj Close"].pct_change(periods=1),4)
    d_return[np.isnan(d_return)]=0
    datab=pd.concat([datab["Close"],d_return,datab["Volume"]],axis=1)
    datab.columns=["Close Price","Change %","Volume"]
    return datab

#getStock(2800,"yyyy-mm-dd")


#getStock("2800","2018-01-01")

#====================================

def printStock(id,days):
         datab=getStock(id,days)
         today = dt.date.today() #todays date
         hsi = yf.download("^hsi",days, str(today))
         #hsi = yf.download("^hsi",days,daysto)
         cmean=datab['Close Price'].rolling(30,min_periods=1).mean()
         cstd=datab['Close Price'].rolling(60,min_periods=1).std()
         usd=cmean+cstd
         dsd=cmean-cstd
         d_return=round(datab['Close Price'].pct_change(periods=1),4)
         d_return[np.isnan(d_return)]=0
         c_return=d_return.add(1).cumprod()*100-100
         hsid_return=round(hsi['Adj Close'].pct_change(periods=1),4)
         hsid_return[np.isnan(hsid_return)]=0
         hsic_return=hsid_return.add(1).cumprod()*100-100
         combinedata = pd.concat([datab['Close Price'],d_return,c_return,hsid_return,hsic_return],axis=1)        
         fig, ax1 = plt.subplots()
         color = "blue"
         ax1.set_ylabel("HSI", color=color)
         ax1.plot(hsi['Adj Close'], color="blue",label="HSI")
         ax1.tick_params(axis='y', labelcolor=color)
         ax2 = ax1.twinx()  # 
         color = "black"
         ax2.set_xlabel('Date')
         ax2.set_ylabel("Price", color=color)  # we already handled the x-label with ax1
         ax2.plot(datab['Close Price'], color=color,label=id)
         ax2.plot(cmean, color="red",label="Mean")
         ax2.plot(usd, color="orange",label="up std")
         ax2.plot(dsd, color="orange",label="dn std")         
         ax2.tick_params(axis='y', labelcolor=color)
         fig.tight_layout()  # otherwise the right y-label is slightly clipped
         plt.grid(True)
         plt.title(id)
         #ax1.legend()
         ax1.legend(loc=0)      
         ax2.legend(loc=2)
         plt.draw()
         #plt.show()
         #=== return
         fig, axb1 = plt.subplots()
         color = 'blue'
         axb1.plot(c_return, color=color,label=id)
         axb1.plot(hsic_return, color="black",label="HSI")
         axb1.set_ylabel('Cumulitive Return %', color=color)
         axb1.tick_params(axis='y', labelcolor=color)
         axb2 = axb1.twinx()  # instantiate a second axes that shares the same x-axis
         color = 'tab:blue'
         axb2.set_xlabel('Date')
         axb2.set_ylabel('Daily Return %', color=color)
         axb2.plot(d_return, color=color,label="Daily Chg %")
         axb2.tick_params(axis='y', labelcolor=color)
         fig.tight_layout()  # otherwise the right y-label is slightly clipped
         plt.grid(True)
         plt.title(id)
         axb1.legend(loc=0)      
         axb2.legend(loc=2)
         plt.draw()
         s=" "
         stockreturn=s.join([id,"D %"])
         stockcreturn=s.join([id,"C %"])
         hsireturn=s.join(["HSI","D %"])
         hsicreturn=s.join(["HSI","C %"])
         combinedata.columns=[id,stockreturn,stockcreturn,hsireturn,hsicreturn]
         combinedata.to_pickle('combinedata.pkl') 
         return combinedata
         plt.show()




printStock("0881","2018-01-01")
db=pd.read_pickle("combinedata.pkl")
