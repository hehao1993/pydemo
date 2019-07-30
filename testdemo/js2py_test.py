import js2py
with open('m.js', 'rb+') as f:
    js = f.read()

context = js2py.EvalJs()
context.execute(js.decode())
num = '12345'
context.execute(f"r = vues('{num}')")
r = context.r
print(r)