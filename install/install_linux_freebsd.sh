#!/bin/sh

if command -v python3 &> /dev/null
then
    python3 -m pip install -r ./requirements_linux_freebsd.txt
else
    if command -v python &> /dev/null
    then
        python -m pip install -r ./requirements_linux_freebsd.txt
    fi
fi

echo "Moving config and site directories"
mv ../sites-example ../sites
mv ../config-example ../config
