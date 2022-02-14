# copyright Karel Kopfrkingl

# this script handles orders from Binance via it's API
# algorithm:
# step 1: choose only filled orders
# step 2: separate buy and sell orders
# step 3: evaluate MARKET orders 
#   - if possitive, calculate buy price as cummulativeQuoteQty/origQty
#   - else read buy price from input dict
#   - same applies for sell orders
# step 4: save buy and sell prices in separate lists
# step 5: calculate average buy and sell price

# imports

# input list
binanceInput = [

    {'symbol': 'LSKUSDT',
    'orderId': 20705263,
    'orderListId': -1,
    'clientOrderId': 'ios_46a6f268bf854872b3f8431993e32cde',
    'price': '1.15500000',
    'origQty': '81.18000000',
    'executedQty': '81.18000000',
    'cummulativeQuoteQty': '93.68172000',
    'status': 'FILLED',
    'timeInForce': 'GTC',
    'type': 'LIMIT',
    'side': 'BUY',
    'stopPrice': '0.00000000',
    'icebergQty': '0.00000000',
    'time': 1594148179514,
    'updateTime': 1594148179514,
    'isWorking': True,
    'origQuoteOrderQty': '0.00000000'},

    {'symbol': 'LSKUSDT',
    'orderId': 20797965,
    'orderListId': -1,
    'clientOrderId': 'ios_5e5f54bc10a94c4bae1111f187036eb8',
    'price': '1.26820000',
    'origQty': '81.18000000',
    'executedQty': '81.18000000',
    'cummulativeQuoteQty': '102.95247600',
    'status': 'FILLED',
    'timeInForce': 'GTC',
    'type': 'LIMIT',
    'side': 'SELL',
    'stopPrice': '0.00000000',
    'icebergQty': '0.00000000',
    'time': 1594217504648,
    'updateTime': 1594217689617,
    'isWorking': True,
    'origQuoteOrderQty': '0.00000000'},

    {'symbol': 'LSKUSDT',
    'orderId': 72085416,
    'orderListId': -1,
    'clientOrderId': 'ios_03e7cd75bcf54cf9bb5d03efa639c366',
    'price': '2.31900000',
    'origQty': '10.00000000',
    'executedQty': '10.00000000',
    'cummulativeQuoteQty': '23.17300000',
    'status': 'FILLED',
    'timeInForce': 'GTC',
    'type': 'LIMIT',
    'side': 'BUY',
    'stopPrice': '0.00000000',
    'icebergQty': '0.00000000',
    'time': 1613079682014,
    'updateTime': 1613079682014,
    'isWorking': True,
    'origQuoteOrderQty': '0.00000000'},

    {'symbol': 'LSKUSDT',
    'orderId': 99382270,
    'orderListId': -1,
    'clientOrderId': 'x-KL0J9FGS_3cmstr_16322878_0',
    'price': '0.00000000',
    'origQty': '5.00000000',
    'executedQty': '5.00000000',
    'cummulativeQuoteQty': '25.13617600',
    'status': 'FILLED',
    'timeInForce': 'GTC',
    'type': 'MARKET',
    'side': 'SELL',
    'stopPrice': '0.00000000',
    'icebergQty': '0.00000000',
    'time': 1616896440736,
    'updateTime': 1616896440736,
    'isWorking': True,
    'origQuoteOrderQty': '0.00000000'}
]

# start of script
def calculateAvgPrices(binanceInput):
    

    # function for calculating MarketOrderPrices (sell and buy)
    def calculateMarketOrderPrice(cummulativeQuoteQty, origQty):
            return float(cummulativeQuoteQty)/float(origQty)
        
    lBuyPrice =[]
    lSellPrice = []

    sumBuyPrice = 0
    sumSellPrice = 0
    sumQty = 0

    # if type is market, price must be calculated: cummulativeQuoteQty / origQty
    for dOrder in binanceInput:

        # step 1: choose only filled orders
        if not dOrder['status'] == 'FILLED':
            continue
        
        # step 2: separate buy and sell orders
        if dOrder['side'] == 'BUY':
            # step 3: evaluate MARKET orders 
            if dOrder['type'] == 'MARKET':
                # call method for calculating MARKET order price
                buyMarketPrice = float(calculateMarketOrderPrice(dOrder['cummulativeQuoteQty'], dOrder['origQty']) )
                # step 4: save buy and sell prices in separate lists
                # add calculated price to list of buy orders prices
                lBuyPrice.append(buyMarketPrice)
                print(f'added to buy list of prices calculated price of MARKET order, value: {buyMarketPrice}')
                
            # buy order, NOT a MARKET type
            else:
                # just read the price from input dict
                buyPrice = float(dOrder['price'])
                
                # step 4: save buy and sell prices in separate lists
                # add the price to list of buy orders prices
                lBuyPrice.append(buyPrice)
                print(f'add to buy list of price given price of MARKET order, value: {buyPrice}')
        
        # step 2: separate buy and sell orders    
        else:
            if dOrder['type'] == 'MARKET':
                # call method for calcucating MARKET order price
                sellMarketPrice = float(calculateMarketOrderPrice(dOrder['cummulativeQuoteQty'], dOrder['origQty']))
                
                # step 4: save buy and sell prices in separate lists
                # add calculated price to list of sell orders prices
                lSellPrice.append(sellMarketPrice)
                print(f'added to sell list of prices calculated price of MARKET order, value: {sellMarketPrice}')
                
            # sell order, NOT a MARKET type
            else:
                # just read the price from input dict
                sellPrice = float(dOrder['price'])
                
                # step 4: save buy and sell prices in separate lists
                # add the price to list of sell orders prices
                lSellPrice.append(sellPrice)
                print(f'add to SELL list of prices given price of MARKET order, value: {sellPrice}')
        
    # step 5: calculate average buy and sell price
    avgBuyPrice = sum(lBuyPrice)/len(lBuyPrice)
    avgSellPrice = sum(lSellPrice)/len(lSellPrice)
    
    return avgBuyPrice, avgSellPrice

a,b = calculateAvgPrices(binanceInput)


#print(calculateAvgPrices(binanceInput))
print(f'prumerna nakupni cena cini: {a}\n prumerna prodejni cena cini: {b}')
