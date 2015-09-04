#!/bin/bash

python chart.py -o /vagrant/stock/high -u 0
python chart.py -o /vagrant/stock/depreciation -u 1
python chart.py -o /vagrant/stock/rise -u 2
python chart.py -o /vagrant/stock/fall -u 3
cd /vagrant/stock
zip -r /vagrant/stock.zip ./*

