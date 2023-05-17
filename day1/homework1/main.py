from utils.binary_search import binary_search
from utils.dict_merge_sort import dict_merge_sort
from utils.words_merge_sort import words_merge_sort

def main(random_word: str, dictionary: list[str]) -> None:
  sorted_random_word: str = words_merge_sort(random_word)
  new_dict: list[str] = []
  for word in dictionary:
    sorted_word: str = words_merge_sort(word)
    new_dict.append([sorted_word, word])
  sorted_dict: list[str] = dict_merge_sort(new_dict)
  
  ans: list[str] = binary_search(sorted_dict, sorted_random_word)
  
  print(ans)

dictionary = ['orange', 'apple', 'peach', 'watermelon', 'alppe', 'appel', 'a', 'app', 'apply']
random_word = ''

main(random_word, dictionary)
