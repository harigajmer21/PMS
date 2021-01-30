from hashlib import md5
from web import app
import json
from datetime import datetime

class Constrain:
    def __init__(self):
        self.constrain = self.read_config()

    def read_config(self):
        constrain_data_loc = "constrain.json"
        with open(constrain_data_loc) as constrain:
            constrain = json.load(constrain)
        return constrain

    def last_update(self):                
        return app.config['CONF_MODIFIED_ON']    
    
    def count_caps(self, fieldName, fieldValue):        
        cap_condition = self.constrain[fieldName]['cap']             
        n_cap = len([l.isupper for l in fieldValue if l.isupper()==True])            
        if n_cap < cap_condition:
            return f'{fieldName} must have at least {cap_condition} capital letters'
        else:
            return None         
    
    def check_min_length(self, fieldName, fieldValue):
        min_length = self.constrain[fieldName]['min_length']
        if len(fieldValue) < min_length:           
            return f'{fieldName} length must have more than {min_length} characters'
        else:
            return None


    def has_number(self, fieldName, fieldValue):
        n_number = self.constrain[fieldName]['number']
        if n_number:
            if any(map(str.isdigit, fieldValue)):
                return None
            return f'{fieldName} must contain a number'
        return None

                # check if fieldvalue contains number or not



class UsernameValidation(Constrain):
    def __init__(self, username):
        super().__init__()
        self.username = username

    def check_all(self):        
        self.error_msg = {}
        field = 'username'
        
        self.error_msg['cap_err'] = self.count_caps(field, self.username)
        self.error_msg['min_len_error'] = self.check_min_length(field, self.username)
        return self.error_msg
    

class PasswordValidation(Constrain):
    def __init__(self, password):
        super().__init__()
        self.password = password

    def check_all(self):        
        self.error_msg = {}
        field = 'password'
        
        self.error_msg['cap_err'] = self.count_caps(field, self.password) 
        self.error_msg['min_len_error'] = self.check_min_length(field, self.password)
        self.error_msg['has_number'] = self.has_number(field, self.password)
        return self.error_msg
    

# class UsernameValidation:
#     def __init__(self, username):
#         self.username = username
#         self.constrain = self.read_config()              
    
#     def read_config(self):
#         constrain_data_loc = "constrain.json"
#         with open(constrain_data_loc) as constrain:
#             constrain = json.load(constrain)
#         return constrain

#     def check_all(self):
#         self.error_msg = {}
#         self.count_caps()
#         self.check_min_length()        
#         return self.error_msg

#     def last_update(self):        
#         # return datetime.strptime(self.constrain['last_update'], '%Y-%m-%d %H:%M:%S.%f')
#         return app.config['CONF_MODIFIED_ON']    
        
#     def count_caps(self):
#         cap_condition = self.constrain['username']['cap']             
#         n_cap = len([l.isupper for l in self.username if l.isupper()==True])            
#         if n_cap != cap_condition:
#             err_msg = f'username must have {cap_condition}'
#             self.error_msg['cap_err']= err_msg
    
#     def check_min_length(self):
#         min_length = self.constrain['username']['min_length']
#         if len(self.username) < min_length:           
#             err_msg = f'length must have more than {min_length} characters'
#             self.error_msg['min_len_err'] = err_msg
            
def dog_watch():
    import hashlib 
    hasher = hashlib.sha256()      
    with open(app.config['CONF_FILE'], 'rb') as f:        
        buf = f.read()
        hasher.update(buf)
        hash_check = hasher.hexdigest()
    
    return app.config['INIT_HASH_FILE'] == hash_check
