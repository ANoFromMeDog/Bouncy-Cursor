import mouse


while True:
   pos = mouse.get_position()
   print(pos, end="")
   print()
   for x in range(50):
        print("\b", end="")
