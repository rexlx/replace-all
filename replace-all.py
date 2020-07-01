import argparse
import os
import time
import shutil
import datetime as dt
import fileinput

"""
this tool will search for a string recursively and replace it with
something else. it backups up the directory by default, but that can be
disabled.

argparse handles the help output...its kind of gross :)

$ python replace-all.py -h
usage: replace-all.py [-h] [-r] -d DIR --match MATCH --replace REPLACE
                      [--im-stupid]

replace a specific string in all files at specified location

optional arguments:
  -h, --help         show this help message and exit
  -r                 recursively (look in all subdirs)
  -d DIR             directory to look in
  --match MATCH      string to match
  --replace REPLACE  replacement string
  --im-stupid        dont back up the directory
"""
# if you want to change the logs name...
logfile = os.path.expanduser("~") + "/replace.log"

def log_it(logfile, time, alert, string):
    date_string = dt.datetime.fromtimestamp(time).strftime(
                 '%Y-%m-%d %H:%M:%S')
    with open(logfile, 'a') as f:
        f.write('\n' + date_string + ': ' + alert + '\n')
        f.write(string)
        f.write('\n')


def get_files(recursive, path):
    """
    returns a list of files with full paths. requires two parameters:
    recursive (boolean) and path (string).

    This function utilizes list comprehensions, for non-python folk,
    you may need to do a little googling as they arent always readable
    to the naked eye
    """
    msg = "getting file list, recursive=" + str(recursive)
    log_it(logfile, time.time(), "info", msg)
    if not recursive:
        # this makes a list of just filenames (no paths)
        filenames = [e for e in os.listdir(path)]
        # but we wants full paths, use an os path join
        file_list = [os.path.join(path, e) for e in filenames]
    else:
        # this will decend into all subdirs
        file_list = [os.path.join(dir_path, x)
                     for dir_path, dirs, files in os.walk(path)
                     for x in files]
    return file_list

def main():
    msg = "replace a specific string in all files at specified location"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument(
                        '-r',
                        dest='recursive',
                        action="store_true",
                        help="recursively (look in all subdirs)"
                        )
    parser.add_argument(
                        '-d',
                        dest='dir',
                        required=True,
                        help="directory to look in"
                        )
    parser.add_argument(
                        '--match',
                        dest='match',
                        required=True,
                        help="string to match"
                        )
    parser.add_argument(
                        '--replace',
                        dest='replace',
                        required=True,
                        help="replacement string"
                        )
    parser.add_argument(
                        '--im-stupid',
                        dest='dumb',
                        action="store_true",
                        help="dont back up the directory"
                        )
    args = parser.parse_args()
    if args.recursive:
        recursive = True
    else:
        recursive = False
    if args.dumb:
        dumb = True
    else:
        dumb = False
    # get the list of files
    files = get_files(recursive, args.dir)
    # this is the users home dir
    user_dir = os.path.expanduser("~")
    try:
        backup_dir = "{}/{}/{}".format(
                                       str(int(time.time())),
                                       user_dir,
                                       args.dir
                                       )
    except Exception as e:
        # user is on unsupported version of
        # python, use legacy concat
        backup_dir = str(int(time.time())) + "/" + user_dir + "/" + args.dir
    if not dumb:
        msg = "creating backup in user home dir"
        log_it(logfile, time.time(), "info", msg)
        print("backing up source directory...")
        shutil.copytree(args.dir, backup_dir)
        print("completed backup")
    else:
        msg = "user elected to NOT backup the src dir"
        log_it(logfile, time.time(), "info", msg)
        print("you have chosen not to backup, may god have mercy on your soul")
    print("looking for files that match..")
    for i in files:
        try:
            with open(i) as f:
                data = f.read()
        except Exception as e:
            log_it(logfile, time.time(), "warn", str(e))
            print(e)
        if args.match in data:
            for line in fileinput.input(i, inplace=True, backup=".backup"):
                line = line.rstrip().replace(args.match, args.replace)
                print(line)
        else:
            # file doesnt contain string, restart the loop
            continue

# if this script is being run (but not imported)
if __name__ == "__main__":
    # do the dang thang
    main()
    print("complete, directory was backed up in the users home directory")
    print("logfile is:\t" + logfile)

