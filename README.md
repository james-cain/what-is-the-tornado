# python-learning
A server based on tonardo。

## RequestHandler

1. 接入点 函数：需要子类继承并定义具体行为的函数在RequestHandler中被称为接入点函数（Entry Point）
   1. get()
   2. initialize()：可以为该函数传递参数，参数来源于配置URL映射时的定义

