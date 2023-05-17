def binary_search(A: list[str], sorted_word: str) -> list[str]:
  ans = []
  N = len(A)
  X = N // 2
  
  mid: str = A[X][0]
  if sorted_word == '':
    return ans
  
  elif sorted_word == mid:
    tmp = X
    while mid == A[X][0]:
      ans.append(A[X][1])
      X += 1
    X = tmp - 1
    while mid == A[X][0]:
      ans.append(A[X][1])
      X -= 1
      
    return ans
  
  else:
    for i in range(min(len(sorted_word), len(mid))):
      if ord(sorted_word[i]) < ord(mid[i]):
        A = A[:X+1]
        binary_search(A, X+1, sorted_word)
      elif ord(sorted_word[i]) > ord(mid[i]):
        A = A[X+1:]
        binary_search(A, N-X-1, sorted_word)