# put your python code here
a = int(input())
b = int(input())
numbers = []
for value in range(a, b + 1):
    if value % 3 == 0:
        numbers.append(value)

print(sum(numbers) / len(numbers))
