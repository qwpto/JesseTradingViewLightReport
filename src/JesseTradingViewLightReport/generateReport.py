from jesse.services.file import store_logs
import jesse.helpers as jh
from jesse.modes import backtest_mode
from jesse.config import config
from jesse.services import charts
from jesse.services import report
from jesse.routes import router
from datetime import datetime, timedelta
from jesse.store import store
import jesse.services.metrics as stats

import pandas as pd

from bottle import template
import os

# from jesse.strategies import Strategy

from enum import IntEnum
class CD(IntEnum):
    date = 0
    open = 1
    close = 2
    high = 3
    low = 4
    volume = 5

def generateReport():
    if(config["app"]["trading_mode"] == 'backtest'):
        
        tpl = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
</head>
<body>
    <div id="tvchart"></div>
</body>
<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
<script>
{{candleData}}

{{orderData}}

const getCandleData = async () => {

  const cdata = candleData.split('\n').map((row) => {
    const [time, open, high, low, close] = row.split(',');
    return {
      time: time * 1,
      open: open * 1,
      high: high * 1,
      low: low * 1,
      close: close * 1,
    };
  });
  return cdata;
};

const getVolumeData = async () => {

  const vdata = candleData.split('\n').map((row) => {
    const [time, x1, x2, x3, x4, volume] = row.split(',');
    return {
      time: time * 1,
      value: volume * 1
    };
  });
  return vdata;
};

const getOrderData = async () => {

  const odata = orderData.split('\n').map((row) => {
    const [time, mode, side, type, qty, price] = row.split(',');
    const position = (side === 'sell')?'aboveBar':'belowBar';
    const shape = (side === 'sell')?'arrowDown':'arrowUp';
    const color = (side === 'sell')?'#e91e63':'#2196F3';
    
    return {
      time: time * 1,
      position: position,
      color: color,
      shape : shape,
      text : type + ' @ ' + price + ' : ' + qty + mode
    };
  });
  return odata;
};

const displayChart = async () => {
  const chartProperties = {
    width: window.innerWidth-20,
    height: window.innerHeight-20,
    timeScale: {
      timeVisible: true,
      secondsVisible: true,
    },
  };
  



  const domElement = document.getElementById('tvchart');
  const chart = LightweightCharts.createChart(domElement, chartProperties);
  const candleseries = chart.addCandlestickSeries();
  const klinedata = await getCandleData();
  candleseries.setData(klinedata);
  const odata = await getOrderData();
  candleseries.setMarkers(odata);

  const histogramSeries = chart.addHistogramSeries({
        color: '#26a69a',
        priceFormat: {
            type: 'volume',
        },
        priceScaleId: '',
        scaleMargins: {
            top: 0.8,
            bottom: 0,
        },
    });
  const vdata = await getVolumeData();
  histogramSeries.setData(vdata);
  //chart.timeScale().fitContent();
  
function updateWindowSize() {
    chart.applyOptions({     width: window.innerWidth-20,    height: window.innerHeight-20, });
}  

  window.onresize = updateWindowSize;



};

displayChart();
</script>
</html>        
        """

        file_name = jh.get_session_id()
        studyname = backtest_mode._get_study_name()
        start_date = datetime.fromtimestamp(store.app.starting_time / 1000) # could optimise this if the generated report already contains data, just start from where it was up to and append.
        date_list = [start_date + timedelta(days=x) for x in range(len(store.app.daily_balance))]
        fullCandles = backtest_mode.load_candles(date_list[0].strftime('%Y-%m-%d'), date_list[-1].strftime('%Y-%m-%d'))
        candles = fullCandles[jh.key(router.routes[0].exchange, router.routes[0].symbol)]['candles']
        
        candleData =  'const candleData = `'
        for candle in candles:
            candleData += str(candle[CD.date]/1000) + ','            
            candleData += str(candle[CD.open]) + ','
            candleData += str(candle[CD.high]) + ','
            candleData += str(candle[CD.low]) + ','
            candleData += str(candle[CD.close]) + ','            
            candleData += str(candle[CD.volume]) + '\n'
        candleData = candleData.rstrip(candleData[-1]) # remove last new line
        candleData += '`;'

        orderData =  'const orderData = `'
        for trade in store.completed_trades.trades:
            for order in trade.orders:
                if(order.is_executed):
                    mode = ''
                    if(order.is_stop_loss):
                        mode = ' (SL)'
                    elif(order.is_take_profit):
                        mode = ' (TP)'                
                    orderData += str(order.executed_at/1000) + ','            
                    orderData += mode + ','
                    orderData += order.side + ','
                    orderData += order.type + ','
                    orderData += str(order.qty) + ','            
                    orderData += str(order.price) + '\n'
        orderData = orderData.rstrip(orderData[-1]) # remove last new line
        orderData += '`;'

        info = {'title': studyname,
            'candleData': candleData,
            'orderData': orderData
            }
            
        result = template(tpl, info)

        filename = "storage/JesseTradingViewLightReport/" + file_name + '.html'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(result)
    
        return filename

