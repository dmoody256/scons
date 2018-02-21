#!/usr/bin/env bash
set -x

sudo pip install coverage
sudo pip install coveralls

# attempt to get a location where we can store the usercustomize.py file
python -m site
export PYSITEDIR=$(python -m site --user-site)
sudo mkdir -p $PYSITEDIR
sudo touch ${PYSITEDIR}/usercustomize.py
        
write the usercustomize.py file so all python processes use coverage and know where the config file is
echo "import os" | sudo tee --append ${PYSITEDIR}/usercustomize.py
echo "os.environ['COVERAGE_PROCESS_START'] = '$PWD/.coveragerc'" | sudo tee --append ${PYSITEDIR}/usercustomize.py
echo "import coverage" | sudo tee --append ${PYSITEDIR}/usercustomize.py
echo "coverage.process_startup()" | sudo tee --append ${PYSITEDIR}/usercustomize.py

