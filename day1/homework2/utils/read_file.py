def read_file(file_path: str) -> list[str]:
  with open(file_path, 'r') as f:
    data: list[str] = f.read().split("\n")
  return data