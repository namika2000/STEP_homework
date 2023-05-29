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


def read_start_bracket(line, index):
    token = {"type": "START_BRACKET"}
    return token, index + 1


def read_end_bracket(line, index):
    token = {"type": "END_BRACKET"}
    return token, index + 1


def evaluate_one_bracket(tokens, start, end):
    number = evaluate(tokens[start + 1 : end])
    token = {"type": "NUMBER", "number": number}
    new_tokens = tokens[:start] + [token] + tokens[end + 1 :]
    return new_tokens


def calculate_bracket(tokens):
    index = 0
    new_tokens = tokens
    start_index = []
    end_index = []
    while index < len(tokens):
        if tokens[index]["type"] == "START_BRACKET":
            start_index.append(index)
        # 初めて括弧の組を見つけたら
        if tokens[index]["type"] == "END_BRACKET":
            end_index.append(index)
            start = start_index[-1]
            end = end_index[0]
            new_tokens = evaluate_one_bracket(tokens, start, end)
            new_tokens = calculate_bracket(new_tokens)
            break
        index += 1
    return new_tokens


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
        elif line[index] == "(":
            (token, index) = read_start_bracket(line, index)
        elif line[index] == ")":
            (token, index) = read_end_bracket(line, index)
        # スペースを許容
        elif line[index] == " ":
            index += 1
            continue
        else:
            print("Invalid character found: " + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# 先に掛け算、割り算だけ計算する
# 括弧の計算に対応できるようmultiply_divide_first()に修正を加えた
# Calculate multiplication and division first
#
# |tokens|: tokens
# Returns: |tokens| 掛け算、割り算だけ計算した新たなtokens
def update_multiply_divide_first(tokens):
    index = 0
    new_tokens = []
    while index < len(tokens):
        if tokens[index]["type"] == "MULTIPLY" or tokens[index]["type"] == "DIVIDE":
            start, end = index - 1, index + 1
            if tokens[index]["type"] == "MULTIPLY":
                number = tokens[start]["number"] * tokens[end]["number"]
            if tokens[index]["type"] == "DIVIDE":
                number = tokens[start]["number"] / tokens[end]["number"]
            # Rewrite the contents of tokens
            tokens[start]["number"] = 0  # Insert a dummy '0' token
            tokens[index] = {"type": tokens[start - 1]["type"]}  # Insert a dummy '+/-' token
            tokens[end]["number"] = number
            # 直近にnew_tokensに追加したものはtokens[start]に当たるので消去
            new_tokens.pop(-1)
        # "*", "/"以外はnew_tokensに追加
        else:
            new_tokens.append(tokens[index])
        index += 1
    return new_tokens


def evaluate(tokens):
    answer = 0
    # 負の数の入力を許容
    if tokens[0] == {"type": "MINUS"}:
        tokens.insert(0, {"type": "NUMBER", "number": 0})  # Insert a dummy '0' token
    tokens.insert(0, {"type": "PLUS"})  # Insert a dummy '+' token
    tokens = update_multiply_divide_first(tokens)
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
    test("1 + 1*4")
    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
