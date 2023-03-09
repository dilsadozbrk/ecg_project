from multiprocessing import Pool
import glob
import multi_def
import pandas as pd

paths_mab = glob.glob('raw_data/*/*/*/*.mat') 
file_list = sorted(paths_mab)[:100]
print(file_list)


if __name__ == '__main__':
    try:
        p = Pool()
        p.map(multi_def.cleanup, file_list)
    
    except:
        FileNotFoundError


df = pd.read_csv('data/matlab_files/mab_pool.csv')
print(df.shape)
print(df['Patient_id'].value_counts())