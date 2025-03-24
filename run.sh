  GNU nano 7.2                                                            matchminer/runner/run.sh                                                                      
#!/bin/bash

nohup python3 manage.py shell <  crawler/main.py > one.log 2>&1 &

nohup python3 manage.py shell <  crawler/main2.py > tow.log 2>&1 &

nohup python3 manage.py shell <  crawler/main3.py > tree.log 2>&1 &
echo "All scripts are running in background."



