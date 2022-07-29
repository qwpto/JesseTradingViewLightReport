# Jesse tradingview light reporting library

Generate an html document containing all of the scripts and data to load tradingview and review the results. This can be generated within a strategy at regular intervals to review the results live.

install with:
	pip install JesseTradingViewLightReport

Add the following to your strategy:

	import JesseTradingViewLightReport
	 
		def terminate(self):
			JesseTradingViewLightReport.generateReport()


