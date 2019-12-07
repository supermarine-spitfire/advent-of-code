print("Running script")

lower_limit = 0
upper_limit = 6
step = -1
m = int(input("Enter number: "))
for n in range(upper_limit, lower_limit, step):
    left = m % 10 ** n // 10 ** (n - 1)
    right = m % 10 ** (n - 1) // 10 ** (n - 2)
    print(f"n: {n}")
    print(f"left: {left}")
    print(f"right: {right}")
