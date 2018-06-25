import os
import sys
import csv
import subprocess

def main():
    if len(sys.argv) != 2:
        print("usage: import.py msecure-export-filename")
        return
    f = open(sys.argv[1], "r")
    reader = csv.reader(f)

    # skip the first line
    next(reader)

    seen_names = set({})
    for r in reader:
        row = lambda x: None if len(r) <= x else r[x]
        subdir = row(0)
        name = row(2) + ((" - " + subdir) if (subdir != 'Unassigned') else "")
        if name in seen_names:
            print("Skipping duplicate: " + name)
        else:
            pass_insert(subdir=None,
                        name=name,
                        password=row(6),
                        url=row(4),
                        user=row(5),
                        notes=row(3).replace('\r', '\n') if row(3) else None)

def pass_insert(subdir, name, password, url, user, notes):
    remapping = {
        '/': '-',
        '\\': '-',
        ' ': '-',
        "'": '',
        '"': '',
        '(': '',
        ')': '',
        '+': '-',
        '$': '',
        '`': '',
        '#': '-',
        '&': '-',
        '|': '-',
    }
    for a, b in remapping.items():
        name = name.replace(a, b)
    while '--' in name:
        name = name.replace('--', '-')

    cmd = "pass insert -m \"" + (os.path.join(subdir, name) if subdir else name) + "\""
    print(cmd)
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)

    injects = [((k + ": ") if k else "") + v
               for k, v in {
                       "": password,
                       "User": user,
                       "Url": url,
                       "Notes": notes,
               }.items()
               if v]
    inject = '\n'.join(injects) + '\n'
    proc.communicate(inject)
    proc.wait()

if __name__ == "__main__":
    main()
