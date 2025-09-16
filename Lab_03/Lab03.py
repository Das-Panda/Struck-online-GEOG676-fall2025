import math

# === Base Shape Class ===
class Shape:
    def area(self):
        raise NotImplementedError("Area method must be implemented by subclass.")

    def perimeter(self):
        raise NotImplementedError("Perimeter method must be implemented by subclass.")

# === Circle ===
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius**2

    def perimeter(self):
        return 2 * math.pi * self.radius

# === Square ===
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side**2

    def perimeter(self):
        return 4 * self.side

# === Rectangle ===
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

# === Triangle (new) ===
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def perimeter(self):
        # Assume right triangle: perimeter = base + height + hypotenuse
        hypotenuse = math.sqrt(self.base**2 + self.height**2)
        return self.base + self.height + hypotenuse

# === Read and Process Shape File ===
def process_shapes(filepath):
    shapes = []

    try:
        with open(filepath, 'r') as file:
            for line_num, line in enumerate(file, 1):
                parts = line.strip().split(',')

                try:
                    shape_type = parts[0].strip().lower()

                    if shape_type == 'circle' and len(parts) == 2:
                        radius = float(parts[1])
                        shape = Circle(radius)

                    elif shape_type == 'square' and len(parts) == 2:
                        side = float(parts[1])
                        shape = Square(side)

                    elif shape_type == 'rectangle' and len(parts) == 3:
                        length = float(parts[1])
                        width = float(parts[2])
                        shape = Rectangle(length, width)

                    elif shape_type == 'triangle' and len(parts) == 3:
                        base = float(parts[1])
                        height = float(parts[2])
                        shape = Triangle(base, height)

                    else:
                        raise ValueError("Invalid parameters or shape type.")

                    shapes.append((shape_type.capitalize(), shape))

                except Exception as e:
                    print(f"Error on line {line_num}: '{line.strip()}' — {e}")

    except FileNotFoundError:
        print(f"File not found: {filepath}")

    return shapes

# === Display Output ===
def display_shapes(shapes):
    for name, shape in shapes:
        print(f"{name}: Area = {shape.area():.2f}, Perimeter = {shape.perimeter():.2f}")

# === Main Program ===
if __name__ == "__main__":
    filepath = r"C:\Users\kenne\Desktop\TAMU Fall 2025\GEOG 676 701 GIS PROGRAMMING\Module 4\shape.txt"
    shapes = process_shapes(filepath)
    display_shapes(shapes)
