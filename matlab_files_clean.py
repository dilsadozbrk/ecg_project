import pandas as pd
import glob
from scipy.io import loadmat as sc  # library to open .mab files


paths_mab = sorted(glob.glob("raw_data/*/*/*/*.mat"))


def cleanup_matmab(files, output):
    for n in range(len(files)):
        patient_id = files[n].split("/")[-1][2:-4]
        # print('Working on ' + patient_id)
        mat = sc(files[n])
        df = pd.DataFrame(mat["val"]).T
        df["Patient_id"] = patient_id
        if n == 0:
            df = df.rename(
                columns=lambda x: x if x == "Patient_id" else f"Dimension_{int(x)+1}"
            )
            df.to_csv(output, index=False)
        else:
            df.to_csv(output, mode="a", index=False, header=False)


files = paths_mab
output = "data/matlab_files/mab_all.csv"
cleanup_matmab(files, output)
