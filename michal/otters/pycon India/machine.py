# david beazley pycon india 2019
# https://www.youtube.com/watch?v=VUT386_GKI8&feature=youtu.be
import struct

class Machine:
    def __init__(self, memsize = 65536):
        self.items = []
        self.memory = bytearray(memsize)

    def load(self, addr):
        return struct.unpack('<d', self.memory[addr:addr+8])[0]

    def store(self, addr, val):
        self.memory[addr:addr+8] = struct.pack('<d', val)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def execute(self, instructions):
        for op, *args in instructions:
            print(op, args, self.items)
            if op == 'const':
                self.push(args[0])
            elif op == 'add':
                right = self.pop()
                left = self.pop()
                self.push(left+right)
            elif op == 'mul':
                right = self.pop()
                left = self.pop()
                self.push(left*right)
            elif op == 'load':
                addr = self.pop()
                self.push(self.load(addr))
            elif op == 'store':
                val = self.pop()
                addr = self.pop()
                self.store(addr, val)
            else:
                raise RuntimeError(f'Bad op{op}')
def example():
    # compute 2+3*0.1

    
#    code = [
#        ('const', 2),
#        ('const', 3),
#        ('const', 0.1),
#        ('mul',),
#        ('add',),
#        ]
#    m = Machine()
#    m.execute(code)
#    print('Result', m.pop())

# after adding memory functionality work with variables is possible:

# x = 2
# v = 3
# x = x + v *0.1

    x_addr = 22
    v_addr = 42
    
    code = [
        ('const', x_addr),
        ('const', x_addr),
        ('load',),
        ('const', v_addr),
        ('load',),
        ('const', 0.1),
        ('mul',),
        ('add',),
        ('store',),
        ]

    m = Machine()
    m.store(x_addr, 2.0)
    m.store(v_addr, 3.0)
    m.execute(code)
    print('Result', m.load(x_addr))

if __name__ == '__main__':
    example()
