# HEICConverter
![GitHub](https://img.shields.io/github/license/adamrees89/HEICConverter.svg)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/adamrees89/HEICConverter.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/adamrees89/HEICConverter.svg)
[![Build Status](https://travis-ci.org/adamrees89/HEICConverter.svg?branch=master)](https://travis-ci.org/adamrees89/HEICConverter)
[![Coverage Status](https://coveralls.io/repos/github/adamrees89/HEICConverter/badge.svg?branch=master)](https://coveralls.io/github/adamrees89/HEICConverter?branch=master)

[![Known Vulnerabilities](https://snyk.io/test/github/adamrees89/HEICConverter/badge.svg)](https://snyk.io/test/github/adamrees89/HEICConverter)
![GitHub issues](https://img.shields.io/github/issues/adamrees89/HEICConverter.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/adamrees89/HEICConverter.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/adamrees89/HEICConverter.svg)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=WWZP5GMRRVPTQ&source=url)

This is a wrapper around PyVips and Vips to enable me to batch convert images from Heic to Jpg for reporting.


## Speed

Currently the script can process approximately XX photos per second, depending on available cores as it uses the [concurrent.futures module.](https://docs.python.org/3.3/library/concurrent.futures.html).  See the table below for the speed comparison before and after adding multithreading.

More information and quick tutorial on concurrent.futures:  https://gist.github.com/mangecoeur/9540178

|  |Number of Photos | Elapsed Time | Seconds/photo |
|---|---|---|---|
No Multithreading | 9 | 21.97 seconds | 2.44 |
Mulithreading with concurrent.futures | 9 | 8.64 seconds| 0.96|