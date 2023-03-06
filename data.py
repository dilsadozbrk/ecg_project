import pandas as pd
import glob 
from scipy.io import loadmat as sc # library to open .mab files

parent_path = ('raw_data/WFDBRecords/01/010/')
paths_hea = glob.glob(parent_path + '*.hea') #getting path for each .hea file
paths_mab = glob.glob(parent_path + '*.mat') #getting path for each .hea file
print(len(paths_hea))


#converting all .mat files to csv and store in ./data/matlab_files directory
for file in paths_mab:
    for n in range(1, len(paths_mab)):
        mat=sc(file)
        df_mat= pd.DataFrame(mat['val'])
        df_mat.to_csv(f'data/matlab_files/mab{n}.csv')

lst = []
for file in paths_hea:
    with open(file, 'r') as fp:
        lines = fp.readlines()[13:16] #fetching relavant lines
    lst.append(lines)                 #nested list with all relavent lines

for i in range(len(lst)):
    lst[i] = [x for xs in lst[i] for x in xs.split(':')] # spliting list elements to get column values
    lst[i] = [x.replace("#", "").replace(" ", "").replace("\n", "") for x in lst[i]] # cleaning special characters
    i +=1
    
# creating a list to store only column names
keys = ['Age', 'Sex', 'Dx']     
# Remove column names from list to store only values
values = [[sub_itm for sub_itm in sub_list if sub_itm not in keys] for sub_list in lst]  
df = pd.DataFrame(values, columns = keys) 
df.to_csv('data/data.csv', sep=';', index=None)






