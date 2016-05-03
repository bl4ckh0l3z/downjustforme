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
sudo apt-get install logrotate

logrotate_conf="/etc/logrotate.d/$(pwd | rev | cut -d"/" -f1-2 | rev | tr '/' '_')"
if [ ! -e $logrotate_conf ];then
    echo "- Configuring logrotate..."
    sudo echo $DOWNJUSTFORME_HOME"logs/*.log {
    missingok
    rotate 2
    size 20M
    compress
}" > $logrotate_conf
else
    echo "- Logrotate is already configured..."
fi

python -c "from downjustforme.dependencies.checkdependencies import CheckDependencies; check_dependecies = CheckDependencies(); check_dependecies.run()"

echo "Done"
