import time
import board
import analogio

# Initialize the analog input on pin GP27_A1
analog_in = analogio.AnalogIn(board.GP27_A1)

def get_voltage(pin):
    # Convert the analog reading to a voltage
    return (pin.value * 3.3) / 65536

def get_resistance(voltage):
    # Assuming a simple voltage divider with a known resistor value
    known_resistor = 10000  # 10k ohms
    return known_resistor * (3.3 / voltage - 1)

while True:
    voltage = get_voltage(analog_in)
    resistance = get_resistance(voltage)
    print(f"Voltage: {voltage:.2f} V, Resistance: {resistance / 1000:.2f} kOhms")
    time.sleep(1)