GitHub link:
https://github.com/xid32/CS337_Proj1

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
First, cd into this directory
Your pwd should be something like this: 

$ /.../.../CS337_Proj1/

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
How to set up: (I am using Python 3.7.4)

1.
$ python3 -m venv virtualenv

2.
$ source virtualenv/bin/activate

3. Note: This command only needs to be run once
$ pip install -r requirements.txt

4.
$ python3 downloader.py

5.
put autograder.py, gg[year]answers.json into the current directory

6.
create a "files" directory under CS337_Proj1 and put json files into this "files" directory


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
How to run our code

$ python3 gg_api.py 20XX

NOTE: Please input the years separately, because there are some global variables in the 'get_nominees' part. For example, 
$ python3 gg_api.py 2013 
$ python3 gg_api.py 2015

Then when you run autograder, gg_api will read the json files generated above
$ python3 autograder.py

You can see the results of our addictional goals by running:
$ python3 additional_goals.py



