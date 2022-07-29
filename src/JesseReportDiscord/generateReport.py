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
const getData = async () => {
  {{resp}}

  const cdata = resp.split('\n').map((row) => {
    const [time, open, high, low, close] = row.split(',');
    return {
      time: time / 1000,
      open: open * 1,
      high: high * 1,
      low: low * 1,
      close: close * 1,
    };
  });
  return cdata;
};

const displayChart = async () => {
  const chartProperties = {
    width: 1500,
    height: 600,
    timeScale: {
      timeVisible: true,
      secondsVisible: true,
    },
  };

  const domElement = document.getElementById('tvchart');
  const chart = LightweightCharts.createChart(domElement, chartProperties);
  const candleseries = chart.addCandlestickSeries();
  const klinedata = await getData();
  candleseries.setData(klinedata);
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
        
        resp =  'const resp = `'
        for candle in candles:
            resp += str(candle[0]) + ','
            resp += str(candle[1]) + ','
            resp += str(candle[2]) + ','
            resp += str(candle[3]) + ','
            resp += str(candle[4]) + '\n'
        resp = resp.rstrip(resp[-1]) # remove last new line
        resp += '`;'

        info = {'title': studyname,
            'resp': resp
            }
            
        result = template(tpl, info)

        filename = "storage/JesseTradingViewLightReport/" + file_name + '.html'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(result)
    


