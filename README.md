# Ducky Disco

This project allows you turn your Ducky keyboard int music equalizer

## Installation
`pipenv install`

## Run
Active pipenv

`pipnev shell`

Run main python script

`python src/main.py

After first run you will get the error:

*PermissionError: [Errno 13] Permission denied: '/dev/hidraw<X>'*. Where <X> - is a specific port number, assigned by OS
To resolve it you need to grant permissions to this port

`sudo chmod +x /dev/hidraw<X>`

