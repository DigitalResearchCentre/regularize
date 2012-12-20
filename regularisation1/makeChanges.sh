#!/bin/bash

cd regularisation1
file="settings.py"
sed -i.bak 's/postgresql.psycopg2/mysql/' $file
sed -i.bak 's/regularize/drc/' $file 
sed -i.bak 's/drc1/50me_pa55w0rd/' $file 
sed -i.bak 's/\/tmp\///' $file
sed -i.bak 's/Users\/erin\/Documents\/DRC\/JSONCR/var\/www\/apps\/regularize/' $file
rm -rf *.bak

cd ../jsRegularize
viewFile="views.py"
sed -i.bak 's/127.0.0.1:8080\/collatex-web-0.9.1-RC2/gregor.middell.net\/collatex/g' $viewFile
rm -rf *.bak

cd ../templates/jsRegularize
textsFile="chooseTexts_interface.html"
rulesFile="chooseRuleSets_interface.html"
collateFile="collate_interface.html"
sed -i.bak 's/127.0.0.1:8000/textualcommunities.usask.ca\/regularize/g' $textsFile $rulesFile $collateFile
rm -rf *.bak
