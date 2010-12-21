"""Everything related to transactions is here."""

from controller import Controller
from jsonrpc.proxy import JSONRPCException

CATEGORY_UNDEF = ''
CATEGORY_SEND = 'send'
CATEGORY_RECEIVE = 'receive'
CATEGORY_MOVE = 'move'

class Transaction(object):
    def __init__(self, txid=None, category=CATEGORY_UNDEF, amount=0, message=None, fee=0, otheraccount=None):
        """Constructor. If txid is given and the transaction is known, all
           other information is read from the bitcoin controller."""
        self.txid = txid
        self.category = category
        self.amount = amount
        self.fee = fee
        self.otheraccount = otheraccount

    def read(self):
        """Read the transaction information from the bitcoin client. Return
           True if the transaction is known, False otherwise."""
        if self.txid is None:
            return False
        try:
            tx = Controller().gettransaction(self.txid)
        except JSONRPCException:
            return False
        self.amount = tx['amount']
        try:
            self.category = tx['category']
        except KeyError:
            if 0 <= self.amount:
                self.category = CATEGORY_RECEIVE
            else:
                self.category = CATEGORY_SEND
        self.fee = tx.get('fee', 0)
        self.message = tx.get('message')
        self.otheraccount = tx.get('otheraccount')
        return True

    def __getattr__(self, name):
        if 'confirmations' == name:
            try:
                tx = Controller().gettransaction(self.txid)
                return tx['confirmations']
            except JSONRPCException:
                return -1
