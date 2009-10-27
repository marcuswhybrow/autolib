"""
Utilities module for tasks related to the googlehooks app.
"""
import datetime, settings

def log(message):
	try:
		f = open(settings.GOOGLEHOOKS_LOGFILE, "a")
	except IOError:
		return
	f.write("%s: %s\n" % (datetime.datetime.now().strftime("%H:%M"), message))
	f.close()
