class A:
    def __enter__(self):
        print("OPEN")
        return self
    def __exit__(self, *args, **kwargs):
        print("CLOSE")
with A() as a:
    print(type(a))
with a:
    print(type(a))