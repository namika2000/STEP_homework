def count_char(word: str) -> list[int]:
  """
  
  単語に含まれる文字の種類と個数をリストで返す
  
  Args: 
      word (str): 単語を表す文字列
      
  Returns:
      list[int]: 文字の種類と個数を表すリスト(list[0]が'a'、list[25]が'z'の個数)
  """
  alphabets = [0] * 26
  for char in word:
    alphabets[ord(char) - ord('a')] += 1

  return alphabets