1. See examples in /basics first 1 by 1
2. Function vs method:
    Function is like when we defined alone without class or not in the class, for ex: len() this is func.
    Method is defined with self.signin() see in examples and which created under class.
3. Self: Represents the specific instance of the class that u currently working with. It allows individual objects to access and maintain their own unique data and methods.
4. Encapsulation: Hiding some of the attributes which is not required to be public or u do not wanted to access from outside/public. See ex in oop_proj.py
In python we cannot actually fully hide/protect the data like we can do in Java but pyhton gives us the functionality to hide it and use it.
5. Getter and setter: we hided the attribute but what if we want to get and change it values we can do using getter and setter. See ex in oop_proj.py.
6. Static method: we can create a static method and use it 
7. Inheritance: It is a way to inherit a child classes into the parent class for more reusability. But parent class has no access to child class.
Constructor, non private attributes and non private methods are inherited.
Constructor overloading: if __init__ constructor is used inside a both parent and child class and child class called then child class contructor will be return not the parent class constructor. Same is with methods if same methods are there in both classes then which class is called their method will takeover/return.
But using super() method we can use both constructors and methods see ex in 4-inheri.py. Super can used within the class only. Only whole method/constructor can be access cannot access individual attribute using super.

Advance inheritance: 1.single inh 2.multilevel inhe 3.Hierarchical 4.Multiple/diamond 5.Hybrid
----------------------------------------------
DVC - Data versioning
1. Data versioning is similar to create versions of the your ML pipeline for rollbacks, upgrades, etc.
2. This pipeline contains [Data ingestion] -> [Data preprocessing] -> [Feature engineering] -> [Feature selection] -> [Model training] -> [Model Evalution].
3. There will be a multiple versions you can create using DVC so we can do upgrades, rollbacks if required.