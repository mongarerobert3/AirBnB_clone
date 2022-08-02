#!/usr/bin/env python3
'''
    Classes that inherit from base model
'''

from models.base_model import BaseModel

class Amenity(BaseModel):
    '''
        attr:
            name: string - empty string
    '''
    name = ''
