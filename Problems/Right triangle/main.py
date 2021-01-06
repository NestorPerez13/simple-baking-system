class RightTriangle:
    def __init__(self, hyp, leg_1, leg_2):
        self.c = hyp
        self.a = leg_1
        self.b = leg_2
        # calculate the area here
        self.is_right = (self.a ** 2 + self.b ** 2) == self.c ** 2
        self.area = (self.a * self.b) * 0.5


# triangle from the input
input_c, input_a, input_b = [int(x) for x in input().split()]

# write your code here
rect = RightTriangle(input_c, input_a, input_b)
if not rect.is_right:
    print("Not right")
else:
    print(f"{rect.area:.1f}")
