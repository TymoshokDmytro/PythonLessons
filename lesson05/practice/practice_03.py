class file_context_manager:

    def __init__(self, filename, mode):
        self._filename = filename
        self._mode = mode
        self._file = None

    def __enter__(self):
        self._file = open(self._filename, self._mode)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        self._file = None


with file_context_manager('test_file.txt', 'w') as file:
    file.writelines("""Hello
here are some 
lines of text""")

with file_context_manager('test_file.txt', 'r') as file:
    lines = file.readlines()
    lines = [line.replace('\n', "") for line in lines]
    print(lines)

