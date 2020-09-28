from binance.client import Client 
import binance_keys
import plotly.graph_objs as graph
import numpy as np
import pandas as panda 
from plotly.subplots import make_subplots

client=Client(api_key=binance_keys.PKey,api_secret=binance_keys.SKey)

def Binance_Wallet():#Shows Nonzero wallet balance on Binance
	print("Looking at Market Prices...")
	newList=[]
	info = client.get_account().get('balances')#gets enire account balance
	btc_avg_price = client.get_avg_price(symbol='BTCUSDT') #gets BTC usd price
	BTC_price=float(btc_avg_price.get('price'))
	eth_avg_price = client.get_avg_price(symbol='ETHUSDT') #gets ETH usd price
	ETH_price=float(eth_avg_price.get('price'))
	ETHBTC=client.get_avg_price(symbol='ETHBTC') #gets btc value of eth to use in calcuatlating total btc
	ETHBTC_price=float(ETHBTC.get('price'))
	btc_total_amount=0.00
	for asset in info:
		if(asset.get('free')!='0.00000000' and asset.get('free')!='0.00'): #find all balances that dont equal 0
			newList.append(asset)
	for asset in newList:
		if(asset.get('asset')==str('BTC')): #if the coin is BTC
			asset['Total $']=str(round(((float(asset.get('free'))+float(asset.get('locked')))*BTC_price),2)) #total $ amount of btc
			#if(float(asset.get('Total $'))>5.00):	
			asset.update({'BTC Total':round((float(asset.get('free'))+float(asset.get('locked'))),8)}) #round that value to 8 decimals
			asset.update({'Market Price':round(float(BTC_price),2)})
			btc_total_amount+=(float(asset.get('free'))+float(asset.get('locked'))) #total btc amount
		elif(asset.get('asset')==str('ETH')): #do the same above with eth
			asset['Total $']=str(round(((float(asset.get('free'))+float(asset.get('locked')))*ETH_price),2))
			#if(float(asset.get('Total $'))>5.00):		
			btc_eth_total=(float(asset.get('free'))+float(asset.get('locked'))*ETHBTC_price)
			btc_total_amount+=btc_eth_total	
			asset.update({'BTC Total':round(btc_eth_total,8)})
			asset.update({'Market Price':round(float(ETH_price),2)})
		else:
			ticker=asset.get('asset')+'BTC' #find btc pair of coins
			if(ticker==None):
				ticker=asset.get('asset')+'USDT'
			elif(ticker=='USDTUSDT' or ticker=='USDTBTC'): #if coin is tether just look at btc usdt value
				ticker="BTCUSDT"
				pair_ticker=client.get_avg_price(symbol=ticker)
				pair_price=float(pair_ticker.get('price')) #get market price for that pair
				val=round(float(asset.get('free'))+float(asset.get('locked')),2)
				asset['Total $']=str(val) #get total $ amount for that coin
				pair_btc_total=(float(asset.get('free'))+float(asset.get('locked')))/BTC_price
				asset.update({'BTC Total':round(pair_btc_total,8)}) #round btc amount to 8 decimals
				asset.update({'Market Price':round(BTC_price,8)}) #round market price amount to 8 decimals
				continue
			pair_ticker=client.get_avg_price(symbol=ticker)
			pair_price=float(pair_ticker.get('price'))
			val=round(((float(asset.get('free'))+float(asset.get('locked')))*pair_price*BTC_price),2) #calculating $ amount of coin
			asset['Total $']=str(val)
			#if(float(asset.get('Total $'))>5.00):	
			pair_btc_total=pair_price*(float(asset.get('free'))+float(asset.get('locked')))
			btc_total_amount+=pair_btc_total #calculating total btc amount in wallet
			asset.update({'BTC Total':round(pair_btc_total,8)}) #round btc and market prices to 8 decimals
			asset.update({'Market Price':round(float(pair_price),8)})
	print("Organizing your wallet...")
	btc_usd_amount=round((btc_total_amount*BTC_price),2)
	btc_total_amount=round(btc_total_amount,8)
	
	for asset in newList:
		asset['available']=asset.pop('free') #changing key 'free' to 'available' cause more intuitive
		
	def WalletDistribution():
		user_input=input("Do you want to see your wallet distribution?(Y/N) ") 
		if(user_input=='Y' or user_input=='y' or user_input=='YES' or user_input=='Yes' or user_input=='yes'):	
			dataframe=panda.DataFrame(newList) #turn data into dataframe to use in creating table and pie chart
			df=dataframe.sort_values(by=['BTC Total'],ascending=False) #sort by btc total descending so highest first sorted to last
			wallet_distribution=make_subplots(rows=1, cols=2, specs=[[{"type":"table"},{"type":"pie"}]])#imagine a table with 2 columns. One is for table and One for pie chart
			wallet_distribution.add_trace(graph.Pie(name="Total $=",values=df['Total $'],title="Wallet Distribution 			         \nFor Legend on right, click on a coin to hide it from pie chart.\nDouble click a coin in the legend on the right to focus it",labels=df['asset'],showlegend=True),row=1,col=2)
			#pie chart, show labels and show legend so when you hover over, it gives $ amount invested into that coin
			wallet_distribution.add_trace(graph.Table(header=dict(values=["Coin","Available","Locked","BTC Total","Total $","Market Price(BTC pair)","TOTAL BTC","TOTAL $"],align="center"),
													   cells=dict(values=[df['asset'],df['available'],df['locked'],df['BTC Total'],'$'+df['Total $'],df['Market Price'],btc_total_amount,'$'+str(btc_usd_amount)],align="center")),row=1,col=1)
			#table shows all colum names and values associated with those columns
			wallet_distribution.show()
					
	
		else: #if user selects anything other than Y, y, Yes, yes, YES automativally exit
			return 

	def Percentage(l, datavalues): #calculates % for pie chart
	    values = int(l / 100.*np.sum(datavalues)) 
	    return "{:.1f}%\n(${:d})".format(l, values) 	
	
	WalletDistribution() #calls this method and asks user if they want to see their wallet.

Binance_Wallet() #calls this method when program is run then run Wallet Distribution once this method is finished.