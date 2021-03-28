# Web-Based-Email-Classification-System
This a Web Base Email Classification System.
In the main interface, user can upload file (single raw text file, or a .tgz file with multiple files) for classification.
Users can also register, login, and change password. 
If a user is logged in, the user's information (entered when registering) will show on the main interface, and the user can also uploade file for classification.
The classification model is pre-trained by 20 newsgroup dataset.
## How to install
This system runs on top of Python and Flask.
To use the repo, do the following steps. The following instruction is referred from [Flask document](https://flask.palletsprojects.com/en/1.1.x/)
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
Activate the virtual environment
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
Visit http://127.0.0.1:5000 in a browser and you should see the main interface of the web site. Then you can now uploade file for classification. To quit, press ```CTRL+C``` in terminal.
## How to test coverage
### To run the tests, use ```pytest``` command. It will find and run the test functions in ```tests```.
```
$ pytest
======================================= test session starts =======================================
platform darwin -- Python 3.7.4, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
rootdir: /Users/victoryang/Singularity_Webproj/Web-Based-Email-Classification-System, configfile: setup.cfg, testpaths: tests
collected 19 items                                                                                

tests/test_auth.py ...............                                                          [ 78%]
tests/test_db.py ..                                                                         [ 89%]
tests/test_factory.py ..                                                                    [100%]

======================================= 19 passed in 1.18s ========================================
```
If any test fail, the ouput will show the error. You can also run ```pytest -v``` to get a list of each tested functions
```
$ pytest -v
============================================================= test session starts ==============================================================
platform darwin -- Python 3.7.4, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /Users/victoryang/Singularity_Webproj/Web-Based-Email-Classification-System/venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/victoryang/Singularity_Webproj/Web-Based-Email-Classification-System, configfile: setup.cfg, testpaths: tests
collected 19 items                                                                                                                             

tests/test_auth.py::test_register PASSED                                                                                                 [  5%]
tests/test_auth.py::test_register_validate_input[---------Username is required.] PASSED                                                  [ 10%]
tests/test_auth.py::test_register_validate_input[a---------Password is required.] PASSED                                                 [ 15%]
tests/test_auth.py::test_register_validate_input[a-a--------Email is required.] PASSED                                                   [ 21%]
tests/test_auth.py::test_register_validate_input[a-a-hello@jjj.com-------Phone is required.] PASSED                                      [ 26%]
tests/test_auth.py::test_register_validate_input[a-a-hello@jjj.com-752-896-147------First Name is required.] PASSED                      [ 31%]
tests/test_auth.py::test_register_validate_input[a-a-hello@jjj.com-752-896-147-Happy-----Middle Name is required.] PASSED                [ 36%]
tests/test_auth.py::test_register_validate_input[a-a-hello@jjj.com-752-896-147-Happy-H.----Last Name is required.] PASSED                [ 42%]
tests/test_auth.py::test_register_validate_input[a-a-hello@jjj.com-752-896-147-Happy-H.-Chen---Address is required.] PASSED              [ 47%]
tests/test_auth.py::test_register_validate_input[a-a-hello@jjj.com-752-896-147-Happy-H.-Chen-888 S Hope--Occupation is required.] PASSED [ 52%]
tests/test_auth.py::test_register_validate_input[test-test-cdf@yahoo.com-456-789-963-Name-M.-Last-10980 Wellworth Ave, Los Angeles, CA 90024-CEO-already registered] PASSED [ 57%]
tests/test_auth.py::test_login PASSED                                                                                                    [ 63%]
tests/test_auth.py::test_login_validate_input[a-test-Incorrect username.] PASSED                                                         [ 68%]
tests/test_auth.py::test_login_validate_input[test-a-Incorrect password.] PASSED                                                         [ 73%]
tests/test_auth.py::test_logout PASSED                                                                                                   [ 78%]
tests/test_db.py::test_get_clos_db PASSED                                                                                                [ 84%]
tests/test_db.py::test_init_db_commant PASSED                                                                                            [ 89%]
tests/test_factory.py::test_config PASSED                                                                                                [ 94%]
tests/test_factory.py::test_hello PASSED                                                                                                 [100%]

============================================================== 19 passed in 1.40s ==============================================================
```
#### To measure the code coverage, use ```coverage``` command to run pytest
```
$ coverage run -m pytest
```
Then, use ```coverage report``` to view simple coverage report in the terminal
```
$ coverage report
Name                       Stmts   Miss Branch BrPart  Cover
------------------------------------------------------------
webapp/__init__.py            23      0      2      0   100%
webapp/auth.py                93     21     44      0    77%
webapp/db.py                  24      0      4      0   100%
webapp/main_interface.py      57     35     14      1    32%
------------------------------------------------------------
TOTAL                        197     56     64      1    70%
```
## Deploy to production
To deploy the application elsewhere, building a distribution file is needed. The current standatd for Python distribution is the wheel format, with the ```.whl``` extension.
The wheel library is installed by ```pip install wheel```, make sure the library is installed.
1. Run ```setup.py``` with ```bdist_wheel```
```
$ python setup.py bdist_wheel
```
Then you can find the file in ```dist/webapp-1.0.0-py3-none-any.whl```.
2. Copy this file to another machine, setup a virtual environment by
```
$ python3 -m venv venv
$ . venv/bin/activate
```
3. Install the file with ```pip```
```
$ pip install webapp-1.0.0-py3-none-any.whl
```
```pip``` will install the project along with its dependencies.
4. Run ```init-db``` under the directory of ```venv/lib/python3.7/site-packages``` to initialize database and to create the database in the instance folder
```
$ cd venv/lib/python3.7/site-packages
$ export FLASK_APP=webapp
$ flask init-db
```
5. Configure the secret key
```
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
```
Create the ```config.py``` file in the instance folder, and copy the generated value to it
```
$ cd venv/var/webapp-instance
$ touch config.py
```
and copy the generated value to it
```python
SERCET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
```
6. Run with a production server
When running publicly, you should not use the built-in development server (```flask run```). Instead, use a production WSGI server.
For example, to use [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/), first install it in the virtual environment:
```
$ pip install waitress
```
Tell waitress to import and call the application factory to get an application object.
```
$ waitress-server --call 'webapp:create_app'
Serving on http://0.0.0.0:8080
```