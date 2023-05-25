from collections import deque

def dict_merge_sort(A: list[str]) -> list[str]:
  """複数の単語が入った二次元配列を昇順にソートする
  
  Args:
      A (list[str]): [[ソート済の辞書の単語, ソート前の辞書の単語]]

  Returns:
      list[str]: Aを一番目の要素で昇順にソートした二次元配列
  """
  N = len(A)
  X =  N // 2
  L = A[:X]
  R = A[X:]

  if len(L) >= 2: L = dict_merge_sort(L)
  if len(R) >= 2: R = dict_merge_sort(R)

  d = deque()
  for l in L: d.append(l)
  for r in reversed(R): d.append(r)

  B = []
  while len(d):
    #単語同士を前から順に１文字ずつ比べる
    first: str = d[0][0]
    last: str = d[-1][0]

    len_first = len(first)
    len_last = len(last)
    flag = True
    for i in range(min(len_first, len_last)):
      if ord(first[i]) < ord(last[i]):
        flag = False
        B.append(d.popleft())
        break
      elif ord(first[i]) > ord(last[i]):
        flag = False
        B.append(d.pop())
        break
    if flag:  
      if len_first <= len_last:
        B.append(d.popleft())
      else:
        B.append(d.pop())
  return B
