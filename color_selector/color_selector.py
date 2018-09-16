import time
import math
from adafruit_circuitplayground.express import cpx

# Set the overall brightness of the pixels.
# Adjust this between 0 and 1 if you want
cpx.pixels.brightness = 0.3

# Starting point in time for the start of the script
starting_time = time.monotonic()


class RGBSelector:
    """Class to control the red, green, and blue channel selection pixels"""
    def __init__(self):
        # Channel names in english so it's easier to test for them in code
        self.channels = ('red', 'green', 'blue')

        # The number of each pixel on the Circuit Playground Express board
        self.led_index = {
            'red': 8,
            'green': 7,
            'blue': 6
        }

        # The index of the channel selected (0, 1, or 2)
        self.selected = 0

    def select(self, color):
        """Select a color channel from a string.

        Can be 'red', 'green' or 'blue'."""
        if (color not in ('red', 'green', 'blue')):
            raise ValueError('{} is not a valid color'.format(color))
        self.selected = self.channels.index(color)

    def next_color(self):
        """Select the next color in the sequence [red, green, blue]

        Prints the selected color"""
        self.selected = self.selected + 1 if self.selected < 2 else 0
        print('Active channel: {}'.format(self.channels[self.selected]))

    def render(self, time_since_start):
        """Render the pulsing of the selected color.

        Generally, you should pass `time.monotonic() - starting_time`
        to this method."""
        # The intensity of the selected pixel is a value from 0 to 1
        # This sin function determines how bright to make the pixel based
        # on how long it's been since the start of the script.
        intensity = 0.5 * math.sin(time_since_start * 4 - (math.pi / 4.0)) + 0.5

        # This set of if-else statements tells the program whether to display
        # a solid color, or a pulsing one defined by `intensity`
        if (self.channels[self.selected] == 'red'):
            # cpx.pixels[] expects an integer index between 0 and 9 and lets us set the color of that pixel
            # self.led_index[] expects a key of 'red', 'green' or 'blue' and returns an integer
            # self.channels[] expects an integer index between 0 and 2 and returns a string
            # self.selected is an integer between 0 and 2
            cpx.pixels[self.led_index[self.channels[self.selected]]] = (math.floor(255 * intensity), 0, 0)
        else:
            cpx.pixels[self.led_index['red']] = (255, 0, 0)

        if (self.channels[self.selected] == 'green'):
            cpx.pixels[self.led_index[self.channels[self.selected]]] = (0, math.floor(255 * intensity), 0)
        else:
            cpx.pixels[self.led_index['green']] = (0, 255, 0)

        if (self.channels[self.selected] == 'blue'):
            cpx.pixels[self.led_index[self.channels[self.selected]]] = (0, 0, math.floor(255 * intensity))
        else:
            cpx.pixels[self.led_index['blue']] = (0, 0, 255)


class ColorDisplay:
    """Class for controlling the color display of the preview pixel."""
    def __init__(self):
        # The index of the pixel is 2
        self.ledPin = 2

        # The starting values of red, green and blue
        self.values = (0, 0, 0)

    def set(self, channel_index, value):
        """Given a channel index [0-2] and a value, set the value of that channel."""
        if channel_index == 0:
            self.set_r(value)
        elif channel_index == 1:
            self.set_g(value)
        elif channel_index == 2:
            self.set_b(value)
        else:
            error = 'Channel "{}" is not a valid channel'.format(channel_index)
            raise ValueError(error)

    def set_r(self, value):
        "Set the red channel to value."
        self.values = (value, self.values[1], self.values[2])

    def set_g(self, value):
        "Set the green channel to value."
        self.values = (self.values[0], value, self.values[2])

    def set_b(self, value):
        "Set the blue channel to value."
        self.values = (self.values[0], self.values[1], value)

    def display(self):
        "Display the current color stored in self.values"
        cpx.pixels[self.ledPin] = self.values


def main():
    """Program loop"""
    # Instantiate the RGBSelector and the ColorDisplay
    selector = RGBSelector()
    display = ColorDisplay()

    # Record the initial state of button B before the loop starts
    last_button_b = cpx.button_b

    # Loop forever
    while True:
        # Test if the B button is pressed
        current_button_b = cpx.button_b

        # If the B button is pressed and it wasn't pressed during
        # the previous loop, then move to the next color.
        # If we didn't do this, then the colors would rotate
        # very quickly as long as you held down the button.
        if current_button_b and not last_button_b:
            selector.next_color()

        # If button A is pressed, increment the value of the selected channel by 2
        # As the button is held down, more and more of the selected channel will be
        # displayed in the preview pixel.
        if cpx.button_a:
            # The "% 255" means the value will loop back to zero after 255
            new_value = (display.values[selector.selected] + 2) % 255
            display.set(selector.selected, new_value)
            print(display.values)

        # Update the pulsing of the selector pixels
        selector.render(time.monotonic() - starting_time)

        # Update the display of the preview pixel
        display.display()

        # Record the state of button B for this loop
        last_button_b = current_button_b


# Run the program
main()
