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
