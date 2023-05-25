def is_anagram(char_list: list[int], word: list[int]) -> bool:
  """
  与えられた単語と辞書の単語がanagramかを判定し、真偽値を返す.
  
  Args: 
      char_list (list[int]): 与えられた単語に含まれる文字の種類と個数を表す整数リスト
      word (list[int]): 辞書の単語に含まれる文字の種類と個数を表す整数リスト

  Returns:
      bool: anagramならTrue,そうでないならFalse
  """
  if word == [0] * 26:
    return False
  else:
    new_list: list[int] = []
    for i in range(len(char_list)):
      new_list.append(char_list[i] - word[i])

    for num in new_list:
      if num < 0:
        return False
    return True