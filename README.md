# pyfileshare
A very simple Python script to serve a specific directory on the computer as a web server. Intended for file sharing. 

## Dependencies
* `python3` (tested to work with `python3.10`)
* `python3` modules `os`, `sys`, `random`, `http.server`

## `--help` output
```

 ./pyfileshare.py, simple Python3-based file sharing script.
 WARNING: This script uses no encryption whatsoever so be aware that connections to it can ONLY be made using the insecure HTTP protocol!

Arguments:
    --help -h Display this help and exit.
    --addr    Specify an address to listen on. Default is localhost
    --port    Specify a port to listen on. Default is a random port between 49152 and 65535
    --form    Specify a directory to serve from. Default is ./fileshare

A call with no arguments is equal to the following call:
./pyfileshare.py --address=localhost --from=./fileshare

If the specified port is in use, this script will exit immediately. Retry with another port.
If the specified address cannot be accessed this script will exit immediately. Retry with another address.
If the specified serving directory cannot be opened this script tries one time to create and then open it. If that fails this script will exit immediately. Retry with another path.

NOTE: If this script fails with a permission error try running it with root, su or sudo permissions (*NIX) or with Admin privileges (Windows Vista and later). Be aware that higher privileges for this script can make your machine more vulnerable in case of an attack!

```
## Notes
It's not very safe to use it in public networks as it cannot serve over a secure connection. Use at your own risk. No file upload intended, only for viewing the files in the served directory. If a directory contans an `index.html` that will be shown instead of the file list of that directory, `index.php` will not override the file view. 
