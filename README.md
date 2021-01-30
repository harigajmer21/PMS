# PMS
A customer wants a Password Management System (PMS) that centrally stores manages and evaluates the passwords of users in legacy applications. 
The main requirements of the system are as follows: -

A. support generation of passwords
B. according to a configurable expression (length, number of upper/lower/special characters)
C. force renewal of existing passwords in case configuration changes
D. storage of password
E. evaluate passwords as part of an authentication process.
F. any service request must be made available via REST/JSON API calls
G. The system must connect and use an external owned password service.

Please follow the document for more details on how to create, manage and operate available features.

# Requirements
1. Python 3.6+
2. pip install -r requirements.txt
3. Postman / curl to test REST services


# How to Run
1. python run.py 

# Run test cases
1. python -m unittest
