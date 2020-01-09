from werkzeug.local import LocalStack
import threading,time

# 验证LocalStack栈隔离的特性

my_stack=LocalStack()
# 将1推入栈中
my_stack.push(1)
print('After push the value,the stack top value is:'+str(my_stack.top))


def worker():
    print('Before push value the stack value is :'+str(my_stack.top))
    my_stack.push(2)
    print('After push new value, the new stack top value is: '+str(my_stack.top))


new_stack=threading.Thread(target=worker,name='qiyue-thread')
new_stack.start()

time.sleep(1)
#主线程
print('Finally, the main stack top value is :'+str(my_stack.top))

#使用线程隔离的意义在于：使当前线程能够正确引用到他自己创建的对象，而不是引用其他线程所创建的对象
