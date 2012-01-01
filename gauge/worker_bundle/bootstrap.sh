export PIP_USE_MIRRORS=true;
export PIP_FIND_LINKS="http://pypi.python.org b.pypi.python.org c.pypi.python.org d.pypi.python.org e.pypi.python.org f.pypi.python.org";
sudo apt-get install python-dev python-setuptools git-core mercurial -y -q;
sudo curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python;
sudo pip install -q -r ~/gauge/requirements.txt;


