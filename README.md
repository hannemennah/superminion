# superminion


Market Analysis Suite
--------------

Swiss Army Knife analytics suite for trading strategy assessment and automated multithreaded backtesting. Includes a GUI built in Tkinter (with an animated .gif displayed as a visual cue for when backtesting is processing, too!) and a highly customized Matplotlib tool which can be launched from the main window at any time as a new process which will not interfere with the primary one. 

Capable of simulating trade latency, strategies using both sells and shorts, and customizable slippage rates. 

Analysis output is directed to a file of the user's choice (myOutputFile.txt by default) and the contents of this file can be emailed to the user's email address at the click of a button.

**Note: the specific variables, heuristics, and the meat of the analytic engine have been deliberately stripped from the public version of this code. What I consider to be "the cool stuff" is not available as open source software, and as a result, some buttons which are present on the UI may do nothing at all, or even produce an error message.**


Running
--------------

This is written for Python 3, not Python 2. For best results, you must install numpy and matplotlib before running superminion.

Also, if you would like to use the Multiplot tool (to generate Matplotlib graphs) or see anything beyond the face of the application itself, you will want to download the trade data for the exchange(s) you're interested in (either Bitfinex or Bitstamp) from [this page](http://api.bitcoincharts.com/v1/csv/), and place it in a folder named "data" in your superminion root directory. Name the file(s) either "bitfinex.csv" or "bitstamp.csv" (or both, if you want to use both exchanges' data). This choice is yours and yours alone.

When you are ready to run the application, simply run:

    python3 superminion.py


