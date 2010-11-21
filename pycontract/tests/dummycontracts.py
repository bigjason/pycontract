from pycontract import *
import datetime

class Person(DataContract):

    name = StringField(1, label="person Name")
    phone = NumberField(2)

class Employee(Person):

    employeeid = NumberField(1)
    department = StringField(4)
    hire_date = DateTimeField(default=lambda: datetime.datetime.now())

    field_overrides = {
        "name": dict(order=2),
        "phone": dict(order=3)
    }

