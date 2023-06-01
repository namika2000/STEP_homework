#! /usr/bin/python3
# homework1: Support multiplication and division
# homework2: Add test cases


def read_number(line: str, index: int) -> list[dict, int]:
    number: int = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == ".":
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token: dict = {"type": "NUMBER", "number": number}
    return token, index


def read_plus(line: str, index: int) -> list[dict, int]:
    token = {"type": "PLUS"}
    return token, index + 1


def read_minus(line: str, index: int) -> list[dict, int]:
    token = {"type": "MINUS"}
    return token, index + 1


def read_multiply(line: str, index: int) -> list[dict, int]:
    token = {"type": "MULTIPLY"}
    return token, index + 1


def read_divide(line: str, index: int) -> list[dict, int]:
    token = {"type": "DIVIDE"}
    return token, index + 1


def tokenize(line: str) -> list[dict]:
    tokens: list[dict] = []
    index: int = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == "+":
            (token, index) = read_plus(line, index)
        elif line[index] == "-":
            (token, index) = read_minus(line, index)
        elif line[index] == "*":
            (token, index) = read_multiply(line, index)
        elif line[index] == "/":
            (token, index) = read_divide(line, index)
        else:
            print("Invalid character found: " + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def multiply_divide_first(tokens: list[dict]) -> list[dict]:
    """
    Calculate multiplication and division first

    Args:
        tokens (list[dict]): List with {"type": str} or {"type": str, "number": float} as an element

    Returns:
        list[dict]: New tokens with only multiplication and division calculated first. List with {"type": str} or {"type": str, "number": float} as an element

    """
    index: int = 0
    new_tokens: list[dict] = []
    while index < len(tokens):
        if tokens[index]["type"] == "MULTIPLY" or tokens[index]["type"] == "DIVIDE":
            start, end = index - 1, index + 1
            if tokens[index]["type"] == "MULTIPLY":
                number: float = tokens[start]["number"] * tokens[end]["number"]
            if tokens[index]["type"] == "DIVIDE":
                number: float = tokens[start]["number"] / tokens[end]["number"]
            # Rewrite the contents of tokens
            tokens[start]["number"] = 0  # Insert a dummy '0' token
            tokens[index] = {"type": tokens[start - 1]["type"]}  # Insert a dummy '+/-' token
            tokens[end]["number"] = number
            # Delete the most recently added tokens in new_tokens, since they are tokens[start]
            new_tokens.pop(-1)
        # Add tokens to new_tokens except "*", "/"
        else:
            new_tokens.append(tokens[index])
        index += 1
    return new_tokens


def evaluate(tokens):
    answer = 0
    if tokens[0] == {"type": "MINUS"}:  # 負の数に対応させる
        tokens.insert(0, {"type": "NUMBER", "number": 0})  # Insert a dummy '0' token
    tokens.insert(0, {"type": "PLUS"})  # Insert a dummy '+' token
    tokens = multiply_divide_first(tokens)
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "NUMBER":
            if tokens[index - 1]["type"] == "PLUS":
                answer += tokens[index]["number"]
            elif tokens[index - 1]["type"] == "MINUS":
                answer -= tokens[index]["number"]
            else:
                print("Invalid syntax")
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function:)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("-1")
    test("-1+2")
    test("-1*2")
    test("-1+2*2-1")
    test("1-2*6")
    test("2*2/8")
    test("-2*2/8")
    test("-1-2*6/3-3")
    test("-0.5")
    test("-0.5*2")
    test("-0.5*4/2.5")
    test("-0.5-3.6/4")
    test("1+1*2*2.5/5-2.4*5+8/4")
    test("2*2.5/5-2.4*5")
    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
