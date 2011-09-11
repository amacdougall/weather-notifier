# Simple weather notification system. Sends emails or whatever when there's
# weather. I mean, I guess there's always weather, but you get the idea.
# Probably hooked up to a cron job or something.
import os
import xml.dom.minidom
from datetime import datetime
from urllib import urlopen

# email configuration
SENDER = "smoke@alanmacdougall.com"
RECIPIENTS = ("smoke@alanmacdougall.com", "nigel.wade7@gmail.com")
SUBJECT = "Weather Update"
BODY = """The temperature outside is now %d, which is within the target range
for MAXIMUM ENJOYMENT. Go outside and play! Unless you have to 'work,' like some
kind of 'responsible adult.' In which case keep a flask in your desk drawer."""

# weather configuration
LOCATION = "Milwaukee"
TARGET_RANGE = (68, 82)
TEMPERATURE_RECORD = "last_temperature.txt"

def update():
    request = "http://www.google.com/ig/api?weather=%s" % LOCATION
    response = xml.dom.minidom.parse(urlopen(request))
    temperature_node = find_node(response, "temp_f")

    temperature = int(temperature_node.attributes["data"].firstChild.nodeValue)
    last_temperature = get_last_temperature()

    if temperature_in_range(temperature):
        # if it just suddenly became a nice day...
        if not temperature_in_range(last_temperature):
            test_weather_update(temperature, "Entered optimal range.")
        else:
            test_weather_update(temperature, "Still in optimal range.")
    else:
        # if it was a nice day and now it's not...
        if temperature_in_range(last_temperature):
            test_weather_update(temperature, "Left optimal range.")
        else:
            test_weather_update(temperature, "Still outside optimal range.")

    save_temperature(temperature)

def temperature_in_range(temperature):
    """True if the supplied temperature is within TARGET_RANGE."""
    min, max = TARGET_RANGE
    return number_in_range(temperature, min, max)

def get_last_temperature():
    """Return the most recently recorded temperature in the log, creating a log
    file if necessary."""
    if os.path.exists(TEMPERATURE_RECORD):
        contents = open(TEMPERATURE_RECORD).read()
        if len(contents) > 0:
            return int(contents)
        else:
            return 0
    else:
        return 0
    
def save_temperature(temperature):
    file(TEMPERATURE_RECORD, "w").write(str(temperature))

# utility
def find_node(root, target_name):
    """Starting from the root node, return the first node with the
    target_name."""

    if root.localName == target_name:
        return root
    elif len(root.childNodes) > 0:
        for node in root.childNodes:
            if node.localName == target_name:
                return node
            elif len(node.childNodes) > 0:
                found = find_node(node, target_name)
                if found is not None:
                    return found
        return None
    else:
        return None

def number_in_range(n, min, max):
    """True if n is within the supplied range."""
    if n >= min and n <= max:
        return True
    else:
        return False

def test_weather_update(temperature, message):
    if not os.path.exists("test.log"):
        log_file = file("test.log", "w")
    else:
        log_file = file("test.log", "a")

    debug_output = "%d degrees, observed %s: %s\n" 
    timestamp = datetime.now().strftime("%H:%M:%S, %Y-%m-%d")
    log_file.write(debug_output % (temperature, timestamp, message))

def send_weather_update(temperature):
    try:
        """Send email with the supplied message."""
        sendmail_location = "/usr/sbin/sendmail" # sendmail location
        p = os.popen("%s -t" % sendmail_location, "w")
        p.write("From: %s\n" % SENDER)
        p.write("To: %s\n" % ",".join(RECIPIENTS))
        p.write("Subject: %s\n" % SUBJECT)
        p.write("\n") # blank line separating headers from body
        p.write(BODY % temperature)
        status = p.close()
        if status != 0:
            # TODO: maybe some kind of logging later?
            pass
    except Exception as error:
        pass
