import threading,time
from werkzeug.local import Local
# 线程隔离
# 原理：使用字典保存数据
# 操作数据
# werkzuge 的local方法 local字典
# LocalStack Local 字典 是一种怎样的关系
# local使用字典的方式实现线程的隔离
# LocalStack封装了local对象，把local对象作为自己的私有属性，实现线程隔离的栈结构
# 封装 如果一次封装解决不了问题，那么就在封装一次

# {thread_id1:value,thread_id2:value.....}
# L是线程隔离的对象
# t1 L.a t2 L.a 也是线程隔离的

class A:
    a=1


my_obj= Local()
#my_obj= A()
my_obj.a=1


def worker():
    my_obj.a=2
    print('Is a new thread is:'+str(my_obj.a))


new_t=threading.Thread(target=worker, name='八月-thread')
new_t.start()

# 主线程
time.sleep(1)
print('Is main thread is:', str(my_obj.a))
