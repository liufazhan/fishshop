from werkzeug.local import LocalStack

# 理解local中pop top push方法

s=LocalStack()
s.push(1)
print(s.top)
print(s.top)
# pop为方法，弹出栈顶的元素
print(s.pop())
# top为属性
print(s.top)

# 栈 栈的特点是先进后出，后进先出
s.push(1)
s.push(2)
print(s.top)
print(s.top)
print(s.pop())
print(s.top)

# 数据结构限制了某些能力