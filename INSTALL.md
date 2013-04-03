INSTALLATION GUIDE

This guide comes with no warrenty or assurance of correctness.  It's mostly meant as a guideline.
Your milage may vary.


__install gcc__
Distro-dependent

__install cmake__
Distro-dependent

__install python's protobuf (google)__
python -m easy_install protobuff

__install flask__
python -m easy_install flask



These next two need to be from the repos for now, as the patches havent been pushed out yet

__install libgit2__
 git clone git://github.com/libgit2/libgit2.git
 follow cmake instructions 
(you must remove old version of libgit2 and it's devel headers)

__install pygit2__
git clone https://github.com/libgit2/pygit2.git ./pygit2
sudo python setup.py install

__install github (python)__ - going to be depricated
python -m easy_install pygithub

__Groundstation setup__
Odds are good if you're reading this, you've already done the following, but incase you're viewing this via a browser:
git clone https://github.com/richo/groundstation ./groundstation

cd groundstation

python stationd
