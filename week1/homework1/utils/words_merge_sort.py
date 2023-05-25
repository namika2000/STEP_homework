from collections import deque

def words_merge_sort(A: str) -> list[str]:
  
  """単語を昇順にソートする.
  
  Args:
      A (str): ソート前の文字列

  Returns:
      list[str]: Aを昇順にソートした文字列
  """
  N = len(A)
  X =  N // 2
  L = A[:X]
  R = A[X:]

  if len(L) >= 2: L = words_merge_sort(L)
  if len(R) >= 2: R = words_merge_sort(R)

  d = deque()
  for l in L: d.append(l)
  for r in reversed(R): d.append(r)

  B = []
  while len(d):
    first: str = d[0]
    last: str = d[-1]
    if ord(first) <= ord(last):
      B.append(d.popleft())
    else:
      B.append(d.pop())
  return B