#!/usr/bin/env python3
'''
    Classes that inherit from base model
'''

from models.base_model import BaseModel

class Review(BaseModel):
    '''
        attr:
            place_id: string - empty string: it will be the Place.id
            user_id: string - empty string: it will be the User.id
            text: string - empty string
    '''
    place_id = ''
    user_id = ''
    text = ''
