# Lab 2 - Fun with Loops
# TAMU GEOG676
# Kenneth Struck

def multiply_list(numbers):
    product = 1
    for num in numbers:
        product *= num
    return product

def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def sum_even(numbers):
    even_total = 0
    for num in numbers:
        if num % 2 == 0:
            even_total += num
    return even_total

if __name__ == "__main__":
    part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
    part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 

    print("Part 1 result:", multiply_list(part1))
    print("Part 2 result:", sum_list(part2))
    print("Part 3 result:", sum_even(part3))
