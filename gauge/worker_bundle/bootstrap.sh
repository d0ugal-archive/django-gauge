export PIP_USE_MIRRORS=true;
export PIP_FIND_LINKS="http://pypi.python.org http://d.pypi.python.org";
sudo apt-get install python-dev python-setuptools git-core -y -q;
echo "installing pip";
sudo easy_install pip;
echo "pip installed";
sudo pip install -q -r ~/gauge/requirements.txt;
