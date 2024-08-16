import re
import pprint

class InfoboxParser:
    def __init__(self, content):
        self.content = content
        self.infobox_data = self.parse_infobox()

    def parse_infobox(self):
        # Find the start of the infobox
        infobox_start = self.content.find("{{Infobox")
        if infobox_start == -1:
            return None  # Infobox not found

        # Find the end of the infobox
        infobox_end = self.content.find("\n}}", infobox_start)
        if (infobox_end == -1):
            infobox_end = len(self.content)  # In case there's no explicit end, take till the end of content

        # Extract the infobox content
        infobox_content = self.content[infobox_start:infobox_end+3].strip()  # Include closing '}}'

        # Parse key-value pairs
        infobox_data = {}
        current_key = None
        current_value = []

        for line in infobox_content.splitlines():
            # Check for new key-value pair
            key_match = re.match(r'\|\s*(\w+)\s*=\s*(.*)', line)
            if key_match:
                if current_key:  # Save the previous key-value pair
                    infobox_data[current_key] = "\n".join(current_value).strip()
                current_key = key_match.group(1)
                current_value = [key_match.group(2).strip()]
            elif current_key:  # Continue value for the current key
                current_value.append(line.strip())

        # Don't forget the last key-value pair
        if current_key:
            infobox_data[current_key] = "\n".join(current_value).strip()

        return infobox_data

    def pretty_print(self):
        pprint.pprint(self.infobox_data, indent=2)

# Example usage
# content = """
# {{Infobox album
# | name        = Lysol
# | type        = studio
# | artist      = Melvins
# | cover       = Melvins-Lysol-Cover.jpg
# | alt         =
# | released    = [[July 1]], [[1992]]
# | recorded    =
# | studio      = Razor's Edge Recording, San Francisco, California
# | genre       = {{hlist|[[Drone metal]]<ref name="dsd">{{cite web | url = http://drownedinsound.com/releases/14698/reviews/4138018 | title = Melvins - Chicken Switch review | publisher = [[Drowned in Sound]] | author = Gardner, Noel | date = October 2, 2009 | accessdate = October 2, 2014 | archive-date = October 6, 2014 | archive-url = https://web.archive.org/web/20141006150155/http://drownedinsound.com/releases/14698/reviews/4138018 | url-status = dead }}</ref>|[[doom metal]]|[[noise rock]]<ref name="pitchfork">{{cite web|url=https://pitchfork.com/thepitch/717-the-revival-of-cherubs/|title=The Revival of Cherubs|last=Earles|first=Andrew|publisher=Pitchfork|date=March 31, 2015|accessdate=October 16, 2017}}</ref>}}
# | length      = {{Duration|31|23}}
# | label       = [[Boner Records]]
# | producer    = [[Melvins]]
# }}
# """
#
# parser = InfoboxParser(content)
# parser.pretty_print()
