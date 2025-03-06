import random
import string


class TextGenerator:

    def generate_random_text(self, length: int, use_letters: bool = True, use_digits: bool = True) -> str:
        charset = ""
        if use_letters:
            charset += string.ascii_letters
        if use_digits:
            charset += string.digits
        if not charset:
            raise ValueError("At least one of 'use_letters' or 'use_digits' must be True.")
        return ''.join(random.choices(charset, k=length))