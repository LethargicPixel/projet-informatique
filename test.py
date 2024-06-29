class A:
    def __init__(self) -> None:
        self.c=1
        
    def a(self):
        def b(self):
            return self.c
        return b(self)
a=A()

print(a.a())
