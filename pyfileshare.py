#!/usr/bin/env python3
try:
    import os, random
    from http.server import HTTPServer, CGIHTTPRequestHandler
except Exception as e:
    print(': '.join([type(e).__name__, str(e)]))
    exit()
from sys import argv
args = argv.copy()
del argv

def argument(argument_to_search_for):
    if not argument_to_search_for in args:
        for arg in args:
            if arg[0:len(argument_to_search_for)+1] == argument_to_search_for+'=':
                return arg.split('=', 1)[1]
        return False
    else:
        return True

# Help doc start.

if argument('--help') or argument('-h'):
    print('''
{name}, simple Python3-based file sharing script.
WARNING: This script uses no encryption whatsoever so be aware that connections to it can ONLY be made using the insecure HTTP protocol!

Arguments:
    --help -h Display this help and exit.
    --addr    Specify an address to listen on. Default is localhost
    --port    Specify a port to listen on. Default is a random port between 10000 and 65535
    --form    Specify a directory to serve from. Default is ./fileshare

A call with no arguments is equal to the following call:
{name} --address=localhost --from=./fileshare

If the specified port is in use, this script will exit immediately. Retry with another port.
If the specified address cannot be accessed this script will exit immediately. Retry with another address.
If the specified serving directory cannot be opened this script tries one time to create and then open it. If that fails this script will exit immediately. Retry with another path.

NOTE: If this script fails with a permission error try running it with root, su or sudo permissions (*NIX) or with Admin privileges (Windows Vista and later). Be aware that higher privileges for this script can make your machine more vulnerable in case of an attack!
'''.format(name=args[0]))
    exit()

# Help doc end.

# Init start.

serve_dir = argument('--from')
if not serve_dir:
    serve_dir = './fileshare'
try:
    print('Opening {} for file sharing...'.format(serve_dir))
    os.chdir(serve_dir)
except OSError as e:
    print(': '.join([type(e).__name__, str(e)]))
    try:
        print('Creating serving directory: {}...'.format(serve_dir))
        os.mkdir(serve_dir)
        print('Opening {} for file serving...'.format(serve_dir))
        os.chdir(serve_dir)
    except Exception as e:
        print('Could not create/open {}! Error message:\n{}: {}\nExiting due to the above exception...'.format(type(e).__name__, str(e)))
        exit('{}: {}'.format(type(e).__name__, str(e)))

if not argument('--address'):
    addr = 'localhost'
else:
    addr = argument('--address')
print('Chose address {} for serving.'.format(addr))

if not argument('--port'):
    print('Choosing a random port between 10000 and 65535...')
    port = random.randint(10000, 65535)
else:
    try:
        port = int(argument('--port'))
    except ValueError as e:
        print('Cannot use non-numerical port ("{}" was specified)!'.format(argument('--port')))
        print('Choosing a random port between 10000 and 65535...')
        port = random.randint(10000, 65535)
print('Chose port {} for serving.'.format(port))

# Init end.

try:
    server_object = HTTPServer(server_address=(addr, port), RequestHandlerClass=CGIHTTPRequestHandler)
    print('Server address: {}:{}'.format(addr, port))
    server_object.serve_forever()
except Exception as e:
    print('Exception occurred!\n{}: {}\nStopping server on {}:{}'.format(type(e).__name__, str(e), addr, port))
    if type(e) == KeyboardInterrupt:
        print('Exiting due to the user cancelling the script...')
        exit(type(e).__name__)
    else:
        print('Exiting due to the above exception...')
        exit('{}: {}'.format(type(e).__name__, str(e)))

