if ! command -v python &> /dev/null
then
    python -m pip install -r requirements_linux_freebsd.txt
fi

if ! command -v python3 &> /dev/null
then
    python3 -m pip install -r requirements_linux_freebsd.txt
fi

mv ../sites-example ../sites
mv ../config-example ../config
