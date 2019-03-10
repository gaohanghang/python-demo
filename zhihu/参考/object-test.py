class Dog():
    '''一次模拟小狗的简单测试'''

    def __init__(self,name,age):
        self.name = name
        self.age = age

my_dog = Dog('Lucy',3)

print("My dog's name is " + my_dog.name +".")
print("My dog is " + str(my_dog.age) +" years old.")