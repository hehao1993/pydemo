class Parent:
    def __init__(self):
        self.prop = 'prop'

    def go(self):
        print('parent do')


class Child(Parent):
    def run(self):
        print(self.prop)


# Child().run()
# Child().go()

# print(None is False)
