##SCORE###########
SCORES: list[int] = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
##################

def calculate_score(word :str) -> int:
  score = 0
  for char in word:
    score += SCORES[ord(char) - ord('a')]
  return score