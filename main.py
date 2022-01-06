# -*- coding: utf-8 -*-

"""This code takes a video source and temporarily applies it as your desktop
wallpaper for the desired duration. Afterwards, your previous wallpaper is
restored."""
__author__ = "Guimoute (https://github.com/Guimoute)"

# Constants.
LIVE_WALLPAPER_DURATION = 5
LIVE_WALLPAPER_FPS = 30 # Do not be greedy here.
VIDEO_SOURCE:int = 0
PRELOAD_VIDEO_SOURCE:bool = True

# Imports.
import ctypes
import cv2
import os
import time
import win32con

# Helper functions.
    # Courtesy of https://stackoverflow.com/a/66775957/9282844
def get_wallpaper() -> str:
    buffer = ctypes.create_unicode_buffer(2**8)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER, len(buffer), buffer, 0)
    return buffer.value

    # Courtesy of https://stackoverflow.com/a/20024286/9282844
def set_wallpaper(path:str):
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path, 0)



if __name__ == "__main__":

    # Backup current wallpaper.
    old_wallpaper_path = get_wallpaper()

    # Try to open the selected video source.
    source = cv2.VideoCapture(VIDEO_SOURCE) # This line may take 10s, be patient.
    if source is None or not source.isOpened():
        raise ValueError("This video source is not available.")

    if PRELOAD_VIDEO_SOURCE:
        input("Press any key to start the live wallpaper.")

    # For a user-specified time, update the wallpaper with the current video feed's latest image.
    live_image_path = os.path.join(os.path.dirname(__file__), "your_live_face.png")
    sleep_time = 1/LIVE_WALLPAPER_FPS
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < LIVE_WALLPAPER_DURATION:
        success, frame = source.read()
        if success:
            cv2.imwrite(live_image_path, frame)
            set_wallpaper(live_image_path)
        time.sleep(sleep_time)

    # Final clean-up.
    set_wallpaper(old_wallpaper_path)
    source.release()
    os.remove(live_image_path)

