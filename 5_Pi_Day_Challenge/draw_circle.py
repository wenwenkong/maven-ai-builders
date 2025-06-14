import pyautogui
import math
import time

# === UPDATE THIS BASED ON YOUR SCREEN/CANVAS ===
canvas_center = (876, 429)  # use your real canvas center
calculate_button = (876, 640)
clear_button = (876, 690)
radius = 80                 # smaller is safer
steps = 360

def get_circle_points(cx, cy, r, steps=360):
    return [
        (cx + r * math.cos(math.radians(angle)),
         cy + r * math.sin(math.radians(angle)))
        for angle in range(0, 360, int(360 / steps))
    ]

def draw_circle(center, radius):
    print(f"✏️ Drawing circle at {center} with radius {radius}")
    points = get_circle_points(*center, radius)
    
    pyautogui.click(*center)  # focus canvas
    time.sleep(0.3)
    
    pyautogui.moveTo(*points[0])
    pyautogui.mouseDown()
    for x, y in points:
        pyautogui.moveTo(x, y, duration=0.003)
    pyautogui.mouseUp()

def click_calculate_button(pos):
    time.sleep(1)
    pyautogui.moveTo(*pos)
    time.sleep(0.2)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    print(f"🖱️ Clicked 'Calculate Pi' at {pos}")

def click_clear_button(pos):
    print(f"🧽 Clicking 'Clear Canvas' at {pos}")
    pyautogui.click(pos[0] - 100, pos[1])  # click nearby to wake up UI
    time.sleep(0.3)
    pyautogui.moveTo(*pos)
    time.sleep(0.2)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(0.5)

def main():
    print("🎯 Make sure the game canvas is open and visible.")
    input("✅ Press ENTER to start. You’ll have 5 seconds to switch to the game...")
    time.sleep(5)

    click_clear_button(clear_button)         # ✅ Clear canvas
    pyautogui.click(*canvas_center)          # 🖱️ Focus canvas
    time.sleep(0.3)
    draw_circle(canvas_center, radius)
    click_calculate_button(calculate_button)

if __name__ == "__main__":
    main()

