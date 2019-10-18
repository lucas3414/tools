# 设置装饰器开关
# switch = True 打开装饰器，执行更新后功能  switch = False 关闭装饰器，执行原来的功能
switch = True


# 这个用例装饰类的 装饰器
def initClassDoSomeThings(switch):
    def wrapper(cls):
        def inner(*args, **kwargs):
            if switch:
                print("我是一个类装饰器，实例化前")
                ret = cls(*args, **kwargs)
                print("我是一个类装饰器，实例化后")
            else:
                ret = cls(*args, **kwargs)

            return ret

        return inner
    return wrapper


# 这个类 是用来装饰 其他类中的 方法的
class FuncWrapper:
    @staticmethod
    def InitFuncDoSomeThings(switch):
        def wrapper(func):
            def inner(*args, **kwargs):
                if switch:
                    print("我是一个类方法装饰器，装饰类的方法，方法执行前")
                    ret = func(*args, **kwargs)
                    print("我是一个类方法装饰器，装饰类的方法，方法执行后")
                else:
                    ret = func(*args, **kwargs)
                return ret

            return inner

        return wrapper


@initClassDoSomeThings(switch)
class Person(object):
    def __init__(self):
        print("我是__init__方法")

    @staticmethod
    @FuncWrapper.InitFuncDoSomeThings(switch)
    def func():
        print("我是一个被装饰的方法")


Person().func()
