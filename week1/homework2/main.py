from utils.calculate_score import calculate_score
from utils.merge_sort_dict_by_score import merge_sort_dict_by_score
from utils.count_char import count_char
from utils.is_anagram import is_anagram
from utils.add_dict_char_list import add_dict_char_list
from utils.read_file import read_file

##CONST##
##DICTIONARY###########
DICTIONARY = read_file("in/words.txt")
#######################

##input_file###########
INPUT_FILE = ["in/small.txt", "in/medium.txt", "in/large.txt"]
#######################

##output_file##########
OUTPUT_FILE = ["out/answer_file_small.txt", "out/answer_file_medium.txt",  "out/answer_file_large.txt", ]
########################
########
  
def main(in_path: str, out_path: str) -> None:
  word_list = read_file(in_path)
  
  new_dict: list[str, int] = []
  for word in DICTIONARY:
    score: int = calculate_score(word)
    new_dict.append([word, score])
    
  sorted_dict_by_score: list[str, int] = merge_sort_dict_by_score(new_dict)
  sorted_dict = add_dict_char_list(sorted_dict_by_score)
      
  anagrams = []
  for random_word in word_list:
    char_list: list[int] = count_char(random_word)
    for word in sorted_dict:
      if is_anagram(char_list, word[0]):
        best_anagram: list[str, int] = word[1:]
        anagrams.append(best_anagram)
        break

  with open(out_path, 'w') as f:
    for anagram in anagrams:
        word: str = anagram[0]
        f.write("%s\n" % word)
        
if __name__ == "__main__":
  for i in range(len(INPUT_FILE)):
    main(INPUT_FILE[i], OUTPUT_FILE[i])