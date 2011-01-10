# -*- coding: utf-8 -*-
# vi: sts=4 et sw=4

from controller import Controller
from jsonrpc.proxy import JSONRPCException

class Address(object):
    '''A Bitcoin address. Bitcoin properties of an address (for example its
       account) may be read and written like normal Python instance attributes
       (foo.account, or foo.account="blah").'''

    def __init__(self, address=None):
        '''Constructor. If address is empty, generate one.'''
        if address is None:
            address = Controller().getnewaddress()
        try:
            if not Controller().validateaddress(address)['isvalid']:
                raise InvalidBitcoinAddressError(address)
        except JSONRPCException:
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

    def uri(self):
        '''Return an URI for the address, of the form "bitcoin:17E9wnB...".
           At the moment, the URI takes no other argument yet.'''
        return "bitcoin:" + self.address

    def qrCode(self, size=80, level='L', formt=None, asURI=True):
        '''Return a string representing the QR code of the address. If `formt`
           is None, the internal format used by PIL is used, otherwise the
           image is converted to the desired format (e.g. 'PNG').
           The level can be one of 'L', 'M', 'Q' or 'H'.
           If `asURI` is True, encode the address's "bitcoin:" URI, otherwise
           encode the raw address.
           This method needs the qrencode module, and returns None if the
           module is not found.'''
        try:
            from qrencode import encode_scaled, QR_ECLEVEL_L, QR_ECLEVEL_M, \
                                 QR_ECLEVEL_Q, QR_ECLEVEL_H
        except ImportError:
            return None
        lvl = {'L': QR_ECLEVEL_L, 'M': QR_ECLEVEL_M, 'Q': QR_ECLEVEL_Q, \
               'H': QR_ECLEVEL_H}[level]
        if asURI:
            data = self.uri()
        else:
            data = self.address
        im = encode_scaled(data, size, level=lvl)[2]
        if formt is None:
            result = im.tostring()
        else:
            from StringIO import StringIO
            buf = StringIO()
            im.save(buf, formt)
            result = buf.getvalue()
            buf.close()
        return result

class InvalidBitcoinAddressError(Exception):
    '''The Bitcoin address is invalid.'''
    pass
