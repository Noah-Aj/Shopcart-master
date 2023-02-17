import uuid
import string
from random import shuffle


def alpha_letters(n):
    str_alpha = ''
    for i in n:
        str_alpha += i
    return str_alpha


def generate_code():
    alphabet_upper = list(string.ascii_uppercase)
    shuffle(alphabet_upper)
    first_three = alpha_letters(alphabet_upper[:3])
    shuffle(alphabet_upper)
    last_three = alpha_letters(alphabet_upper[-3:])

    code = str(uuid.uuid4()).replace("-", "")[:9]
    code_id = str(first_three) + code + str(last_three)
    return code_id

