from utils.count_char import count_char
from utils.is_anagram import is_anagram
from utils.sort_dict_by_score import sort_dict_by_score
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
  sorted_dict = sort_dict_by_score(DICTIONARY)
      
  anagrams = []
  for random_word in word_list:
    char_list: list[int] = count_char(random_word)
    for word in sorted_dict:
      if is_anagram(char_list, word[0]):
        best_anagram: list[str, int] = word[1:]
        anagrams.append(best_anagram)
        break

  overall_score = 0
  with open(out_path, 'w') as f:
    for anagram in anagrams:
        word: str = anagram[0]
        score: int = anagram[1]
        f.write("%s\n" % word)
        overall_score += score

  # print('-------', overall_score)
        
for i in range(len(INPUT_FILE)):
  main(INPUT_FILE[i], OUTPUT_FILE[i])