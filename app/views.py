from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.utils import secure_filename
import os
import torch
from PIL import Image
import torchvision as tv
import torch.nn.functional as F
import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# get the directory containing this script
main_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(main_dir, "static", "uploads")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# db = SQLAlchemy(app)
mysql = MySQL(app)
files_to_predict = []


def read_sql_file(filename):
    with app.open_resource(filename, mode='r') as f:
        sql = f.read()
    return sql


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results')
def works():
    return render_template('history.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():

    # Launch upload
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    msg = ''
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("upload réussi")
            cur.execute("INSERT INTO mednet.images (fileName) VALUES (%s)", [
                        file.filename])
            mysql.connection.commit()
            cur.close()
            print('File successfully uploaded ' +
                  file.filename + ' to the database!')
            files_to_predict.append(filename)
        else:
            print('Invalid Uplaod only png, jpg, jpeg, webp')
        msg = 'Success Upload'
    return jsonify(msg)


@app.route('/predict', methods=['POST'])
def predict():
    predictions_list = []
    model = torch.load('app/static/model/saved_model.pt',
                       map_location=torch.device('cpu'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    for file in files_to_predict:

        # Load, open and transform in tensor
        path = 'app/static/uploads/' + file
        img_scaled = scaleImage(Image.open(path).resize((64, 64)))
        image_tensor = torch.stack([img_scaled])

        # If image is not grayscale
        if image_tensor.shape[1] != 1:
            gray = 0.299 * image_tensor[:, 0, :, :] + 0.587 * \
                image_tensor[:, 1, :, :] + 0.114 * image_tensor[:, 2, :, :]
            image_tensor = gray.unsqueeze(0)
            print("Image Tensor Shape : ", image_tensor.shape)

        # Make a prediction
        logits = model(image_tensor)
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1)

        # Map the predicted class index to the corresponding class name
        class_names = ['AbdomenCT', 'BreastMRI',
                       'ChestCT', 'CXR', 'Hand', 'HeadCT']
        predicted_class_name = class_names[predicted_class.item()]
        print('Predicted class:', predicted_class_name)
        predictions_list.append(predicted_class_name)
        files_tmp = files_to_predict.copy()
        # Save label in database
        cur.execute("UPDATE mednet.images SET date = %s, label = %s WHERE fileName = %s", [
            datetime.datetime.now(), predicted_class_name, file])
        mysql.connection.commit()

    cur.close()
    # Return the prediction as JSON
    files_to_predict.clear()
    return jsonify({'predictions': predictions_list, 'files': files_tmp})


def scaleImage(x):
    toTensor = tv.transforms.ToTensor()
    y = toTensor(x)
    # Assuming the image isn't empty, rescale so its values run from 0 to 1
    if (y.min() < y.max()):
        y = (y - y.min())/(y.max() - y.min())
    # Subtract the mean value of the image
    z = y - y.mean()
    return z


@app.route('/history', methods=['POST'])
def history():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(
        "SELECT * FROM mednet.images WHERE `label` != 'NULL' ORDER BY date desc LIMIT 10")
    images = cur.fetchall()
    cur.close()
    print(images)
    return jsonify({'images': images, 'path': os.path.dirname(os.path.abspath(__file__))})
