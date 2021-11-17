#!/usr/bin/env python3
import argparse
import pathlib
from datetime import date, datetime
import logging
import shutil
import sys
import os
import re

LOGGER_NAME='simplebackup'
DATETIME_STRING='%Y_%m_%d'

# Sets up a basic logger
def setup_logger():
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT)

# Parse cli arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Simple file backup.')
    parser.add_argument('--copies', type=int, help='maximum number of copies to keep', default=12)
    parser.add_argument('src', type=pathlib.Path, help='src file to backup')
    parser.add_argument('dest', type=pathlib.Path, help='backup directory')
    return parser.parse_args()

# Creates backup file name based on src file, returns a string of the destination file name
def create_file_name(src):
    date_string = date.today().strftime(DATETIME_STRING)
    file_name = src.name
    return f'{date_string}_{file_name}.bkp'

# Copies the backup file to destination
def transfer_file(src, dest):
    dest_path = os.path.join(dest.resolve(), create_file_name(src))
    if src.is_dir():
        if src.exists():
            shutil.rmtree(dest_path)
        shutil.copytree(src.resolve(), dest_path)
    else:
        shutil.copy(src.resolve(), dest_path)

# Checks if files in the dest directory match a backup file
# Returns a list of the backup files with their corresponding date
def get_backup_files(src, dest):
    base_regex = '^(?P<date>[\\d]{4}_[01][\\d]_[0123][\\d])_' + src.name + '\\.bkp$'
    engine = re.compile(base_regex)
    backup_files = []
    for child in dest.iterdir():
        res = engine.match(child.name)
        if child.exists() and res:
            backup_date = datetime.strptime(res.groupdict()['date'], DATETIME_STRING)
            backup_files.append((backup_date, child))
    return backup_files

# Delete stale backups
def delete_stale_backups(stale_backups):
    for backup in stale_backups:
        path = backup[1]
        if not path.exists():
            continue
        if path.is_dir():
            shutil.rmtree(path.resolve())
        else:
            path.unlink()



# Removes old backups based on the number of copies requested
def cleanup_backups(src, dest, count):
    # Get backup like files
    backup_files = get_backup_files(src, dest)
    # Sort them based on their date in the filename with most recent at the top
    backup_files.sort(key=lambda x: x[0], reverse=True)
    # Slice off old backups
    stale_backups = backup_files[count:]
    delete_stale_backups(stale_backups)
    



def main():
    # Setup logging
    setup_logger()
    logger = logging.getLogger(LOGGER_NAME)
    # Parse arguments
    args = parse_args()
    # Validate arguments
    if not args.src.exists():
        logger.error('src file does not exist')
        sys.exit(1)
    if not args.dest.exists():
        args.dest.mkdir()
    # Make the file transfer
    try:
        transfer_file(args.src, args.dest)
    except IOError as e:
        logger.error(f'unable to backup file: {args.src.resolve()}, {e}')
        sys.exit(1)
    # Cleanup extra backups
    try:
        cleanup_backups(args.src, args.dest, args.count)
    except IOError as e:
        logger.error(f'unable to cleanup backups, {e}')
        sys.exit(1)



if __name__=='__main__':
    main()