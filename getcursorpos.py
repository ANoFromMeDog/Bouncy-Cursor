from win32api import GetCursorPos

while True:
   pos = GetCursorPos()
   print(pos, end="\n")