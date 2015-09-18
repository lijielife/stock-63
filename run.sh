#!/usr/bin/bash

#export LANG=ja_JP.utf8
source /home/vagrant/.bash_profile
source /home/vagrant/.bashrc
source /home/vagrant/py27/bin/activate

date >> /stock/stock.log

#/home/vagrant/py27/bin/activate.csh

dt=$(date '+%Y%m%d') 
folder=$(echo "/stock/`date '+%Y%m%d'`")

if [ -e $folder ]; then
    # 存在する場合
    #cd $folder
    :
else
    # 存在しない場合
    mkdir $folder
    #cd $folder
    mkdir $folder/all
    mkdir $folder/high
    mkdir $folder/depreciation
    mkdir $folder/rise
    mkdir $folder/fall
    mkdir $folder/golden
    mkdir $folder/dead
fi

cd /stock/src

#env > $folder/run.log
which python > $folder/run.log
#env |grep LANG >> $folder/run.log
echo -n "start:" >> $folder/run.log
date >> $folder/run.log
#/home/vagrant/py27/bin/python /stock/src/print.py >> $folder/run.log
#/home/vagrant/py27/bin/python /stock/src/cron.py -o $folder/high -u 0 >> $folder/run.log


python /stock/src/cron.py -o $folder/high -u 0 >> $folder/run.log
mv /stock/src/collection_url.txt $folder/high/high$dt.txt
python /stock/src/cron.py -o $folder/depreciation -u 1 >> $folder/run.log
mv /stock/src/collection_url.txt $folder/depreciation/depreciation$dt.txt
python /stock/src/cron.py -o $folder/rise -u 2 >> $folder/run.log
mv /stock/src/collection_url.txt $folder/rise/rise$dt.txt
python /stock/src/cron.py -o $folder/fall -u 3 >> $folder/run.log
mv /stock/src/collection_url.txt $folder/fall/fall$dt.txt
python /stock/src/cron.py -o $folder/golden -u 4 >> $folder/run.log
mv /stock/src/collection_url.txt $folder/golden/golden$dt.txt
python /stock/src/cron.py -o $folder/dead -u 5 >> $folder/run.log
mv /stock/src/collection_url.txt $folder/dead/dead$dt.txt

python /stock/src/allchart.py -o $folder/all -u 0 >> $folder/run.log
cp /stock/src/codelist.txt $folder/all/all$dt.txt

echo -n "end:" >> $folder/run.log
date >> $folder/run.log

