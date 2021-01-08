#! python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import pandas as pd

class Recorder(object):


    def __init__ (self, myfolder):
        self.myfolder = myfolder

        
    def out_log (self, txt, rtn=''):
        print('{}{}'.format(txt, rtn))

        
    def out_file (self, txt, rtn=''):
        filePath = '{}/Robot_log.txt'.format(self.myfolder)
        with open(filePath, 'a') as result:
            print('{}{}'.format(txt, rtn), file = result)


    def out_csv (self, df, filePath):
        df.to_csv(filePath, encoding='cp932')

                    
