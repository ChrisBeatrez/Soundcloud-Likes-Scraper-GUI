from cx_Freeze import setup, Executable
import sys

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"    # Tells the build script to hide the console.

setup(name="Soundcloud Scraper",
      version="0.1",
      description="",
      executables=[Executable("main.py", base=base)])