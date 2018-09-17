import pulseio
import board
import time
import math


def lerp(start, stop, amount):
    """Linearly interpolate amount between start and stop.

    Source: https://en.wikipedia.org/wiki/Linear_interpolation#Programming_language_support"""
    return (1 - amount) * start + amount * stop


def get_current_value(time_s, sequence):
    """Get the interpolated value as defined by a sequence of values and a timestamp.

    sequence is a list of 1 second interval values for the LED.
    time_s is the time in seconds (float)"""
    sequence_index = math.floor(time_s) % len(sequence)
    subsecond_progress = time_s % 1
    next_index = (sequence_index + 1) % len(sequence)
    return lerp(sequence[sequence_index], sequence[next_index], subsecond_progress)


def main():
    """Main execution and loop"""
    # Setup Pulse Width Modulation on digital pin 13 (red LED)
    pwm = pulseio.PWMOut(board.D13)

    # Timing source:
    # https://www.mindbodygreen.com/0-4386/A-Simple-Breathing-Exercise-to-Calm-Your-Mind-Body.html
    value_sequence = [0.0, 0.5, 1.0, 1.0, 0.75, 0.5, 0.25, 0.0]
    last_time = time.monotonic()
    while True:
        time_delta = time.monotonic() - last_time
        value = get_current_value(time_delta, value_sequence)
        pwm.duty_cycle = int((2 ** 16 - 1) * value)

        # Stop time_delta from getting too big
        if time_delta > len(value_sequence):
            last_time = time.monotonic()


# Run the main function
main()
