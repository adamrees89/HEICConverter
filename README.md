# HEICConverter
![GitHub](https://img.shields.io/github/license/adamrees89/HEICConverter.svg)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/adamrees89/HEICConverter.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/adamrees89/HEICConverter.svg)
[![Coverage Status](https://coveralls.io/repos/github/adamrees89/HEICConverter/badge.svg?branch=master)](https://coveralls.io/github/adamrees89/HEICConverter?branch=master)

![GitHub issues](https://img.shields.io/github/issues/adamrees89/HEICConverter.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/adamrees89/HEICConverter.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/adamrees89/HEICConverter.svg)

~~This is a wrapper around PyVips and Vips to enable me to batch convert images from Heic to Jpg for reporting.~~

Project has been updated to utilise pillow_heif

## Speed

Currently the script can process approximately 14.34 photos per second, depending on available cores, as it uses the [concurrent.futures module.](https://docs.python.org/3.3/library/concurrent.futures.html).  See the table below for the speed comparison before and after adding multithreading.

More information and quick tutorial on concurrent.futures:  https://gist.github.com/mangecoeur/9540178

|  |Number of Photos | Elapsed Time | Seconds/photo |
|---|---|---|---|
| VIPS No Multithreading | 9 | 21.97 seconds | 2.44 S/P |
| VIPS Mulithreading with concurrent.futures | 9 | 8.64 seconds| 0.96 S/P |
| Pillow and Pillow_heif Multithreading with concurrent.futures | 9 | 4.38 seconds | 0.49 S/P |

Having changed computer since, I didn't want to rerun the above numbers to get fair results, but starting with the last item, further improvements are shown below:

|  |Number of Photos | Elapsed Time | Seconds/photo |
|---|---|---|---|
| Pillow and Pillow_heif Multithreading with concurrent.futures | 120 | 26.9 seconds | 0.224 S/P |
| Multithreading with chunksize = 10 | 120 | 20.1 seconds | 0.168 S/P |
| Multithreading with chunksize = 5 | 120 | 19.32 seconds | 0.161 S/P |
| Multithreading with chunksize = 3 & directory traversing improvement | 120 | 8.9 seconds | 0.074 S/P |

Another computer change means a new set of numbers and photos. Starting with the fastest case above then progressing from there:

|  |Number of Photos | Elapsed Time | Seconds/photo |
|---|---|---|---|
| Multithreading with chunksize = 3 & directory traversing improvement | 320 | 32.48 seconds | 0.101 S/P |
| Optimised JPG quality | 320 | 31.29 seconds | 0.098 S/P |
| Multiprocessing instead of multithreading with chunksize = 3 | 320 | 23.14 seconds | 0.072 S/P |
| Multiprocessing with chunksize = 5 | 320 | 22.32 seconds | 0.070 S/P |