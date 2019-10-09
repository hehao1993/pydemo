import pickle


class Test:
    def run(self):
        print('test.run')


# print(pickle.dumps(Test))

getattr(pickle.loads(b'\x80\x03c__main__\nTest\nq\x00.')(), 'run')()
