# Ducky Disco

This project allows you turn your Ducky keyboard into music equalizer

## Installation
`pipenv install`

## Run
Activate pipenv

`pipenv shell`

Run main python script

`python src/main.py`

After first run you will get an error:

*PermissionError: [Errno 13] Permission denied: '/dev/hidrawX'*. Where X - is a specific port number, assigned by OS.
To resolve it you need to grant permissions for this port

`sudo chmod 777 /dev/hidrawX`


