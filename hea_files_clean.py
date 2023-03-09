import pandas as pd
import glob

paths_hea = sorted(glob.glob('raw_data/*/*/*/*.hea'))#getting path for each .mat file

def fetch_lines(paths = paths_hea):
    lst = []
    for file in paths:        
        with open(file, 'r') as fp:
            lines = fp.readlines()[13:16] #fetching relavant lines
        lst.append(lines)    
    return lst


def fetch_id(paths = paths_hea):
    ids = []
    for file in paths:
        patient_id = file.split('/')[-1][2:-4]
        ids.append(patient_id)    
    return ids


def create_col(line_list): 
    line_list = fetch_lines()   
    for i in range(len(line_list)):
        line_list[i] = [x for xs in line_list[i] for x in xs.split(',')] # spliting dx values
        i +=1 
    return line_list   


def create_df(cols, id_col):
    df_concat = pd.DataFrame(cols)
    df_concat = df_concat.rename(columns = lambda x: f"Dx_{int(x)-1}" if int(x) > 1 else x)
    df_concat.columns.values[0:2] =["Age", "Sex" ]
    df_concat['id'] = id_col
    return df_concat


def clean_col(df, output):
    cols = df.columns
    for col in cols:
        if col != "Sex":
            df[col] = df[col].str.extract('(\d+)')
        else:
            df[col] = df[col].str.slice(6,7)
        df.to_csv(output, index = False)
    return df


output = 'data/hea_files.csv'
cols = create_col('line_list')
ids = fetch_id()
df = clean_col(create_df(cols, ids), output)
df.head()