# Cura PostProcessingPlugin
# Author:   Samuel Roberts
# Date:     15th July 2020

# Description:  Show time remaining and layer progress on the LCD

import re
import datetime

from ..Script import Script

class DisplayTimeAndLayerOnLCD(Script):
    
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Display Time and Layer on LCD",
            "key": "DisplayTimeAndLayerOnLCD",
            "metadata": {},
            "version": 2,
            "settings":
            {
                
            }
        }"""
    
    def execute(self, data):
        time_string = "??:??:??"
        max_layer = 0
        current_layer = 0

        for layer in data:

            layer_index = data.index(layer)
            lines = layer.split("\n")

            for line in lines:

                # Handle time
                if line.startswith(";TIME:"):
                    line_index = lines.index(line)          # We take a hold of that line
                    split_string = re.split(":", line)      # Then we split it, so we can get the number

                    string_with_numbers = "{}".format(split_string[1])      # Here we insert that number from the
                                                                            # list into a string.
                    total_time = int(string_with_numbers)                   # Only to contert it to a int.

                    m, s = divmod(total_time, 60)    # Math to calculate
                    h, m = divmod(m, 60)             # hours, minutes and seconds.
                    time_string = "{:d}h {:02d}m {:02d}s".format(h, m, s)           # Now we put it into the string

                elif line.startswith(";TIME_ELAPSED:"):
                    line_index = lines.index(line)          # We get a hold of the line
                    list_split = re.split(":", line)        # Again, we split at ":" so we can get the number
                    string_with_numbers = "{}".format(list_split[1])   # Then we put that number from the list, into a string

                    current_time = float(string_with_numbers)       # This time we convert to a float, as the line looks something like:
                                                                    # ;TIME_ELAPSED:1234.6789
                                                                    # which is total time in seconds

                    time_left = total_time - current_time   # Here we calculate remaining time
                    m1, s1 = divmod(time_left, 60)          # And some math to get the total time in seconds into
                    h1, m1 = divmod(m1, 60)                 # the right format. (HH,MM,SS)
                    time_string = "{:d}h {:2d}m {:2d}s".format(int(h1), int(m1), int(s1))   # Here we create the string holding our time

                # Handle layers
                if line.startswith(";LAYER_COUNT:"):
                    max_layer = line
                    max_layer = max_layer.split(":")[1]

                if line.startswith(";LAYER:"):
                    current_layer += 1
                    display_text = "M117 {} ({}/{})".format(time_string, current_layer, max_layer)
                    line_index = lines.index(line)
                    lines.insert(line_index + 1, display_text)
            
            final_lines = "\n".join(lines)
            data[layer_index] = final_lines
            
        return data
                    
        

