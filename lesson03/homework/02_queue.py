
class Stack:

    def __init__(self):
        self._elements = []

    def push(self, obj):
        self._elements.append(obj)

    def pop(self):
        if len(self._elements) == 0:
            raise IndexError('The stack is empty')
        first = self._elements[0]
        self._elements = self._elements[1:]
        return first

    def top(self):
        if len(self._elements) == 0:
            raise IndexError('The stack is empty')
        return self._elements[0]

    def get_size(self):
        return len(self._elements)

    def __str__(self):
        return 'Queue: ' + str(self._elements)


stack = Stack()
stack.push(1)
stack.push('str')
print('top=', stack.top(), 'type=', type(stack.top()))
stack.push(2)
print(stack)

print(stack.pop())
print(stack)
print(stack.pop())
print(stack)
print(stack.pop())
print(stack)
