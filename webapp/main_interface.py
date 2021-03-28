import os
import io
import sys
import pickle
import tarfile
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, current_app)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from webapp.auth import login_required
from webapp.db import get_db
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report

bp = Blueprint('interface', __name__)

# load the pre-trained classifier model
model = pickle.load(open('webapp/model.pkl', 'rb'))
# load the pre-fitted stopword remove vectorizer
vectorizer = pickle.load(open('webapp/vectorizer.pkl', 'rb'))
# load the pre-fitted tfidf transform
tfidf_T = pickle.load(open('webapp/tfidf.pkl', 'rb'))
# the list of categories name
label_name = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', \
              'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', \
              'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',\
              'sci.electronics', 'sci.med', 'sci.space', 'soc.religion.christian', \
              'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']


@bp.route('/', methods=('GET', 'POST'))
def index():
    if g.user:
        # if logged in user, return the interface with user information
        return render_template('main_interface/index_user.html')
    else:
        # if no user logged in, just return the interface
        return render_template('main_interface/index.html')


@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        error = None
        if not f:
            # check if a file is select for classification
            error = 'Please select file for classificaion!'
            # show the error if no file selected
            flash(error)
            return redirect(url_for('index'))

        else:
            # print(type(test_data))
            if 'tgz' in f.filename:
                # if the uploaded file is a zip file
                # need to save the uploaded file and extract it for usage
                userpath = os.path.join('webapp/uploded_files', g.user['username'])
                # create path for storing user's uploaded file
                # the uploaded file will be stored at 'uploaded_files/username'
                if not os.path.isdir(userpath):
                    os.mkdir(userpath)
                # save the file for further usage
                f.save(os.path.join(userpath, f.filename))
                tgz_file_path = os.path.join(userpath, f.filename)              # indicate the directory of the stored uploaded file 
                ext_file = tarfile.open(tgz_file_path)                          # extract file by tarfile
                ext_file.extractall(userpath)                                   # extract file by tarfile
                test_path = os.path.join(userpath, 'data/test')                 # specify the path of testing data: 'webapp/uploded_files/username/data/test'
                test_data = datasets.load_files(test_path, encoding='latin-1')  # specify the test data using sklearn dataloader
                X_test = vectorizer.transform(test_data.data)                   # remove stopword by the pre-fitted vectorizer in the previous MLproj
                X_test_tfidf = tfidf_T.transform(X_test)                        # perform TF-IDF transform by the pre-fitted tfidt transform
                y_test = test_data.target                                       # specify the label of testing data
                y_pred = model.predict(X_test_tfidf)                            # predict the label by the pre-trained model in the previous MLproj
                # print the classification result for showing on the interface
                result = classification_report(y_test, y_pred, target_names=test_data.target_names)

                if g.user:
                    return render_template("main_interface/index_user.html", Result=result)
                else:
                    return render_template('main_interface/index.html', Result=result)
            else:
                test_data = f.read()
                trans_list = []
                trans_list.append(test_data)
                test_file = vectorizer.transform(trans_list)        # remove stopword by the pre-fitted vectorizer in the previous MLproj
                test_feature = tfidf_T.transform(test_file)         # perform TF-IDF transform by the pre-fitted tfidt transform
                prediction = model.predict(test_feature)            # predict the label by the pre-trained model in the previous MLproj
                # the prediction output is a index, needed to specify which category by checking the label_name list
                if g.user:
                    return render_template("main_interface/index_user.html", Predict_label='The category of this email is {}'.format(label_name[int(prediction)]))
                else:
                    return render_template('main_interface/index.html', Predict_label='The category of this email is {}'.format(label_name[int(prediction)])) 
        