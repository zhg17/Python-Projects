class RightTriangle:
    def __init__(self, hyp, leg_1, leg_2):
        self.c = hyp
        self.a = leg_1
        self.b = leg_2
        self.area = (1 / 2) * leg_1 * leg_2


# triangle from the input
input_c, input_a, input_b = [int(x) for x in input().split()]

if (input_c * input_c) == (input_a * input_a) + (input_b * input_b):
    right_triangle = RightTriangle(input_c, input_a, input_b)
    print('%.1f' % right_triangle.area)
else:
    print("Not right")
