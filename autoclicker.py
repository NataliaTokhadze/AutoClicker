import pydirectinput
import threading
import time
import keyboard
import tkinter as tk
import traceback

pydirectinput.PAUSE = 0

keys = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9',
]

Interval = 0.01        # seconds between key events
per_key_hold = 0.02  # how long to hold each keyDown before keyUp (short)
key_to_press = 'space'
toggle_key = 'p'

running = False
lock = threading.Lock()

def auto_press():
    global running
    iteration = 0
    try:
        while True:
            # sample running
            with lock:
                is_running = running
            if is_running:
       
                try:
                    # Press each key
                    for key in keys:
                        try:
                            pydirectinput.keyDown(key)
                        except Exception as e:
                            print(f"[auto_press] keyDown error for '{key}': {e}")
                        
                        time.sleep(per_key_hold)
                        try:
                            pydirectinput.keyUp(key)
                        except Exception as e:
                            print(f"[auto_press] keyUp error for '{key}': {e}")

                except Exception as e:
                    # catch unexpected errors so the thread won't die silently
                    print("[auto_press] unexpected exception in loop:")
                    traceback.print_exc()

            time.sleep(Interval)
    except Exception:
        print("[auto_press] thread-level exception (should be impossible):")
        traceback.print_exc()


debounce_seconds = 0.5
_last_toggle_time = 0.0

def handle_toggle_key(event):

    global running, _last_toggle_time
    now = time.time()
    # ignore if toggled very recently
    if now - _last_toggle_time < debounce_seconds:
        return

    with lock:
        running = not running
        state = running
    _last_toggle_time = now
    if state:
        print(f"running")
    else:
        print(f"stopped")


# Use on_press_key so the stop happens immediately on key-down
keyboard.on_press_key(toggle_key, handle_toggle_key)

def exit_on_esc():
    keyboard.wait('esc')
    print("\nClosing Program...")
    try:
        root.destroy()
    except Exception:
        pass
    try:
        root.quit()
    except Exception:
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # hotkey registration (non-blocking)
    threading.Thread(target=auto_press, daemon=True).start()
    threading.Thread(target=exit_on_esc, daemon=True).start()

    print("Press 'p' to Start/Stop. Press 'ESC' to close.")
    root.mainloop()
