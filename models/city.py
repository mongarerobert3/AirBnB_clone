#!/usr/bin/env python3
'''
    Classes that inherit from base model
'''

from models.base_model import BaseModel

class City(BaseModel):
    '''
        attr:
            state_id: string - empty string: it will be the State.id
            name: string - empty string
    '''
    state_id = ''
    name = ''
