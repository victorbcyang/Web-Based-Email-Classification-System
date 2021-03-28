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
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
tfidf_T = pickle.load(open('tfidf.pkl', 'rb'))
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
        # f.save(os.path.join('webapp/uploded_files', secure_filename(f.filename)))
        # test_data = open(os.path.join('webapp/uploded_files', secure_filename(f.filename)), 'r')
        error = None
        if not f:
            error = 'Please Select file for classificaion!'
            flash(error)
            return redirect(url_for('index'))

        else:
            # print(type(test_data))
            if 'tgz' in f.filename:
                # if the uploaded file is a zip file
                # need to save the uploaded file and extract it for usage
                userpath = os.path.join('webapp/uploded_files', g.user['username'])
                if not os.path.isdir(userpath):
                    os.mkdir(userpath)

                f.save(os.path.join(userpath, f.filename))
                tgz_file_path = os.path.join(userpath, f.filename)
                ext_file = tarfile.open(tgz_file_path)
                ext_file.extractall(userpath)
                test_path = os.path.join(userpath, 'data/test')             # 'webapp/uploded_files/data/test'
                test_data = datasets.load_files(test_path, encoding='latin-1')
                X_test = vectorizer.transform(test_data.data)
                X_test_tfidf = tfidf_T.transform(X_test)
                y_test = test_data.target
                y_pred = model.predict(X_test_tfidf)
                result = classification_report(y_test, y_pred, target_names=test_data.target_names)
                if g.user:
                    return render_template("main_interface/index_user.html", Result=result)
                else:
                    return render_template('main_interface/index.html', Result=result)
            else:
                test_data = f.read()
                trans_list = []
                # trans_list.append(test_data.read())
                trans_list.append(test_data)
                test_file = vectorizer.transform(trans_list)
                test_feature = tfidf_T.transform(test_file)
                prediction = model.predict(test_feature)
        
                if g.user:
                    return render_template("main_interface/index_user.html", Predict_label='The category of this email is {}'.format(label_name[int(prediction)]))
                else:
                    return render_template('main_interface/index.html', Predict_label='The category of this email is {}'.format(label_name[int(prediction)])) 
        