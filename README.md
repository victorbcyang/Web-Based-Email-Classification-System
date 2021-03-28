# Web-Based-Email-Classification-System
This a Web Base Email Classification System.
In the main interface, user can upload file (single raw text file, or a .tgz file with multiple files) for classification.
Users can also register, login, and change password. 
If a user is logged in, the user's information (entered when registering) will show on the main interface, and the user can also uploade file for classification.
The classification model is pre-trained by 20 newsgroup dataset.
## How to install
This system runs on top of Python and Flask.
To use the repo, do the following steps.
1. Clone the repo by
```
git clone https://github.com/victorbcyang/Web-Based-Email-Classification-System.git
```
2. Check the Python version by
```
python --version
```
If the output shows ```Python 2.x.x```, follow the [link](https://www.python.org/downloads/) to install Python 3.

3. Activate the virtual environment under the cloned directory.
Change the directory to ```Web-Based-Email-Classification-System```
```
cd Web-Based-Email-Classification-System
```
​Activate the virtual environment
On Max/Linux:
```
$ . venv/bin/activate
```
On Windows:
```
> venv\Scripts\activate
```
4. Install the required packages by 
```
pip install -r requirements.txt
```
This includes installing Flask.
## Run the application
After activating the virtual environment and installing the required packages, you can run the application using ````flask``` command.
The command should be run in the ```Web-Based-Email-Classification-System``` directory, not in ```webapp``` package.
For Mac/Linux:
```
$ export FLASK_APP=webapp
$ exprot FLASK_ENV=development
$ flask run
```
For Windows cmd:
```
> set FLASK_APP=webapp
> set FLASK_ENV=development
> flask run
```
For Windows PowerShell, use ```$env:``` instead of ```export```:
```
> $env:FLASK_APP = "webapp"
> $env:FLASK_ENV = "development"
> flask run
```
Then you can see the output similar to the following:
```
 * Serving Flask app "webapp" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 286-706-937
```
Visit http://127.0.0.1:5000 in a browser and you should see the main interface of the web site. To quit, press ```CTRL+C``` in terminal.