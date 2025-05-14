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


class RobotParser(Parser):
    def __init__(self, input_str):
        tokens = input_str.strip().split()
        super().__init__(tokens)

    def parse(self):
        return self.start() and self.get_current_token() == self.get_tokens_count()

    def start(self):
        return self.maybe(lambda: self.match('start') and self.rule1() and self.match('stop'))

    def rule1(self):
        return self.maybe(lambda: self.rule2() and self.ruleZ())

    def ruleZ(self):
        return (self.maybe(lambda: self.rule4() and self.rule2() and self.ruleZ()) or True)

    def rule2(self):
        return self.maybe(lambda: self.rule3() and self.ruleV())

    def ruleV(self):
        return (self.maybe(lambda: self.rule5() and self.rule3() and self.ruleV())) or True

    def rule3(self):
        return (self.maybe(lambda: self.match('left'))) or \
               self.maybe(lambda: self.match('right')) or \
               self.maybe(lambda: self.match('on45') and self.rule3()) or \
               self.maybe(lambda: self.match('hands_up') and self.rule1() and self.match('hands_down'))

    def rule4(self):
        return self.maybe(lambda: self.match('step_(') and self.rule6() and self.match(')'))

    def rule5(self):
        return self.maybe(lambda: self.match('turn_head'))

    def rule6(self):
        return (self.maybe(lambda: self.match_number()) or
                self.maybe(lambda: self.match_number() and self.rule6()))


test_cases = [
    "start  left stop",  # OK 3
    "start  left  turn_head on45 left step_( 9 )  on45 right step_( 9 ) left  stop",  # OK 15
    "start    stop",  # ERR 2
    "start  on45 on45 on45 on45 on45 left stop",  # OK 8
    "start left  step_( 67890 )  hands_up  hands_up  hands_up  left hands_down  hands_down hands_down stop",  # OK 13
]


def main():
    for test in test_cases:
        parser = RobotParser(test)

        print(f"Тест: '{test}'. ", end='')
        
        success = parser.parse()
        if success:
            print("OK", end=' ')
        else:
            print("ERR", end=' ')

        print(parser.get_tokens_count() if success else parser.get_error_index() + 1)


if __name__ == "__main__":
    main()