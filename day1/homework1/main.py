import sys
sys.path.append('../')
from homework2.utils.read_file import read_file
from utils.binary_search import binary_search
from utils.dict_merge_sort import dict_merge_sort
from utils.words_merge_sort import words_merge_sort

##CONST##
##DICTIONARY###########
DICTIONARY = read_file("words.txt")
#######################

def main(random_word: str) -> None:
  if random_word == '':
    print('文字列を入力してください')
    return
  sorted_random_word: str = words_merge_sort(random_word)
  new_dict: list[str] = []
  for word in DICTIONARY:
    sorted_word: str = words_merge_sort(word)
    new_dict.append([sorted_word, word])
  sorted_dict: list[str] = dict_merge_sort(new_dict)
  
  ans: list[str] = binary_search(sorted_dict, sorted_random_word)
  
  if ans is None:
    print('anagramが見つかりません')
    return
  
  print(f'{random_word}のanagramは{ans}です')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s data_file" % sys.argv[0])
        exit(1)
    print('---', sys.argv[1])
    main(sys.argv[1])


