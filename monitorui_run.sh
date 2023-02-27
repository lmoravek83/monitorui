if command -v python3 > /dev/null
then
    python3 ./monitorui.py
else
    if command -v python > /dev/null
    then
        python ./monitorui.py
    fi
fi


