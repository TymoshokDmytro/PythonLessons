
class Stack:

    def __init__(self):
        self._elements = []

    def push(self, obj):
        self._elements.append(obj)

    def pop(self):
        if len(self._elements) == 0:
            raise IndexError('The stack is empty')
        return self._elements.pop()

    def top(self):
        if len(self._elements) == 0:
            raise IndexError('The stack is empty')
        return self._elements[self.get_size()-1]

    def get_size(self):
        return len(self._elements)

    def __str__(self):
        return 'Stack: ' + str(self._elements)


stack = Stack()
stack.push(1)
stack.push('1')
print('top=', stack.top(), 'type=', type(stack.top()))
stack.push(2)
print(stack)

print(stack.pop())
print(stack)
print(stack.pop())
print(stack)
print(stack.pop())
print(stack)
print(stack.pop())
print(stack)
