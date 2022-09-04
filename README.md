# Jesse tradingview light reporting library

Generate an html document containing all of the scripts and data to load tradingview and review the results. This can be generated within a strategy at regular intervals to review the results live.

The library is published to pypi: https://pypi.org/project/JesseTradingViewLightReport/

So to install, from a command prompt where you would be running python:
```
pip install JesseTradingViewLightReport
```

Upgrade:
```
pip install JesseTradingViewLightReport --upgrade
```

To generate just the candlestick, volume, and order report - Add the following to your strategy:
```python
import JesseTradingViewLightReport

	def terminate(self):
		JesseTradingViewLightReport.generateReport()
```

But you can also add custom data for example:

```python
JesseTradingViewLightReport.generateReport(
	customData={
		"atr":{"data":self.atr, "options":{"pane":1, "colour":'rgba(251, 192, 45, 1)'}}, 
		'two':{"data":self.candles[:,1]-5, "options":{"pane":2}, "type":"HistogramSeries"}, 
		'three':{"data":self.candles[:,1]+5, "options":{"pane":2, "color":'purple'}}
	}
)
```

![demo](https://github.com/qwpto/JesseTradingViewLightReport/blob/release/example1.png?raw=true)

Available types are:
- LineSeries
- HistogramSeries
- AreaSeries
- BaselineSeries

You may be able to use:
- BarSeries
- CandlestickSeries

For more information on plot types and options see:
- https://tradingview.github.io/lightweight-charts/docs/series-types
- https://tradingview.github.io/lightweight-charts/docs/api
- https://www.tradingview.com/lightweight-charts/

For the moment, the data will need to be the same length as the number of candles you would receive from self.candles

The different panes can be resized by dragging them with the cursor.

It is also possible to change the candle colors to PVSRA candles with the option:
```python
JesseTradingViewLightReport.generateReport(chartConfig={'isPvsra':True})
```
However, at the moment it is not possible to use multiple panes with this option. This restiction will be removed in a future release.
![demo2](https://github.com/qwpto/JesseTradingViewLightReport/blob/release/example2.png?raw=true)

It is possible to also plot the profit and loss with for example:
```python
JesseTradingViewLightReport.generateReport(chartConfig={'pnl':True})
```

The generateReport function returns the relative location of the file. You can also find it inside where you're running the jesse strategy from there will be a folder called storage, inside that this plugin creates a folder called JesseTradingViewLightReport. Then each time you run a strategy with different parameters it will create a unique file called something like 77cbda27-6eec-48b6-90fb-621656d9e9d8.html 

So in this example it'll be:
c:/whereveryourunjesse/storage/JesseTradingViewLightReport/77cbda27-6eec-48b6-90fb-621656d9e9d8.html

CHANGELOG:
1.1.0 - added support for jesse 0.39.+, and added PNL calculation for all orders. With accumulated PNL plotting.
1.2.0 - Generate charts for live trading.
1.2.1 - Allow missing latest data in custom data.
1.2.2 - added trade ID to order data.