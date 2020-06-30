These instructions have been tested on a mac and linux environment using python 3. You may have to do things slightly different on a Windows machine.

0. Optional but recommended: Create a python virtual environment using "python -m venv myenv" and activate it using "source myenv/bin/activate"
1. Installation: Run "pip install -r requirements.txt" to get all the dependencies. 
2. Input your Twitter API consumer token and secret into the first few lines of the script. 
3. Run "python tweet_hydration.py <tweet_list.csv> <output_file>".
