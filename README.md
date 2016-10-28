# 15_midnighters

The program finds Devman users who sent their solutions at night. The term night is defined here as the time between midnight and dawn, where dawn can be defined by user and is 5 AM by default. It only looks for users who submitted their attempts not so long ago, as the API only allows to access 10 pages of logs.   

Dawn time is the only positional integer argument. 5 by default.   

### How to use

> python seek_dev_nighters.py   

Find all users made an attempt between 12 AM and 5 AM   

> python seek_dev_nighters.py 6   

Find all users made an attempt between 12 AM and 6 AM   

