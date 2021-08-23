import os
import winshell
from pathlib import Path
import time
import sys
import concurrent.futures

def VipsSetup():
    ParentDirectory = os.path.join(winshell.my_documents(),"HelperScripts")
    os.makedirs(ParentDirectory, exist_ok=True)

    LibDirectory = os.path.join(ParentDirectory,"lib","vips")
    os.makedirs(ParentDirectory, exist_ok=True)

    vipshome = os.path.join(LibDirectory,"bin")
    os.environ['PATH'] = vipshome + ';' + os.environ['PATH']


VipsSetup()
import pyvips


def BatchConvert(fileList):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(SingleConvertHeictoJpeg, fileList)


def SingleConvertHeictoJpeg(Heicfile):
    image = pyvips.Image.new_from_file(Heicfile)
    out = Heicfile.replace("heic","jpg")
    image.jpegsave(out)
    FilePath = Path(Heicfile)
    ConvertedPath = os.path.join(FilePath.parent,"Converted",os.path.basename(FilePath))
    os.makedirs(Path(ConvertedPath).parent, exist_ok=True)
    os.rename(Heicfile,ConvertedPath)


if __name__ == "__main__":
    start = time.time()
    ClickedOnFolder = " ".join(sys.argv[1:])
    HeicList = []

    if ClickedOnFolder == "":
        HeicDirectory = r"C:\Users\adamr\OneDrive\Python Resource\ConvertTest"
    else:
        HeicDirectory = ClickedOnFolder

    for x in os.listdir(HeicDirectory):
        if "heic" in x:
            HeicList.append(os.path.join(HeicDirectory,x))
        if "HEIC" in x:
            HeicList.append(os.path.join(HeicDirectory,x))
        else:
            pass

    NumberOfFiles = len(HeicList)
    BatchConvert(HeicList)

    end = time.time()

    if NumberOfFiles == 0:
        print("No HEIC files found in directory")
    else:
        print(f"""
            Done! Converted {NumberOfFiles} Image files in {round(end-start,2)} seconds.\n
            Processed at a rate of {round(round(end-start, 2)/NumberOfFiles, 3)} seconds per Image.
            """)

    time.sleep(2)