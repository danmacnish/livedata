#! /bin/bash
echo installing modified OWSLib
cd OWSLib-modified
sudo python setup.py install
echo installing dependencies
sudo pip install pyfirmata
echo done