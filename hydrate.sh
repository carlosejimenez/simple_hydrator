#!/usr/bin/env bash

python hydrate.py
while [ $? -eq 111 ]
do
sleep 905
python hydrate.py
done
echo "Completed hydration"
