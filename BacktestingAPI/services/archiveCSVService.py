import os
import glob
from datetime import date
from BacktestingAPI.services.constants import PATH

def archive():
    today = date.today()
    todayString = today.strftime("%Y%m%d")
    
    for xlsxfile in glob.glob(PATH + f'/*.xlsx'):
        originalFile = xlsxfile.replace("\\", "/")
        archivePath = f'{PATH}/Archive/{todayString}'
        if not os.path.exists(archivePath):
            os.makedirs(archivePath)
        
        os.rename(originalFile, f'{archivePath}/{os.path.basename(xlsxfile)}')
