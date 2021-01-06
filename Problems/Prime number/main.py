number_input = int(input())


def is_prime(number):
    if number > 1:
        for x in range(2, number):
            if number % x == 0:
                return "This number is not prime"
        return "This number is prime"
    else:
        return "This number is not prime"


print(is_prime(number_input))
