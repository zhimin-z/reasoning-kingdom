# 第四部分：Python进阶——面向对象与函数式编程

## 词条9：面向对象编程高级特性

### 官方解释
**面向对象编程**（OOP）不仅包括基本的类、对象、继承，还有更多高级特性：多重继承、抽象类、接口、属性装饰器、类方法、静态方法、魔术方法等。

Python OOP特性：
- 多重继承：一个类可以继承多个父类
- 抽象基类（ABC）：定义接口，不能实例化
- 属性装饰器：@property, @setter, @deleter
- 类方法和静态方法：@classmethod, @staticmethod
- 魔术方法：`__init__`, `__str__`, `__len__`等

### 兔狲老师解释
OOP高级特性让代码更灵活、更安全、更易维护。

小小猪的比喻：
- 多重继承：像混血儿，继承父母双方特征
- 抽象类：像设计规范，规定必须实现的方法
- 属性装饰器：像智能门卫，控制对属性的访问
- 魔术方法：像魔法咒语，让对象有特殊行为

设计原则：
- 单一职责原则：一个类只做一件事
- 开放封闭原则：对扩展开放，对修改封闭
- 里氏替换原则：子类可以替换父类
- 接口隔离原则：接口要小而专
- 依赖倒置原则：依赖抽象，不依赖具体

### 思考题17：动手题
问题：实现OOP高级特性示例：

```python
# 1. 多重继承
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "..."

class Mammal(Animal):
    def give_birth(self):
        return f"{self.name} gives birth to live young"

class Bird(Animal):
    def lay_eggs(self):
        return f"{self.name} lays eggs"

class Platypus(Mammal, Bird):
    """鸭嘴兽：既是哺乳动物又是卵生"""
    def speak(self):
        return "Quack?"

# 2. 抽象基类
from abc import ABC, abstractmethod

class Shape(ABC):
    """形状抽象基类"""
    
    @abstractmethod
    def area(self):
        """计算面积"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """计算周长"""
        pass
    
    def describe(self):
        """通用描述方法"""
        return f"这是一个形状，面积={self.area():.2f}，周长={self.perimeter():.2f}"

class Circle(Shape):
    """圆形"""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    """矩形"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# 3. 属性装饰器
class BankAccount:
    """银行账户"""
    
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self._balance = initial_balance  # 私有属性
    
    @property
    def balance(self):
        """获取余额"""
        return self._balance
    
    @balance.setter
    def balance(self, amount):
        """设置余额（有验证）"""
        if amount < 0:
            raise ValueError("余额不能为负数")
        self._balance = amount
    
    @balance.deleter
    def balance(self):
        """删除余额（实际是重置）"""
        print(f"警告：正在重置{self.owner}的余额")
        self._balance = 0
    
    def deposit(self, amount):
        """存款"""
        if amount <= 0:
            raise ValueError("存款金额必须为正数")
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        """取款"""
        if amount <= 0:
            raise ValueError("取款金额必须为正数")
        if amount > self.balance:
            raise ValueError("余额不足")
        self.balance -= amount
        return self.balance

# 4. 类方法和静态方法
class Date:
    """日期类"""
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"
    
    @classmethod
    def from_string(cls, date_string):
        """从字符串创建日期对象（类方法）"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @staticmethod
    def is_leap_year(year):
        """判断是否为闰年（静态方法）"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    @property
    def is_leap(self):
        """判断当前年份是否为闰年（属性）"""
        return self.is_leap_year(self.year)

# 测试多重继承
print("多重继承测试：")
perry = Platypus("Perry the Platypus")
print(f"名字: {perry.name}")
print(f"叫声: {perry.speak()}")
print(f"繁殖方式1: {perry.give_birth()}")
print(f"繁殖方式2: {perry.lay_eggs()}")

print("\n" + "="*50)

# 测试抽象基类
print("抽象基类测试：")
circle = Circle(5)
rectangle = Rectangle(4, 6)

print(f"圆形: {circle.describe()}")
print(f"矩形: {rectangle.describe()}")

print("\n" + "="*50)

# 测试属性装饰器
print("属性装饰器测试：")
account = BankAccount("小小猪", 1000)
print(f"账户所有者: {account.owner}")
print(f"初始余额: {account.balance}")

account.deposit(500)
print(f"存款500后余额: {account.balance}")

account.withdraw(300)
print(f"取款300后余额: {account.balance}")

try:
    account.withdraw(2000)
except ValueError as e:
    print(f"取款失败: {e}")

print("\n" + "="*50)

# 测试类方法和静态方法
print("类方法和静态方法测试：")
date1 = Date(2023, 12, 25)
date2 = Date.from_string("2024-02-29")

print(f"日期1: {date1}")
print(f"日期2: {date2}")
print(f"2023是闰年吗？{Date.is_leap_year(2023)}")
print(f"2024是闰年吗？{Date.is_leap_year(2024)}")
print(f"日期2的年份是闰年吗？{date2.is_leap}")
```

### 思考题18：动脑题
问题：面向对象设计原则在实际编程中如何应用？

思考方向：
- 如何判断一个类是否违反了单一职责原则？
- 在什么情况下应该使用组合而不是继承？
- 接口隔离原则如何提高代码的可维护性？
- 依赖注入是什么？如何实现？
- 设计模式（工厂、观察者、策略等）如何体现设计原则？

---

## 词条10：函数式编程与Pythonic代码

### 官方解释
**函数式编程**（Functional Programming）是一种编程范式，强调纯函数、不可变数据、高阶函数、函数组合。Python虽然不是纯函数式语言，但支持许多函数式特性。

Python函数式特性：
- 高阶函数：函数可以作为参数或返回值
- 匿名函数：lambda表达式
- 内置高阶函数：map, filter, reduce
- 列表推导式、字典推导式、集合推导式
- 生成器：惰性求值，节省内存

Pythonic代码：
- 简洁、清晰、易读
- 利用Python特有语法和特性
- 符合"Python之禅"（import this）

### 兔狲老师解释
函数式编程让代码更简洁、更可预测、更易测试。

小小猪的比喻：
- 纯函数：像数学函数，相同输入总是相同输出
- 高阶函数：像函数工厂，生产或消费函数
- 生成器：像流水线，需要时才生产数据
- 装饰器：像包装纸，给函数添加功能

Pythonic哲学：
- 优美胜于丑陋
- 明了胜于晦涩
- 简洁胜于复杂
- 可读性很重要

### 思考题19：动手题
问题：实践函数式编程和Pythonic代码：

```python
# 1. 高阶函数和lambda
def apply_operation(numbers, operation):
    """应用操作到每个数字（高阶函数）"""
    return [operation(n) for n in numbers]

# 使用lambda定义简单操作
numbers = [1, 2, 3, 4, 5]
print("原始数字:", numbers)

double = lambda x: x * 2
square = lambda x: x ** 2
increment = lambda x: x + 1

print("加倍:", apply_operation(numbers, double))
print("平方:", apply_operation(numbers, square))
print("加1:", apply_operation(numbers, increment))

# 2. 内置高阶函数
print("\n内置高阶函数：")
print("map加倍:", list(map(double, numbers)))
print("filter偶数:", list(filter(lambda x: x % 2 == 0, numbers)))

from functools import reduce
print("reduce求和:", reduce(lambda x, y: x + y, numbers))
print("reduce求积:", reduce(lambda x, y: x * y, numbers))

# 3. 列表推导式 vs 传统循环
print("\n列表推导式 vs 传统循环：")

# 传统方式
squares_old = []
for n in numbers:
    squares_old.append(n ** 2)

# Pythonic方式
squares_new = [n ** 2 for n in numbers]

print("传统方式:", squares_old)
print("Pythonic方式:", squares_new)

# 带条件的列表推导式
even_squares = [n ** 2 for n in numbers if n % 2 == 0]
print("偶数的平方:", even_squares)

# 4. 字典推导式和集合推导式
print("\n字典推导式和集合推导式：")

# 字典推导式
square_dict = {n: n ** 2 for n in numbers}
print("数字平方字典:", square_dict)

# 集合推导式（自动去重）
numbers_with_duplicates = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {n ** 2 for n in numbers_with_duplicates}
print("唯一平方集合:", unique_squares)

# 5. 生成器
print("\n生成器：")

def fibonacci_generator(n):
    """生成斐波那契数列的生成器"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

print("斐波那契数列（前10个）:")
for num in fibonacci_generator(10):
    print(num, end=" ")

print("\n\n生成器表达式:")
# 生成器表达式（惰性求值）
big_numbers = (x ** 2 for x in range(1000000) if x % 100000 == 0)
print("大数字生成器（前5个）:")
for i, num in enumerate(big_numbers):
    if i >= 5:
        break
    print(num, end=" ")

# 6. 装饰器
print("\n\n装饰器：")

def timer_decorator(func):
    """计时装饰器"""
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.6f}秒")
        return result
    
    return wrapper

def cache_decorator(func):
    """缓存装饰器（记忆化）"""
    cache = {}
    
    def wrapper(*args):
        if args in cache:
            print(f"从缓存获取 {func.__name__}{args}")
            return cache[args]
        result = func(*args)
        cache[args] = result
        print(f"计算并缓存 {func.__name__}{args} = {result}")
        return result
    
    return wrapper

@timer_decorator
@cache_decorator
def slow_fibonacci(n):
    """慢速斐波那契计算（用于演示）"""
    if n <= 1:
        return n
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)

print("\n带装饰器的斐波那契计算:")
print(f"F(5) = {slow_fibonacci(5)}")
print(f"F(5) = {slow_fibonacci(5)}")  # 第二次应该从缓存获取
print(f"F(6) = {slow_fibonacci(6)}")
```

### 思考题20：动脑题
问题：函数式编程和面向对象编程如何结合使用？

思考方向：
- 在什么场景下函数式编程更有优势？
- 如何用函数式思想改进面向对象代码？
- Python的装饰器如何体现函数式特性？
- 不可变数据在并发编程中有什么优势？
- 如何平衡Pythonic代码和性能优化？

---

## 兔狲学院Python小结

### 学习收获
通过本章学习，你掌握了：

1. **Python基础语法**：
   - 变量、数据类型、运算符
   - 控制结构、函数、模块化编程

2. **四种基础数据结构**：
   - **哈希表（字典）**：快速查找的魔法
   - **链表**：灵活的动态序列
   - **树**：层次化数据结构
   - **图**：复杂关系的网络

3. **算法思维**：
   - 排序与搜索算法
   - 动态规划与贪心算法
   - 时间复杂度与空间复杂度分析

4. **Python进阶**：
   - 面向对象编程高级特性
   - 函数式编程与Pythonic代码
   - 设计原则与最佳实践

### 兔狲教授的最后一课
"亲爱的未来推理科学家：

编程不是关于记忆语法，而是关于表达思想；不是关于控制计算机，而是关于解决问题。

Python就像一支好用的笔，数据结构就像不同的纸张，算法就像写作技巧。好的程序员不是记住所有语法，而是知道如何选择合适的工具解决问题。

记住：
1. **代码是写给人看的**，只是恰好能被计算机执行
2. **清晰的思维产生清晰的代码**，清晰的代码解决复杂的问题
3. **数据结构是算法的基石**，选择合适的数据结构事半功倍
4. **算法是解决问题的艺术**，理解原理比记住实现更重要
5. **编程是终身学习**，保持好奇，持续实践

现在，你拥有了从基础语法到数据结构的完整工具箱。但工具的价值在于使用。用这些工具去实现你的想法，解决真实的问题，创造有用的程序。

推理的民主化不是让每个人成为专家，而是让每个人都能使用这些强大的思维工具。Python降低了编程的门槛，让你能专注于思考而不是语法。

现在，轮到你去探索、去创造、去推理了。

兔狲教授在黑石屋的书房里，泡好茶，运行着Python解释器，等着看你的代码。"

---

## 兔狲学院四章总结

经过四章的学习，你已经掌握了从中学到大学过渡的完整知识体系：

1. **微积分**：理解变化与累积的语言
2. **线性代数**：处理多维数据的工具  
3. **西方近代以前哲学**：理性思维的基础训练
4. **Python编程与数据结构**：计算思维的实践工具

这些知识不是孤立的学科，而是相互关联的思维框架：
- 用微积分理解变化，用线性代数处理结构
- 用哲学追问根本，用编程实现想法
- 用数据结构组织信息，用算法解决问题

**致未来的推理科学家**：
你现在拥有了探索知识世界的基本工具。但记住，工具的价值在于使用。真正的学习发生在实践中，在解决问题中，在创造价值中。

推理的民主化意味着每个人都应该有机会掌握这些强大的思维工具。现在，这个机会在你手中。

去探索吧，去创造吧，去推理吧。世界需要更多像你一样的思考者。

