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

Currently the script can process approximately XX photos per second, depending on available cores as it uses the [concurrent.futures module.](https://docs.python.org/3.3/library/concurrent.futures.html).  See the table below for the speed comparison before and after adding multithreading.

More information and quick tutorial on concurrent.futures:  https://gist.github.com/mangecoeur/9540178

|  |Number of Photos | Elapsed Time | Seconds/photo |
|---|---|---|---|
VIPS No Multithreading | 9 | 21.97 seconds | 2.44 |
VIPS Mulithreading with concurrent.futures | 9 | 8.64 seconds| 0.96 |
Pillow and Pillow_heif Multithreading with concurrent.futures | 9 | 4.38 seconds | 0.49 |