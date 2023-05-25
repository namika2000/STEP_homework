def read_file(file_path: str) -> list[str]:
  """
  ファイルを読み取って、データを配列として返す
  
  Args:
    file_path (str): ファイルパスを表す文字列

  Returns:
      list[str]: データを表す文字列配列
  """
  with open(file_path, 'r') as f:
    data: list[str] = f.read().split("\n")
  return data