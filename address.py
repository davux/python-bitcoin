# -*- coding: utf-8 -*-
# vi: sts=4 et sw=4

from controller import Controller

class Address(object):
    '''A Bitcoin address. Bitcoin properties of an address (for example its
       account) may be read and written like normal Python instance attributes
       (foo.account, or foo.account="blah").'''

    def __init__(self, address=None):
        '''Constructor. If address is empty, generate one.'''
        if address is None:
            address = Controller().getnewaddress()
        if not Controller().validateaddress(address)['isvalid']:
            raise InvalidBitcoinAddressError(address)
        self.address = address

    def __str__(self):
        return self.address

    def __getattr__(self, name):
        if 'account' == name:
            return Controller().getaccount(self.address)

    def __setattr__(self, name, value):
        if 'account' == name:
            if value is None:
                Controller().setaccount(self.address)
            else:
                Controller().setaccount(self.address, value)
        else:
            object.__setattr__(self, name, value)

    def getReceived(self):
        '''Returns the total amount received on this address.'''
        return Controller().getreceivedbyaddress(self.address)

class InvalidBitcoinAddressError(Exception):
    '''The Bitcoin address is invalid.'''
    pass
