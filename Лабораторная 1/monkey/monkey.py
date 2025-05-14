import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0
        self.furthest = 0

    def get_tokens_count(self):
        return len(self.tokens)

    def get_current_token(self):
        return self.current_token

    def match_number(self):
        token = self.peek()
        if token is not None and re.fullmatch(r'[0-9]+', token):
            self.current_token += 1
            if self.current_token > self.furthest:
                self.furthest = self.current_token
            return True
        return False

    def match(self, expected):
        if self.peek() == expected:
            self.current_token += 1
            if self.current_token > self.furthest:
                self.furthest = self.current_token
            return True
        return False

    def peek(self):
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token]
        return None

    def set_current_token(self, token):
        if token < 0 or token > len(self.tokens):
            raise ValueError('Invalid token index')
        self.current_token = token

    def maybe(self, callable):
        pos = self.get_current_token()
        if callable():
            return True
        self.set_current_token(pos)
        return False

    def get_error_index(self):
        return self.furthest


class FirstMonkeyPopulationParser(Parser):
    def __init__(self, input_str):
        tokens = input_str.strip().split()
        super().__init__(tokens)

    def parse(self):
        return self.rule1() and self.get_current_token() == self.get_tokens_count()

    def rule1(self):
        return self.maybe(lambda: self.rule2() and self.ruleZ())
    
    def ruleZ(self):
        return (self.maybe(lambda: self.match('ау') and self.rule2() and self.ruleZ())) or True

    def rule2(self):
        return self.maybe(lambda: self.rule3() and self.ruleV())

    def ruleV(self):
        return (self.maybe(lambda: self.match('ку') and self.rule3() and self.ruleV())) or True

    def rule3(self):
        return (self.maybe(lambda: self.match('ух-ты'))) or \
               self.maybe(lambda: self.match('хо') and self.rule3()) or \
               self.maybe(lambda: self.match('ну') and self.rule1() and self.match('и_ну'))


class SecondMonkeyPopulationParser(Parser):
    def __init__(self, input_str):
        tokens = input_str.strip().split()
        super().__init__(tokens)

    def parse(self):
        return self.rule1() and self.get_current_token() == self.get_tokens_count()

    def rule1(self):
        return self.maybe(lambda: self.match('ой') and self.rule2() and self.match('ай') and self.rule3())

    def rule2(self):
        if not self.match('ну'):
            return False

        while self.peek() == 'ну':
            self.match('ну')

        return True

    def rule3(self):
        return (self.maybe(lambda: self.match('ух-ты'))) or \
               (self.maybe(lambda: self.match('хо') and self.rule3() and self.match('хо')))


test_cases = [
    # Первая популяция
    "ух-ты",
    "хо ух-ты",
    "ну ух-ты и_ну",

    # Первая популяция
    "хо хо ну ух-ты и_ну",
    "ну ну ух-ты и_ну и_ну",
    "хо хо ну хо ну ух-ты и_ну и_ну",
    "хо ух-ты ау ух-ты ку хо ух-ты ку ух-ты ау хо ну ух-ты и_ну ку ух-ты",

    # Вторая популяция
    "ой ну ай ух-ты",
    "ой ну ну ай хо ух-ты хо",
    "ой ну ну ну ай хо хо хо ух-ты хо хо хо",

    # Неместные обезьяны
    "ух-ты и_ну",
    "ой ух-ты",
    "хо хо ой ну ай ух-ты",
    "ой ну ну ай хо ух-ты хо ну ух-ты и_ну",
]


def main():
    for test in test_cases:
        first_parser = FirstMonkeyPopulationParser(test)
        second_parser = SecondMonkeyPopulationParser(test)

        print(f"Тест: '{test}'. ", end='')

        if first_parser.parse():
            print("Первая популяция")
        elif second_parser.parse():
            print("Вторая популяция")
        else:
            print("Неместная обезьяна")


if __name__ == "__main__":
    main()