#! python
# -*- coding: cp932 -*-

import glob
import shutil

directory = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/testreport/櫻田/'
path = directory + '*20102951T*旭真空*.pdf'
files = glob.glob(path)

for file in files:
    try:
        new_file_path = './'
        shutil.copy(file, new_file_path)

    except FileNotFoundError:
        print('File Not Found!')


