#imports
import mplfinance as mpf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

#central board
st.write("# Stock Analysis")
isvalidInput=False
stkList=[]
st.write("\n")
isOHCL =st.checkbox("OHCL PLot")
isCandle=st.checkbox("Candlestick Plot")
isHCandle=st.checkbox("Hollow Candlestick Plot")
isLineP=st.checkbox("Close Price Line Plot")
isLineV=st.checkbox("Volume Line Plot")
isStats=st.checkbox("Data Statistics")

#side bar
st.sidebar.header("Stock")

#Stock list generation
def get_stockList():
    #csv file reading
    df = pd.read_csv("C:/Users/Yuti/PycharmProjects/StockAnalysis/stockList.csv")
    global stkList
    #if list is already ready
    if(len(stkList)!=0):
        return;
    #else
    stkList.append(df["symbol"][0])
    for i in range(1, len(df)):
        if (df["symbol"][i] != df["symbol"][i-1]):
            stkList.append(df["symbol"][i])

#user input about date and stock name
def get_input():
    start_date= st.sidebar.text_input("Start Date","2021-01-04")
    end_date=st.sidebar.text_input("End Date","2021-01-22")
    stock_symbol=st.sidebar.text_input("Stock Symbol","AAPL")
    inSymbol=stock_symbol
    return start_date,end_date,stock_symbol.upper()

#forming dataframe of input stock for input duration
def get_data(symbol,start,end):
    df=pd.read_csv("C:/Users/Yuti/PycharmProjects/StockAnalysis/stockList.csv")
    global isvaliddate
    #check for invalid dates
    try:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
    except:
        start = pd.to_datetime("2021-01-04")
        end = pd.to_datetime("2021-01-22")
        st.sidebar.write("Invalid date. Default date selected")
    global isvalidInput
    #searching the stock
    for i in range(0,len(df)):
        if(symbol==df["symbol"][i]):
            startInd=i;
            isvalidInput=True
            break;
    #stock not found default set
    if(isvalidInput==False):
        symbol="AAPL"
        st.sidebar.write("Stock does not exist. Enter a valid symbol")
        return
    #start date set
    for i in range(0, len(df)):
        if (symbol==df["symbol"][i] and start<= pd.to_datetime(df['date'][i])):
            start_row=i;
            break;
    #end date set
    for i in range(start_row, len(df)):
        if (symbol==df["symbol"][i] and end<= pd.to_datetime(df['date'][i])):
            end_row=i;
            break;
        if(symbol!=df["symbol"][i]):
            end_row = i-1;
            break;
    #setting index as date values
    df=df.set_index(pd.DatetimeIndex(df['date'].values))
    #slicing dataframe according to date
    return df.iloc[start_row:end_row+1,:]

start,end,symbol=get_input()
df=get_data(symbol,start,end)

#sidebar
st.sidebar.write("Range: Jan 2021 - August 2021\n")
isStkList=st.sidebar.button("List of all stocks")
st.sidebar.write("\n")

st.set_option('deprecation.showPyplotGlobalUse', False)

#to not display any charts
def nocharts():
    global isOHCL ;isOHCL= False
    global isCandle; isCandle=  False
    global isHCandle; isHCandle=False
    global isLineP;  isLineP=False
    global isLineV ; isLineV=False
    global isStats ; isStats=False
    return

#to display stocks
if(isStkList):
    nocharts()
    get_stockList()
    st.header("\nThe Stock List in alphabetical order :")
    stkList.sort()
    c=1
    for i in stkList:
        output=str(c)+") "+i
        st.write(output)
        c+=1
    isStkList=False

#Display in acse of invalid stock
if(isvalidInput==False ):
    symbol="AAPL"
    nocharts()
    st.header("Stock does not exist. Enter a valid symbol")

#display of OHCL plot
if(isOHCL):
    st.header(symbol+" OHCL Plot")
    mpf.plot(df)
    st.pyplot()
    st.write("")

#display of candlestick plot
if(isCandle):
    st.header(symbol+ " Candlestick Plot")
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name=symbol)])

    fig.update_xaxes(type='category')
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)
    st.write("")

#display of hollow candlestick plot
if(isHCandle):
    st.header(symbol+ " Hollow Candlestick Plot")
    mpf.plot(df, type='candle')
    st.pyplot()
    st.write("")

#display of Price Line plot
if(isLineP):
    st.header(symbol+" Close Price Line Plot")
    st.line_chart(df['close'])
    st.write("")

#display of Volume Line plot
if(isLineV):
    st.header(symbol+" Volume Line Plot")
    st.line_chart(df['volume'])
    st.write("")

#diaplay of stats of the stock
if(isStats):
    st.header(symbol+" Data Statistics")
    st.write(df.describe())
    st.write("")


