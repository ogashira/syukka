import platform
import pdfplumber
import subprocess
from typing import List, Dict
import pandas as pd

class TssCoaFromMhs:

    def __init__(self, MHS_nonExistent_coa: List[List[str]], 
                 coa_folder: str)-> None:
        """
        HS_nonExistent_coaはnonExistent_coaの中の品管ｼｰﾄ分のみ
        """
        self.MHS_nonExistent_coa: List[List[str]] = MHS_nonExistent_coa
        self.coa_folder: str = coa_folder

        self.exe_path: str = r'/mnt/public/TSS_System/TssSystem/ToyoKogyo/Bat/' \
                        r'ToyoKogyoMhsRepBat/ToyoKogyoMhsRepBat.exe'
        if platform.system() == 'Windows':
            self.exe_path: str = r'//192.168.1.247/共有/TSS_System/TssSystem/' \
                    r'ToyoKogyo/Bat/ToyoKogyoMhsRepBat/ToyoKogyoMhsRepBat.exe'

    
    def create_coa(self)-> List[List[str]]:

        nonCreate_coa: List[List[str]] = []

        for line in self.MHS_nonExistent_coa:
            lot: str = line[0]
            args = ["--lot", lot, "--outputdir", self.coa_folder]
            result = None

            try:
                result = subprocess.run(
                        [self.exe_path] + args,
                        capture_output=True,
                        text=True
                        )
            except Exception as e: 
                nonCreate_coa.append(line)

            '''
            resultのreturncodeが1でないとcoaは発行されていない。これは例外で
            引っかからない。従って、resultのreturncode=1でない時は、nonCreate_coaに
            appendする
            '''
            if result.returncode != 1:
                line.append(f'result.returncode={result.returncode}')
                nonCreate_coa.append(line)

        
        return nonCreate_coa
