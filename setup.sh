mkdir storage
mkdir storage/snapshots
mkdir storage/highlights
mkdir storage/masks

pip3 install -r requirements.txt

# wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
# tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2
# sudo cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/
# rm -r phantomjs-2.1.1-linux-x86_64
# rm phantomjs-2.1.1-linux-x86_64.tar.bz2

wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -zxvf geckodriver-v0.19.1-linux64.tar.gz
rm geckodriver-v0.19.1-linux64.tar.gz
sudo mv geckodriver /usr/bin/geckodriver