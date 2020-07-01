# replace-all
replace strings in a file in place recursively.

"okay...but why do i ned this?"
<br>
you work on a team where a tool is packaged maybe not as ideal as you'd like and any time the setup changes, you have to modify a dozen lines of code in a milliion files spanning several different directories. Sure, theres sed...its  great for onsies and twosies. but when you find 90 instances of a word spanning multiple locations, it starts to become a pain.
<br>
```bash
$ python bin/scripts/replace-all.py -h
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
```
<br>
