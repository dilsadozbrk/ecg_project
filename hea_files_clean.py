import pandas as pd
import glob

paths_hea = sorted(glob.glob("raw_data/*/*/*/*.hea"))  # getting path for each .hea file


def fetch_lines(paths=paths_hea):
    """Extracts relavent lines from .hea files

    Args:
        line_list (list):

    Returns:
        list: Nested list of lines for each file
    """
    lst = []
    for file in paths:
        with open(file, "r") as fp:
            lines = fp.readlines()[13:16]  # fetching relavant lines from hea files
        lst.append(lines)
    return lst


def fetch_id(paths=paths_hea):
    """Extracts id number for each .hea file from their file names

    Args:
        paths (list): Defaults to paths_hea.

    Returns:
        list: list of id number for each patient
    """
    ids = []
    for file in paths:
        patient_id = file.split("/")[-1][2:-4]
        ids.append(patient_id)
    return ids


def create_col(line_list):
    """Splits lines which is seperated by ","

    Args:
        line_list (list): Nested list of lines for each file

    Returns:
        list
    """
    line_list = fetch_lines()
    for i in range(len(line_list)):
        line_list[i] = [
            x for xs in line_list[i] for x in xs.split(",")
        ]  # spliting dx values
        i += 1
    return line_list


def create_df(cols, id_col):
    """Creates concatenated df from 2 different list

    Args:
        cols (str): Column names for dataframe
        id_col (list): list of id number for each patient

    Returns:
        dataframe
    """
    df_concat = pd.DataFrame(cols)
    df_concat = df_concat.rename(
        columns=lambda x: f"Dx_{int(x)-1}" if int(x) > 1 else x
    )
    df_concat.columns.values[0:2] = ["Age", "Sex"]
    df_concat["id"] = id_col
    return df_concat


def clean_col(df, output):
    """Cleans column names of df and save the df as csv file

    Args:
        df (dataframe)
        output (str): path to save df as csv file

    Returns:
        df
    """
    cols = df.columns
    for col in cols:
        if col != "Sex":
            df[col] = df[col].str.extract("(\d+)")
        else:
            df[col] = df[col].str.slice(6, 7)
        df.to_csv(output, index=False)
    return df


output = "data/hea_files.csv"
cols = create_col("line_list")
ids = fetch_id()
df = clean_col(create_df(cols, ids), output)
df.head()
