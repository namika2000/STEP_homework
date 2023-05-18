from utils.count_char import count_char

def add_dict_char_list(sorted_dict_by_score: list[str, int]) -> list[int, str, int]:
  """
  スコアで降順にソートされた辞書を受け取り、各単語内の単語内の文字の種類と個数の情報を付与して返す
  
  Args:
      sorted_dict_by_score (list[str, int]): スコアで降順にソートされた辞書を表す配列。要素は [単語, スコア]

  Returns:
      list[int, str, int]: 要素は [[単語内の文字の個数を表す配列], 単語, スコア]
  """
  new_dict: list[int, str, int] = []
  for word in sorted_dict_by_score:
    new_word: list[int, str, int] = [count_char(word[0]),word[0], word[1]]  #[単語内の各文字の個数, 単語, スコア]
    new_dict.append(new_word)
    
  return new_dict