word_input = input()


def camel_case_to_snake_case(word):
    snake_case = ''
    idx = 0
    for letter in word:
        if str.isupper(letter):
            if idx == 0:
                snake_case += str.lower(letter)
            else:
                snake_case += f'_{str.lower(letter)}'
        else:
            snake_case += letter
        idx += 1
    return snake_case


print(camel_case_to_snake_case(word_input))
