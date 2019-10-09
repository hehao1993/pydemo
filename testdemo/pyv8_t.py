"""
Python3 安装不要使用pip，因为官方只支持 Python2，需要在这里下载对应系统的二进制文件：emmetio/pyv8-binaries
然后解压后将 PyV8.py 与 _PyV8.so (如so不是这个名字需要改成这样) 两文件复制到 Python 的 site-packages 目录下
"""
import PyV8


# with PyV8.JSContext() as ctx:
#     ctx.eval("""
#         function add(x, y) {
#             return x + y;
#         }
#     """)
#     print(ctx.locals.add(1, 2))
#

# with open('m.js', 'rb+') as f:
#     js = f.read()
#
# with PyV8.JSContext() as ctx:
#     ctx.eval(js)
#     print(ctx.locals.md5(''.join(['1555656067', 'xianyin', 'test123456'])))

# # PyV8执行步骤
# with PyV8.JSLocker():
#     ctxt = PyV8.JSContext()
#     ctxt.enter()
#     ctxt.eval(js)
#     a = ctxt.locals.md5(''.join(['1555656067', 'xianyin', 'test123456']))
#     ctxt.leave()
# print(a)
