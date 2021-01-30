import unittest
import os
from .models import Password as Password
from .models import User as User
from web.rest.helper.config_helper import PasswordValidation
class PasswordTest(unittest.TestCase):
    
    def setUp(self):
        self.password1 = "1234567"
        self.password2 = "ABC12345"
        self.password3 = "B%CF$#@123"
        self.password4 = "ABC"
    
    # Test password complexity
    def test_complexity(self):
        password1Test = PasswordValidation(self.password1)
        password1Test.check_all()              
        # self.assertFalse(any(password1Test.error_msg.values()))
        self.assertFalse(all(value == None for value in password1Test.error_msg.values()))

        password2Test = PasswordValidation(self.password2)
        password2Test.check_all()              
        self.assertTrue(all(value == None for value in password2Test.error_msg.values()))

        password3Test = PasswordValidation(self.password3)
        password3Test.check_all()              
        self.assertTrue(all(value == None for value in password3Test.error_msg.values()))

        password4Test = PasswordValidation(self.password4)
        password4Test.check_all()              
        self.assertFalse(all(value == None for value in password4Test.error_msg.values()))

    #Check the HIBP status
    def test_hibp(self):
        self.assertTrue(Password.is_hibp(self.password1))
        self.assertTrue(Password.is_hibp(self.password2))
        self.assertFalse(Password.is_hibp(self.password3))
        self.assertTrue(Password.is_hibp(self.password4))
    
    #Check the hashing function
    def test_hash_pwd(self):
        self.assertTrue(User.hash_pwd(self.password1))
        self.assertTrue(User.hash_pwd(self.password2))
        self.assertTrue(User.hash_pwd(self.password3))
        self.assertTrue(User.hash_pwd(self.password4))
    
    #Check the encrypt and decrypt
    def test_encrypt_decrypt(self):
        cipher_text = Password.encrypt_message(self.password3)
        decrypt_text = Password.decrypt_message(cipher_text).decode('utf-8')
        self.assertTrue(decrypt_text == self.password3)
        self.assertFalse(decrypt_text == self.password4)



    def tearDown(self):
        pass   

    
   
if __name__ == '__main__':
    unittest.main()