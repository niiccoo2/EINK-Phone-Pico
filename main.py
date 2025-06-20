from machine import Pin, I2C
from mcp23017 import MCP23017
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
print(i2c.scan())  # Should print a list like [32]


mcp = MCP23017(i2c)

cols = [1, 0, 15, 14, 13, 12, 11, 10, 9, 8]
rows = [2, 3, 4, 5, 6]

keymap = {
    (0, 0): '1', (0, 1): '2', (0, 2): '3', (0, 3): '4', (0, 4): '5', (0, 5): '6', (0, 6): '7', (0, 7): '8', (0, 8): '9', (0, 9): '0',
    (1, 0): 'Q', (1, 1): 'W', (1, 2): 'E', (1, 3): 'R', (1, 4): 'T', (1, 5): 'Y', (1, 6): 'U', (1, 7): 'I', (1, 8): 'O', (1, 9): 'P',
    (2, 0): 'A', (2, 1): 'S', (2, 2): 'D', (2, 3): 'F', (2, 4): 'G', (2, 5): 'H', (2, 6): 'J', (2, 7): 'K', (2, 8): 'L', (2, 9): 'Backspace',
    (3, 0): 'Z', (3, 1): 'X', (3, 2): 'C', (3, 3): 'V', (3, 4): 'B', (3, 5): 'N', (3, 6): 'M', (3, 7): ',', (3, 8): '.', (3, 9): 'Enter',
    (4, 0): 'Escape', (4, 1): 'Shift', (4, 2): 'Symbol', (4, 3): 'Space'
}


# Setup rows as outputs, start HIGH
for r in rows:
    mcp.pin(r, mode=0, value=1)

# Setup cols as inputs with pull-ups
for c in cols:
    mcp.pin(c, mode=1, pullup=1)

def scan_matrix():
    pressed_keys = []
    for r in rows:
        mcp.pin(r, value=0)  # Drive this row LOW
        time.sleep_ms(1)      # Small delay for signal to settle
        for c_index, c in enumerate(cols):
            if mcp.pin(c) == 0:  # Active LOW means key pressed
                pressed_keys.append((rows.index(r), c_index))
        mcp.pin(r, value=1)  # Drive row back HIGH
    return pressed_keys

while True:
    keys = scan_matrix()
    if keys:
        key_labels = []
        for k in keys:
            label = keymap.get(k, f"({k[0]},{k[1]})")
            key_labels.append(label)
        print("Keys pressed:", key_labels)
    time.sleep(0.1)
