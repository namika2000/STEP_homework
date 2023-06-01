#! /usr/bin/python3
# homework4: Support abs(), int(), round()


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


def read_char(line: str, index: int) -> list[dict, int]:
    """
    Read strings and returns their type and the index of the next character
    Return an error if the string read is nor abs, int, or round

    Args:
        line (str): Strings as input
        index (int): The index of the string

    Returns:
        list[dict, int]: The token  indicating the type of the string
                        and the index of the next character to be read.
    """
    string: str = ""
    type_list: list[str] = ["abs", "int", "round"]
    while index < len(line) and line[index].isalpha():
        string += line[index]
        index += 1
    if string in type_list:
        token: dict() = {"type": string}
    else:
        print("Invalid character found: " + string)
        exit()
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


def abs_cal(num: float) -> float:
    ans = num
    if num < 0:
        ans *= -1
    return ans


def int_cal(num: float) -> float:
    is_negative = False
    if num < 0:
        num = abs_cal(num)
        is_negative = True
    ans = num // 1
    if is_negative:
        ans *= -1
    return ans


def round_cal(num: float) -> float:
    is_negative = False
    if num < 0:
        num = abs_cal(num)
        is_negative = True
    num_int = int_cal(num)
    first_decimal_num = (num - num_int) * 10 // 1
    if first_decimal_num >= 5:
        ans = num_int + 1
    else:
        ans = num_int
    if is_negative:
        ans *= -1
    return ans


def complicate_calculation(tokens: list[dict], index: int, type: str) -> list[dict]:
    """
    Calculate corresponding to type(abs,int,round)

    Args:
        tokens (list[dict]): List with {"type": str} or {"type": str, "number": float} as an element
        index (int): The index of the result of the calculation inside of brackets
        type (str): The type of the strings before brackets

    Returns:
        list[dict]: New tokens after calculation corresponding to type(abs,int,round). List with {"type": str} or {"type": str, "number": float} as an element
    """
    num = tokens[index]["number"]
    if type == "abs":
        ans = abs_cal(num)
    elif type == "int":
        ans = int_cal(num)
    else:
        ans = round_cal(num)
    token = {"type": "NUMBER", "number": ans}
    new_tokens = tokens[: index - 1] + [token] + tokens[index + 1 :]
    return new_tokens


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
            type = new_tokens[start - 1]["type"]
            new_tokens = evaluate_one_bracket(tokens, start, end)
            # calculate according to type(abs, int, round)
            if type in ["abs", "int", "round"]:
                new_tokens = complicate_calculation(new_tokens, start, type)
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
        elif line[index].isalpha:
            (token, index) = read_char(line, index)
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
    test("1+1")
    test("abs(3.4)")
    test("int(3.4)")
    test("round(3.4)")
    test("abs(-3.4)")
    test("int(-3.4)")
    test("round(-3.4)")
    test("abs(3.6)")
    test("int(3.6)")
    test("round(3.6)")
    test("abs(-3.6)")
    test("int(-3.6)")
    test("round(-3.6)")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")
    test("2*abs(2/int(1+3.4*2.3)+round(abs(int(3-3.7)))+2/3)")
    test("ab(1)")
    test("abc(1)")
    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    tokens = calculate_bracket(tokens)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
