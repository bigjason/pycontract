============================
Python Data Contracts
============================
A declarative data contract container type for Python
------------------------------------------------------

*Pycontracts is currently an internal beta and not ready for production use yet.*


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

--------
Features
--------
* Customizable validation (compatible with django validators).
* Data processors to clean up and format data.
* Declarative field definitions.
* Enforced value assignment helps avoid regression errors.
* Licensed under the `MIT License`_.

Basic Usage
-----------
The first step is define a basic contract.  This is done by inheriting from ``pycontract.DataContract``.  Next
we decide if there is standard processing that is needed for each field.  For example we could use the 
``strip_white_space`` processor to call pythons ``strip`` on each value.  Finally we decide if there is any 
extra validation that is needed on the values.  For example to ensure that the persons name starts with an "a"
we could use the ``RegexValidator``.  So with this information we would declare this DataContract like this::

    from pycontract import DataContract, StringField, NumberField, strip_white_space, RegexValidator
    
    class Person(DataContract):
        name = StringField(processors=(strip_white_space,), validators=(RegexValidator(r"[aA].+"),))
        phone = StringField(null=True)
        age = NumberField(null=True)

Now at runtime we can set the values, check for a valid contract and finally access the values.  That would like something
like this::

	>>> manny = Person()
	>>> manny["name"] = "Angel Man "
	>>> manny["phone"] = "999555-1234"
	>>> manny["age"] = 22
	>>> manny.is_valid()
	True
	>>> print manny.name
	'Angel Man'
	
This is early release and the code base is very short, so for more information see the code.  The source 
code can be found at github_.

.. _github: https://github.com/bigjason/pycontract
.. _MIT License: http://en.wikipedia.org/wiki/MIT_License