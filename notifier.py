# Simple weather notification system. Sends emails or whatever when there's
# weather. I mean, I guess there's always weather, but you get the idea.
# Probably hooked up to a cron job or something.
import urllib

LOCATION = "Milwaukee"

def update():
    request = "http://www.google.com/ig/api?weather=%s" % LOCATION
    response = urllib.urlopen(request).read()

