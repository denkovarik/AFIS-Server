apt-get install wget
./setupPython.sh

pip3 install -r ../source/pythonScripts/requirements.txt
pip3 install wsq
#pip3.8 install tensorflow
#pip3.8 install keras

# Extract Datasets
./setupDatasets.sh

# Change permissions (May not be an issue for you but was on Google Server)
chmod a+r ../
chmod a+w ../
chmod a+r ../runFingerprintID.php
chmod a+w ../runFingerprintID.php

chmod a+r ../Datasets/
chmod a+w ../Datasets/
chmod a+r ../Datasets/MOLF/
chmod a+w ../Datasets/MOLF/
chmod a+r ../Datasets/MOLF/MindtctOutput/
chmod a+w ../Datasets/MOLF/MindtctOutput/
chmod a+r ../Datasets/MOLF/MinutiaeOut/
chmod a+w ../Datasets/MOLF/MinutiaeOut/

cd bin/ 
./setupDatabase
chown www-data:www-data ../../uploads/
