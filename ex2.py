class Person(object):
    def __init__(self, first, last, age):
        self.firstname = first
        self.lastname = last
        self.age = age

    def __str__(self):
        return self.firstname + " " + self.lastname + ', ' + str(self.age)


class Employee(Person):
    def __init__(self, first, last, age, staffnum):
        super(Employee, self).__init__(first, last, age)
        self.staffnumber = staffnum

    def __str__(self):
        return super(Employee, self).__str__() + ', ' + self.staffnumber


x = Person("Marge", "Simpson", 28)
y = Employee("Homer", "Simpson", 28, "1007")

print(x)
print(y)
