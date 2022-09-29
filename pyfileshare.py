#!/usr/bin/env python3
try:
    import os, random, socket
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
    print(f'''
{args[0]}, simple Python3-based file sharing script.
WARNING: This script uses no encryption whatsoever so be aware that connections to it can ONLY be made using the insecure HTTP protocol!

Arguments:
    --help -h Display this help and exit.
    --addr    Specify an address to listen on. Default is localhost
    --port    Specify a port to listen on. Default is a random port between 49152 and 65535
    --form    Specify a directory to serve from. Default is ./fileshare

A call with no arguments is equal to the following call:
{args[0]} --address=localhost --from=./fileshare

If the specified port is in use, this script will exit immediately. Retry with another port.
If the specified address cannot be accessed this script will exit immediately. Retry with another address.
If the specified serving directory cannot be opened this script tries one time to create and then open it. If that fails this script will exit immediately. Retry with another path.

NOTE: If this script fails with a permission error try running it with root, su or sudo permissions (*NIX) or with Admin privileges (Windows Vista and later). Be aware that higher privileges for this script can make your machine more vulnerable in case of an attack!
''')
    exit()

# Help doc end.

# Init start.

serve_dir = argument('--from')
if not serve_dir:
    serve_dir = './fileshare'
try:
    print(f'Opening {serve_dir} for file sharing...')
    os.chdir(serve_dir)
except OSError as e:
    print(': '.join([type(e).__name__, str(e)]))
    try:
        print(f'Creating serving directory: {serve_dir}...')
        os.mkdir(serve_dir)
        print(f'Opening {serve_dir} for file serving...')
        os.chdir(serve_dir)
    except Exception as e:
        print(f'Could not create/open {serve_dir}! Error message:\n{type(e).__name__}: {e}\nExiting due to the above exception...')
        exit(f'{type(e).__name__}: {e}')

if not argument('--address'):
    addr = 'localhost'
else:
    addr = argument('--address')
print(f'Chose address {addr} for serving.')

if not argument('--port'):
    print('Choosing a random port between 49152 and 65535...')
    port = random.randint(49152, 65535)
else:
    try:
        port = int(argument('--port'))
    except ValueError as e:
        print(f'Cannot use non-numerical port ("{argument("--port")}" was specified)!')
        print('Choosing a random port between 49152 and 65535...')
        port = random.randint(49152, 65535)
print(f'Chose port {port} for serving.')

def get_ip(): # This function is from https://stackoverflow.com/a/23822431/17865928, copied 2022-09-25 17:05
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]
print(f'Current LAN IP address: {get_ip()}')

# Init end.

try:
    server_object = HTTPServer(server_address=(addr, port), RequestHandlerClass=CGIHTTPRequestHandler)
    print(f'Server address: {addr}:{port}')
    server_object.serve_forever()
except Exception as e:
    print(f'Exception occurred!\n{type(e).__name__}: {e}\nServer on {addr}:{port} stopped!')
    if type(e) == KeyboardInterrupt:
        print('Exiting due to the user cancelling the script...')
        exit(type(e).__name__)
    else:
        print('Exiting due to the above exception...')
        exit(f'{type(e).__name__}: {e}')


