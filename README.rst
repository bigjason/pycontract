============================
Python Data Contracts
============================
A declarative data contract container type for Python
------------------------------------------------------

Python data contracts (pycontracts in PyPi) is a  library for exchanging data between
systems.  It is losesly based on the django forms api to help ease adoption. A simple example::

    from pycontract import DataContract, StringField, NumberField
    
    class Person(DataContract):
        name = StringField()
        phone = StringField(null=True)
        age = NumberField(null=True)
        
    bob = Person()
    bob["name"] = "Bob Smith"
    bob["phone"] = "999-555-1234"
    bob["age"] = 32
    
In this example the contract for person is declared and the record for bob is instantiated.  In 
addition to the basic data we can add ``processors`` which manipulate or clean the data as well 
as ``validators`` which validate the data similar to django validators.

Features
--------
* Customizable validation (compatible with django validators).
* Data processors to clean up and format data.
* Declarative field definitions.
* Enforced value assignment helps avoid regression errors.
* Licensed under the MIT License to be business friendly. (License decision is pending)