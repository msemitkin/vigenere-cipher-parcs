from main import alphabet
from random import randint


def generate():
    sequence_length = int(input("String length: "))
    alphabet_length = len(alphabet)
    sequence = [alphabet[randint(0, alphabet_length - 1)] for _ in range(sequence_length)]
    result = ""
    for i in sequence:
        result += i
    with open(f"test_{sequence_length}.txt", 'w') as f:
        f.write("8\n" + result)
        f.write('\n')


generate()
