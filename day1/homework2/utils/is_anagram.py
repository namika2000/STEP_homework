def is_anagram(char_list: list[int], word: list[int]) -> bool:
  if word == [0] * 26:
    return False
  else:
    new_list: list[int] = []
    for i in range(len(char_list)):
      new_list.append(char_list[i] - word[i])
      
    # new_list: list[int] = [x - y for (x, y) in zip(char_list, word)]
    for num in new_list:
      if num < 0:
        return False
    return True

#''でもTrueになってしまっているものがある