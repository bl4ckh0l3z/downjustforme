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

already_configured=$(grep -c $DOWNJUSTFORME_HOME /etc/logrotate.conf)
if [ "$already_configured" -eq "0" ];then
    echo "Configuring logrotate..."
    sudo echo $DOWNJUSTFORME_HOME"logs {
    missingok
    rotate 2
    size 20M
    compress
}" >> /etc/logrotate.conf
else
    echo "Logrotate is already configured..."
fi

python -c "from downjustforme.dependencies.checkdependencies import CheckDependencies; check_dependecies = CheckDependencies(); check_dependecies.run()"

echo "done"
