#!/usr/bin/env python3

class Person():
    __firstname = None
    __lastname = None

    def __init__(self, firstname, lastname):
        self.__firstname = firstname
        self.__lastname = lastname
    
    @property
    def fullname(self):
        return f"{self.__firstname} {self.__lastname}"

    @property
    def firstname(self):
        return self.__firstname
    
    @firstname.setter
    def firstname(self, name):
        self.__firstname = name
    
    @firstname.deleter
    def firstname(self):
        self.__firstname = None

person = Person("Peter", "Mgembe")

person.firstname = "James"
del person.firstname
print(person.fullname)