# Simplebackup

## Description

Simple backup python script to backup a file or directory.

## Usage 
Base usage
```
./simplebackup.py [-h] [--copies COPIES] src dest
```
Examples
```
./simplebackup.py --copies 6 ./file/to/backup.txt ./mybackup/folder
```
Copies _./backup.txt_ to _./mybackup/folder_ with a date appended. The `--copies 6` argument ensures that only 6 of the most recent backups will be kept. 

The intended idea is to add this script to `chrontab` or whatever scheduler service of your OS. 

## Notes
The default backup format is `%Y_%m_%d_[filename].bkp`. The datetime can be changed in the constants at the top of the program

The granularity of the date resolution is per day therefore any consecutive backups made in the same day will be overwritten.
If the date format is changed to include hours, minutes, etc... this granularity will change.

