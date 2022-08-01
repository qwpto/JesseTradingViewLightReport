# Jesse tradingview light reporting library

Generate an html document containing all of the scripts and data to load tradingview and review the results. This can be generated within a strategy at regular intervals to review the results live.

install with:
	pip install JesseTradingViewLightReport

To generate just the candlestick, volume, and order report - Add the following to your strategy:

	import JesseTradingViewLightReport
	 
		def terminate(self):
			JesseTradingViewLightReport.generateReport()


But you can also add custom data for example:

	generateReport(customData={"atr":{"data":self.atr, "options":{"pane":1, "colour":'rgba(251, 192, 45, 1)'}}, 'two':{"data":self.candles[:,1]-5, "options":{"pane":2}, "type":"HistogramSeries"}, 'three':{"data":self.candles[:,1]+5, "options":{"pane":2, "color":'purple'}}})

	![alt text](https://github.com/qwpto/JesseTradingViewLightReport/blob/release/example1.jpg?raw=true)

For more information on plot types and options see:
- https://tradingview.github.io/lightweight-charts/docs/api
- https://www.tradingview.com/lightweight-charts/