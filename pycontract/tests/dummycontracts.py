from pycontract import *
import datetime

class Person(DataContract):

    name = StringField(1, label="person Name", null=False)
    phone = NumberField(2)

class Employee(Person):

    employeeid = NumberField(1)
    department = StringField(4)
    hire_date = DateTimeField(default=lambda: datetime.datetime.now())

    field_overrides = {
        "name": dict(order=2, default=lambda: "Name For {0}".format(datetime.date.today())),
        "phone": dict(order=3)
    }


e = Employee(phone="asd", employeeid="2asd", department="Our dept")

print e.is_valid()
print e.name
print e.hire_date
print e._errors
