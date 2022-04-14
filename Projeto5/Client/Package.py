from enlace import *
import time
import numpy as np
import utils
import math
from utils import *

class Package:

    def __init__(self, type, originId, destinyId, payload = None, nPackage = None, nPackages = None):

        self.type = type
        self.originId = originId
        self.destinyId = destinyId
        self.payload = payload
        self.nPackage = nPackage
        self.nPackages = nPackages

        self.head = self.createHead()
        self.payload = payload
        self.eop = b'\xAA\xBB\xCC\xDD'


    def createHead(self):

        h0 = self.type.to_bytes(1,byteorder='big')
        h1 = self.originId.to_bytes(1,byteorder='big')
        h2 = self.destinyId.to_bytes(1,byteorder='big')

        h8 = b'\x00'
        h9 = b'\x00'

        if self.type == 1:
            h3 = self.nPackages.to_bytes(1,byteorder='big')
            h4 = self.nPackage.to_bytes(1,byteorder='big')
            h5 = b'\x00'
            h6 = b'\x00'
            h7 = b'\x00'


        elif self.type == 2:
            h3 = b'\x00'
            h4 = b'\x00'
            h5 = b'\x00'
            h6 = b'\x00'
            h7 = b'\x00'
        
        elif self.type == 3:
            h3 = self.nPackages.to_bytes(1,byteorder='big')
            h4 = self.nPackage.to_bytes(1,byteorder='big')
            h5 = (len(self.payload)).to_bytes(1,byteorder='big')
            h6 = b'\x00'
            h7 = b'\x00'

        elif self.type == 4:
            h3 = b'\x00'
            h4 = b'\x00'
            h5 = b'\x00'
            h6 = b'\x00'
            h7 = self.nPackage.to_bytes(1,byteorder='big')

        elif self.type == 5:
            h3 = b'\x00'
            h4 = b'\x00'
            h5 = b'\x00'
            h6 = b'\x00'
            h7 = b'\x00'

        elif self.type == 6:
            h3 = b'\x00'
            h4 = b'\x00'
            h5 = b'\x00'
            h6 = self.nPackage.to_bytes(1,byteorder='big')
            h7 = (self.nPackage-1).to_bytes(1,byteorder='big')

        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        return head

    def getContent(self):
        if self.payload is None:
            return self.head + self.eop
        else:
            return self.head + self.payload + self.eop
