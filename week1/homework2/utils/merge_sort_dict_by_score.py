from collections import deque

def merge_sort_dict_by_score(A: list[str, int]) -> list[str, int]:
  """複数の単語が入った二次元配列をスコアで降順にソートする
  
  Args:
      A (list[str, int]): [[ソート前の辞書の単語, スコア]]

  Returns:
      list[str, int]: Aをスコアで降順にソートした二次元配列
  """
  N = len(A)
  X =  N // 2
  L = A[:X]
  R = A[X:]

  if len(L) >= 2: L = merge_sort_dict_by_score(L)
  if len(R) >= 2: R = merge_sort_dict_by_score(R)

  d = deque()
  for l in L: d.append(l)
  for r in reversed(R): d.append(r)

  B: list[str, int] = []
  while len(d):
    #単語同士を前から順に１文字ずつ比べる
    first: str = d[0][1]
    last: str = d[-1][1]
    
    if first >= last:
      B.append(d.popleft())
    else:
      B.append(d.pop())

  return B
