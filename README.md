# HEICConverter
![GitHub](https://img.shields.io/github/license/adamrees89/HEICConverter.svg)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/adamrees89/HEICConverter.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/adamrees89/HEICConverter.svg)

![GitHub issues](https://img.shields.io/github/issues/adamrees89/HEICConverter.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/adamrees89/HEICConverter.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/adamrees89/HEICConverter.svg)

~~This is a wrapper around PyVips and Vips to enable me to batch convert images from Heic to Jpg for reporting.~~

Project has been updated to utilise pillow_heif

## Speed

Currently the script can process approximately 13.5 photos per second, depending on available cores as it uses the [concurrent.futures module.](https://docs.python.org/3.3/library/concurrent.futures.html).  See the table below for the speed comparison before and after adding multithreading.

More information and quick tutorial on concurrent.futures:  https://gist.github.com/mangecoeur/9540178

|  |Number of Photos | Elapsed Time | Seconds/photo |
|---|---|---|---|
VIPS No Multithreading | 9 | 21.97 seconds | 2.44 |
VIPS Mulithreading with concurrent.futures | 9 | 8.64 seconds| 0.96 |
Pillow and Pillow_heif Multithreading with concurrent.futures | 9 | 4.38 seconds | 0.49 |

Having changed computer since, I didn't want to rerun the above numbers to get fair results, but starting with the last item, further improvements are shown below:

|  |Number of Photos | Elapsed Time | Seconds/photo |
|---|---|---|---|
Pillow and Pillow_heif Multithreading with concurrent.futures | 120 | 26.9 seconds | 0.224 |
Multithreading with chunksize = 10 | 120 | 20.1 seconds | 0.168 |
Multithreading with chunksize = 5 | 120 | 19.32 seconds | 0.161 |
Multithreading with chunksize = 3 & directory traversing improvement | 120 | 8.9 seconds | 0.074 |