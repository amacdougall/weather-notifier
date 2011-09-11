# Simple weather notification system. Sends emails or whatever when there's
# weather. I mean, I guess there's always weather, but you get the idea.
# Probably hooked up to a cron job or something.
import urllib

LOCATION = "Milwaukee"

def update():
    request = "http://www.google.com/ig/api?weather=%s" % LOCATION
    response = xml.dom.minidom.parse(urlopen(request))
    temperature_node = find_node(reponse, "temp_f")
    temperature = temperature_node.attributes["data"].firstChild.nodeValue;
    # TODO: do something with the temperature

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
