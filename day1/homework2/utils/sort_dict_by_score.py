


from utils.calculate_score import calculate_score
from utils.count_char import count_char
from utils.merge_sort_dict_by_score import merge_sort_dict_by_score

def sort_dict_by_score(dictionary: list[str]) -> list[int, str, int]:
  new_dict: list[str, int] = []
  for word in dictionary:
    score: int = calculate_score(word)
    new_dict.append([word, score])
    
  sorted_dict_by_score: list[str, int] = merge_sort_dict_by_score(new_dict)
  
  #単語内の各文字の個数の情報を付与
  new_dict: list[int, str, int] = []
  for word in sorted_dict_by_score:
    new_word: list[int, str, int] = [count_char(word[0]),word[0], word[1]] #[単語内の各文字の個数, 単語, スコア]
    new_dict.append(new_word)
    
  return new_dict