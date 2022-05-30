import os
from flask import Flask, render_template, request, flash
import uuid
import img_handle
import query
import CNN
from threading import Thread

app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'data', 'user')
app.config['VEHICLE_FOLDER'] = os.path.join('static', 'data', 'vehicles')
app.config['NON_VEHICLE_FOLDER'] = os.path.join('static', 'data', 'non-vehicles')
app.config['LOGO'] = os.path.join('static', 'logo.png')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=('GET', 'POST'))
def index():  # put application's code here
    img_ids = dict2list(query.get_all_img_ids())
    unconfirmed_ids = dict2list(query.get_all_unconfirmed_img_ids())
    if request.method == 'POST':
        if request.form['button'] == 'Upload':
            image = request.files['image']
            upload(image)
            img_ids = dict2list(query.get_all_img_ids())
            unconfirmed_ids = dict2list(query.get_all_unconfirmed_img_ids())
            return render_template('index.html', path=app.config['LOGO'], imageNames=img_ids,
                                   imageNameNotConfirmed=unconfirmed_ids,
                                   data=query.get_table_data(), accuracy=query.get_accuracy())
        if request.form['button'] == 'View' or request.form['button'] == 'View Result':
            image_id = request.form['selected_image']
            if image_id == 'None':
                flash('No image selected')
            else:
                image_name = query.get_name_by_id(image_id)
                path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                if request.form['button'] == 'View Result':
                    info = query.get_image_by_name(image_name)
                    result = info[0]['is_vehicle']
                    flash('Not vehicle' if result == 0 else 'Vehicle')
                return render_template('index.html', path=path, imageNames=img_ids,
                                       imageNameNotConfirmed=unconfirmed_ids, data=query.get_table_data(),
                                       accuracy=query.get_accuracy())
        if request.form['button'] == 'Predict':
            image_id = request.form['selected_image']
            image_name = query.get_name_by_id(image_id)
            if image_name == 'None':
                flash('No image selected')
            else:
                result, path = predict(image_name)
                flash(result)
                unconfirmed_ids = dict2list(query.get_all_unconfirmed_img_ids())
                return render_template('index.html', path=path, imageNames=img_ids,
                                       imageNameNotConfirmed=unconfirmed_ids, data=query.get_table_data(),
                                       accuracy=query.get_accuracy())

        if request.form['button'] == 'Correct' or request.form['button'] == 'Incorrect':
            correct = True if request.form['button'] == 'Correct' else False
            image_id = request.form['selected_image']
            if image_id == 'None':
                flash('No image selected')
            else:
                image_name = query.get_name_by_id(image_id)
                result = query.check_predicted(image_name)
                # new_path = ''
                if (correct == 1 and result == 1) or (correct == 0 and result == 0):
                    img_handle.move_img(image_name, app.config['UPLOAD_FOLDER'], app.config['VEHICLE_FOLDER'])
                    new_path = os.path.join(app.config['VEHICLE_FOLDER'], image_name)
                else:
                    img_handle.move_img(image_name, app.config['UPLOAD_FOLDER'], app.config['NON_VEHICLE_FOLDER'])
                    new_path = os.path.join(app.config['NON_VEHICLE_FOLDER'], image_name)
                query.update_image_by_name(image_name, path=new_path, is_confirmed=True, correct=correct)
                unconfirmed_ids = dict2list(query.get_all_unconfirmed_img_ids())
                return render_template('index.html', path=app.config['LOGO'], imageNames=img_ids,
                                       imageNameNotConfirmed=unconfirmed_ids, data=query.get_table_data(),
                                       accuracy=query.get_accuracy())
        if request.form['button'] == 'Train':
            if query.get_training_status():
                flash('Model already under training!')
            else:
                train_thread = Thread(target=CNN.train_model)
                train_thread.start()
                flash('Training started')
    return render_template('index.html', path=app.config['LOGO'], imageNames=img_ids,
                           imageNameNotConfirmed=unconfirmed_ids,
                           data=query.get_table_data(), accuracy=query.get_accuracy())


def dict2list(d):
    return [item['id'] for item in d]


def upload(image):
    name = f'user_img_{uuid.uuid4()}.png'
    img_handle.save_img(image, app.config['UPLOAD_FOLDER'], name)
    path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    query.save_img(name, path)


def predict(image_name):
    predicted = query.check_predicted(image_name)
    path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if predicted:
        return 'vehicle' if predicted == 1 else 'not vehicle', path
    image = img_handle.get_img(path)
    result = CNN.predict(image)
    if result == 'vehicle':
        query.update_image_by_name(image_name, path, is_vehicle=True)
    else:
        query.update_image_by_name(image_name, path, is_vehicle=False)
    return result, path


if __name__ == '__main__':
    app.run()
