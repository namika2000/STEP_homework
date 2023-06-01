#! /usr/bin/python3
# homework3: Support brackets calculation


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


def read_start_bracket(line: str, index: int) -> list[dict, int]:
    token = {"type": "START_BRACKET"}
    return token, index + 1


def read_end_bracket(line: str, index: int) -> list[dict, int]:
    token = {"type": "END_BRACKET"}
    return token, index + 1


def evaluate_one_bracket(tokens: list[dict], start: int, end: int) -> list[dict]:
    """
    Calculate the simplest pair of non-nested brackets

    Args:
        tokens (list[dict]): List with {"type": str} or {"type": str, "number": float} as an element
        start (int): The index of the start bracket
        end (int): The index of the end bracket

    Returns:
        list[dict]: New tokens with one pair of brackets calculated first. List with {"type": str} or {"type": str, "number": float} as an element

    """
    number: float = evaluate(tokens[start + 1 : end])
    token: dict = {"type": "NUMBER", "number": number}
    new_tokens: list[dict] = tokens[:start] + [token] + tokens[end + 1 :]
    return new_tokens


def calculate_bracket(tokens):
    """
    Calculate the contents of brackets first

    Args:
        tokens (list[dict]): List with {"type": str} or {"type": str, "number": float} as an element

    Returns:
        list[dict]: New tokens with one pair of brackets calculated first. List with {"type": str} or {"type": str, "number": float} as an element
    """
    index = 0
    new_tokens = tokens
    start_index = []
    end_index = []
    while index < len(tokens):
        if tokens[index]["type"] == "START_BRACKET":
            start_index.append(index)
        # If you find a pair of brackets for the first time,
        # calculate inside those brackets
        if tokens[index]["type"] == "END_BRACKET":
            end_index.append(index)
            start = start_index[-1]
            end = end_index[0]
            new_tokens = evaluate_one_bracket(tokens, start, end)
            # Execute this function with new_tokens as input
            # and compute the outer brackets
            new_tokens = calculate_bracket(new_tokens)
            break
        index += 1
    return new_tokens


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
        elif line[index] == "(":
            (token, index) = read_start_bracket(line, index)
        elif line[index] == ")":
            (token, index) = read_end_bracket(line, index)
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


def evaluate(tokens: list[dict]) -> float:
    answer = 0
    if tokens[0] == {"type": "MINUS"}:  # Support negative numbers
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


def test(line: str) -> None:
    tokens = tokenize(line)
    tokens = calculate_bracket(tokens)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function:)
def run_test():
    print("==== Test started! ====")
    test("(1+1)")
    test("(1*1)")
    test("1+(1+1)+1")
    test("1-(1+1)-1")
    test("1*(1+1)-1")
    test("1-(1+1)*1")
    test("1/(1+1)*1")
    test("(2+3*(4-2/7+(2-3)*5))")
    test("2*(1+1)-3")
    test("2/(1+(2-4)*3)")
    test("2/(1+(2-4)*3)")
    test("2/(1+(2-4)*3)-8")
    test("2/(1+(2-4)*3)-8")
    test("(2+3*(4-2/7+(2-3)*5))*(2/(1+(2-4)*3)-8)")
    test("1*4-2-(2+3*(4-2/7+(2-3)*5))*(2/(1+(2-4)*3)-8)+3")
    test("(1+(1+1)+(1+1))-8")
    test("1/(2/(3-(4-1)*2)*(2-3)*3)")
    test("(-1)*3")
    test("2*(-2-3-(6/(-3))*2-1)")
    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    tokens = calculate_bracket(tokens)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
