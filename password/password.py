from setting import *
from json import load
import os 
basedir = os.path.abspath(os.path.dirname(__file__))


class Password:

    def password_complexity(password):
        #Load the json file and check the complexity
        with open(basedir + '/'+'password_config.json', 'r') as file:
            fields = load(file)
            uppercase = fields['Uppercase']
            lowercase = fields['Lowercase']
            digits = fields['Digits']
            spCharacters = fields['spCharacters']

            print(fields)

            if uppercase:
                print ("True")
                return True
            
            elif lowercase:
                print ("True")
                return True

            elif digits:
                print ("True")
                return True
            elif spCharacters:
                print ("True")
                return True

    def  hibp(password):
        #Load the HIPB api and check the password is exist or not
        if hibp_response is True:
            print("This password is in HIBP Status database")
            return True
        else:
            return False #This means this password is secure. and good password

    def encrypt(password):
        #Do the encrypt process
        print("this is encrypt function")

        

