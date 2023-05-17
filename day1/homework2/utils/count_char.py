def count_char(word: str) -> list[int]:
  alphabet = [0] * 26
  for char in word:
    alphabet[ord(char) - ord('a')] += 1

  return alphabet