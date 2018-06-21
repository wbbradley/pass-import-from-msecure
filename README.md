# pass-import-from-msecure

This is a little script that I used to migrate my data out of mSecure, and into a local [password
store](https://www.passwordstore.org/).

This assumes you have installed `pass`.

## Step-by-step

1. Export your passwords from mSecure to a file. For example `$HOME/msecure-exported.csv`
2. Ensure that you have a `pass` store.
```
cd $HOME
pass init
```
3. Run this script against the exported file.
```
python import.py $HOME/msecure-exported.csv
```
4. `rm $HOME/msecure-exported.csv`
