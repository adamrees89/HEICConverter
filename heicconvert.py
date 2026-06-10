import os
from pathlib import Path
import time
import sys
import concurrent.futures
import re
from PIL import Image
from pillow_heif import register_heif_opener
from tkinter import Tk
from tkinter.filedialog import askdirectory
#from progress.bar import Bar
from tqdm import tqdm

def init_worker():
    register_heif_opener()

def BatchConvert(fileList, NumberOfFiles):
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    with concurrent.futures.ProcessPoolExecutor(initializer=init_worker,
                                                max_workers=os.cpu_count()) as executor:
        list(tqdm(executor.map(SingleConvertHeictoJpeg, fileList, chunksize=5), total=NumberOfFiles))

def SingleConvertHeictoJpeg(Heicfile):
    #Open the image
    try:
        image = Image.open(Heicfile)
    except Exception as e:
        tqdm.write(f"Open/save failed for {Heicfile}: {e}")
        return
    #Change the extension from heic to jpg
    # outName = Heicfile.replace(".heic",".jpg")
    outName = re.sub(re.escape(".heic"),".jpg",Heicfile,flags=re.IGNORECASE)
    #Save the new image as outName (New Extension)
    image.save(outName,
               "JPEG",
               quality=90,
               optimize=False,
               progressive=False)
    #The below lines take the original photo filepath and modify it so the photos move into the converted subfolder
    FilePath = Path(Heicfile)
    ConvertedPath = os.path.join(FilePath.parent,"Converted",os.path.basename(FilePath))
    os.makedirs(Path(ConvertedPath).parent, exist_ok=True)
    os.rename(Heicfile,ConvertedPath)


if __name__ == "__main__":
    ClickedOnFolder = " ".join(sys.argv[1:])
    HeicList = []

    if ClickedOnFolder == "":
        Tk().withdraw()
        HeicDirectory = askdirectory()
    else:
        HeicDirectory = ClickedOnFolder

    HeicDirectory = os.path.normpath(HeicDirectory)
    
    start = time.time()

# Old Single Folder file finder:
    # for x in os.listdir(HeicDirectory):
    #     if "heic" in x:
    #         HeicList.append(os.path.join(HeicDirectory,x))
    #     if "HEIC" in x:
    #         HeicList.append(os.path.join(HeicDirectory,x))
    #     else:
    #         pass

# New sub-folder file finder:

    for root, dirs, files in os.walk(HeicDirectory):
        if 'Converted' in dirs:
            dirs.remove('Converted')
        for x in files:
            if x.lower().endswith('.heic'):
                HeicList.append(os.path.join(root,x))

    NumberOfFiles = len(HeicList)
    
    endFileOps = time.time()

    if NumberOfFiles == 0:
        print("No HEIC files found in directory")
    else:
        print(f"""
            Attempting to convert {NumberOfFiles} Image files\n
            """)
        
        startConvert = time.time()

        BatchConvert(HeicList, NumberOfFiles)

        end = time.time()

        print(f"""
            Done! Converted {NumberOfFiles} Image files in {round(end-start,2)} seconds.\n
            Processed at a rate of {round(round(end-start, 2)/NumberOfFiles, 3)} seconds per image or {round(NumberOfFiles/round(end-start, 2), 3)} images per second
            """)
        
        # print(f"""
        #       Time benchmarking:\n
        #         Total time: {round(end-start,2)} seconds\n
        #         Time to find files: {round(endFileOps-start,2)} seconds\n
        #         Time to convert files: {round(startConvert-endFileOps,2)} seconds\n
        #       """)

    time.sleep(2)