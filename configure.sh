#!/bin/bash

DOWNJUSTFORME_HOME="/home/xxx/srv_xxx/downjustforme/"
cd $DOWNJUSTFORME_HOME
rm -Rf downjustforme.env
virtualenv downjustforme.env
source downjustforme.env/bin/activate

pip install -r requirements.txt
sudo apt-get install firefox
sudo apt-get install xvfb
sudo apt-get install libasound2

python -c "from downjustforme.dependencies.checkdependencies import CheckDependencies; check_dependecies = CheckDependencies(); check_dependecies.run()"

echo "done"
