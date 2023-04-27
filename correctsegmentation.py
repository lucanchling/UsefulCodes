import SimpleITK as sitk
import numpy as np
from dcmconvert import search
import os
import multiprocessing as mp

def correctseg(files):
    for file in files:
        if file.endswith("Seg_Max.nii.gz"):

            img = sitk.ReadImage(file)
            array = sitk.GetArrayFromImage(img)
            if max(np.unique(array)) != 1:
                print(os.path.basename(file),np.unique(array))
        else:
            img = sitk.ReadImage(file)
            size = np.array(img.GetSize())
            if size[0] <= 128 or size[1] <= 128 or size[2] <= 128:
                print(os.path.basename(file),size)
                # # print(array.shape)
                # correctarray = np.where(array == np.amax(array),0,0)

                # img = sitk.GetImageFromArray(correctarray)
                # sitk.WriteImage(img,os.path.join(out_dir,os.path.basename(file)))

if __name__ == "__main__":
    
    data_dir = "/home/luciacev/Desktop/Luc_Anchling/TRAINING/LATESTCleft/data/Patients"
    # out_dir = "/home/lucia/Desktop/Luc/DATA/AMASSS/CorrectSeg/"
    
    # if not os.path.exists(out_dir):
    #     os.makedirs(out_dir)

    files = search(data_dir,".nii.gz")[".nii.gz"]

    splits = np.array_split(files,mp.cpu_count())

    processes = [mp.Process(target=correctseg, args=(split,)) for split in splits]

    for p in processes:
        p.start()
    for p in processes:
        p.join()
        