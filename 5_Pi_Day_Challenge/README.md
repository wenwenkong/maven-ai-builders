# Pi Day Challenge Automation

This project uses Python and `pyautogui` to automatically draw a perfect circle in the [Pi Day Challenge](https://yage.ai/genai/pi.html) game and then calculate the accuracy.

The goal is to simulate a mouse-drawn circle on the canvas to achieve a high Pi approximation score.

---

## Features

- Draws a smooth circle on the canvas using mouse automation
- Clicks the "Clear Canvas" button to reset the canvas before each run
- Clicks the "Calculate Pi" button to get the result
- Includes configurable timing and positioning

---

## Calibrate positions

Before using the script, you need to determine 3 screen positions:
- Canvas center
- "Clear Canvas" button
- "Calculate Pi" button

To find these, run
```
python3 -m pyautogui
```

Then hover over the center of the canvas and the two buttons to get their `(x, y)` values. Update these values in the `draw_circle.py` script.

---

## Note

Make sure place the browser on your primary monitor, even if you are using an external monitor. 
