import week10library

def Menu():
    print("Calculate the Area of: ")
    print("(1) Rectangle")
    print("(2) Triangle")
    print("(3) Circle")
    print("(q) Quit")
    command = input("Enter:")
    return command

command = Menu()

while command != "q":
    if command == "1":
        height = float(input("Enter the height: "))
        width = float(input("Enter the width: "))
        Area = week10library.RectangleArea(height,width)
    elif command == "2":
        height = float(input("Enter the height: "))
        width = float(input("Enter the width: "))
        Area = week10library.TriangleArea(height,width)
    elif command == "3":
        radius = float(input("Enter the radius: "))
        Area = week10library.CircleArea(radius)
    print("Area: ",Area)
    command = Menu()

