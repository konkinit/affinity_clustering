wget https://nrvis.com/download/data/rec/rec-epinions.zip -P ./data/inputs

unzip ./data/inputs/rec-epinions.zip -d ./data/inputs

rm ./data/inputs/rec-epinions.zip

python ./src/transform-network-data.py

rm ./data/inputs/rec-epinions.edges

rm ./data/inputs/readme.html
