#! python
# -*- coding: cp932 -*-

import glob
import shutil

directory = r'//192.168.1.247/���L/�c�Ɖ�̫���/testreport/�N�c/'
path = directory + '*20102951T*���^��*.pdf'
files = glob.glob(path)

for file in files:
    try:
        new_file_path = './'
        shutil.copy(file, new_file_path)

    except FileNotFoundError:
        print('File Not Found!')


