#! /usr/bin/python3


def read_number(line, index):
    number = 0
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
    token = {"type": "NUMBER", "number": number}
    return token, index


def read_plus(line, index):
    token = {"type": "PLUS"}
    return token, index + 1


def read_minus(line, index):
    token = {"type": "MINUS"}
    return token, index + 1


def read_multiply(line, index):
    token = {"type": "MULTIPLY"}
    return token, index + 1


def read_divide(line, index):
    token = {"type": "DIVIDE"}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
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


# 先に掛け算、割り算だけ計算する
# Calculate multiplication and division first
#
# |tokens|: tokens
# Returns: |tokens| 掛け算、割り算だけ計算した新たなtokens
def multiply_divide_first(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]["type"] == "MULTIPLY" or tokens[index]["type"] == "DIVIDE":
            # print("-----元のtokens", tokens)
            start, end = index - 1, index + 1
            if tokens[index]["type"] == "MULTIPLY":
                number = tokens[start]["number"] * tokens[end]["number"]
            if tokens[index]["type"] == "DIVIDE":
                number = tokens[start]["number"] / tokens[end]["number"]
            # Rewrite the contents of tokens
            tokens[start]["number"] = 0  # Insert a dummy '0' token
            tokens[index] = {"type": tokens[start - 1]["type"]}  # Insert a dummy '+/-' token
            tokens[end]["number"] = number
            # print("掛け算割り算した後のtokens", tokens)
        index += 1
    return tokens


def evaluate(tokens):
    answer = 0
    # 負の数の入力を許容
    if tokens[0] == {"type": "MINUS"}:
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
