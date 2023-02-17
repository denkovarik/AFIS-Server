# This is a bash script that downloads and extracts the datasets

git clone git@bitbucket.org:afis-system/afis-datasets.git

mv afis-datasets/Datasets.tgz ../Datasets.tgz

rm -rf afis-datasets/

cd ../

tar xzvf Datasets.tgz

rm Datasets.tgz

cd setup/
