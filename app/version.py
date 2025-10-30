import sys
import os

print("Python 版本:", sys.version)
print("Python Executable:", sys.executable)
print("Virtual Environment Path:", os.path.dirname(sys.executable))
print("Site Packages Path:", sys.path)