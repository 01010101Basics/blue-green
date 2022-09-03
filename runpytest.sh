#!/bin/bash
####Creating the Display Port#######
export DISPLAY=:99
echo "The Display is: $DISPLAY"
# Creating the Xvfb desktop ###########
Xvfb :99 -ac -screen 0 1280x1024x24 &
# Run the browser test ################
#python3 -m pytest testsite.py --junit-xml=pytest_unit.xml
python3 testsite.py


