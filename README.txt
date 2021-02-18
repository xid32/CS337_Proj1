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
create a "files" directory under CS337_Proj1 and put json files (corpus) into this "files" directory


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
How to run our code:

1.
	No need to run preceremony, since gg_api calls preceromony.
	Just run gg_api.py like the following and the gg[year]results.json file will be generated in the current directory.

	$ python3 gg_api.py 20XX

	NOTE: Please input the years separately, because there are some global variables in the 'get_nominees' part. For example, 
	$ python3 gg_api.py 2013 
	$ python3 gg_api.py 2015


2.
	After running gg_api.py: 
	The Json file with format required on Canvas will be stored as gg[year]formated_results.json in the current directory.


3. 
	Then you can run the autograder.py, the methods in gg_api will read the json files: gg[year]results.json generated above
	$ python3 autograder.py

4. 
	You can see the results of our addictional goals by running the following. 
	It requires gg[year]results.json, because it needs the hosts name.
	$ python3 additional_goals.py year

5.
	Finally, if you want to see the human-readable output, do:
	$ python3 human_readable_output.py year

6. In summary:
	1. The json files with required format are in gg[year]formated_results.json
	2. The required human-readable output can be view by doing: 
		python3 human_readable_output.py year



