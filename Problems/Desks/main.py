# put your python code here
# n_math_class_roms = 3
# students_per_desk = 2
import math
n_students_g1 = int(input())
n_students_g2 = int(input())
n_students_g3 = int(input())
print(math.ceil(n_students_g1 / 2)
      + math.ceil(n_students_g2 / 2)
      + math.ceil(n_students_g3 / 2))
