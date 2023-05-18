def binary_search(A: list[str], sorted_word: str) -> list[str]:
  """
  二分探索でAの中からsorted_wordと等しいものを見つける
  
  Args:
      A (list[str]): [[ソート後の単語, ソート前の単語],]
      
      sorted_word (str): Aの中から探索する文字列
  
  Returns:
      list[str]: sorted_wordのanagramを[[ソート後の単語, ソート前の単語],]として返す
  """
  ans = []
  N = len(A)
  X = N // 2

  mid: str = A[X][0]
  if sorted_word == '':
    return
  
  if sorted_word == mid:
    tmp = X
    while True:
      if X > N - 1:
        break
      else:
        if A[X][0] != sorted_word:
          break
        else:
          ans.append(A[X][1])
          X += 1
          
    X = tmp - 1
    while True:
      if X < 0:
        break
      else:
        if A[X][0] != sorted_word:
          break
        else:
          ans.append(A[X][1])
          X -= 1
      
    return ans
  
  else:
    len_sorted_word: int = len(sorted_word)
    len_mid: int = len(mid)
    for i in range(min(len_sorted_word, len_mid)):
      if ord(sorted_word[i]) < ord(mid[i]):
        A = A[:X]
        return binary_search(A, sorted_word)
      else:
        A = A[X:]
        return binary_search(A, sorted_word)
    if len_sorted_word < len_mid:
      A = A[:X]
      return binary_search(A, sorted_word)
    else:
      A = A[X:]
      return binary_search(A, sorted_word)