
import os
import sys
import re
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

#set the path that the upload file will store
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#check that if the upload file extension is correct for security consideration
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#Main page
@app.route('/')
def index():
    return "Hello, World!"

#curl -F "file=@/home/wenyan/Documents/d.png" http://127.0.0.1:5000/uploads
#curl -F "file=@/home/usrname/Documents/image.png" http://localhost:5000/uploads
@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    os.system('python database_connect.py')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            global filename, output
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',filename=filename))
            #file.save(os.path.join(UPLOAD_FOLDER,file.filename))
            #return '<p>success</p>'
            recognise = os.popen('python predict_deep.py '+app.config['UPLOAD_FOLDER']+filename) # return file
            output = recognise.read()
            recognise.close()
            predict=re.findall(r"\d+\.?\d*",output)
            os.system('python database_connect.py '+filename+' '+predict[0])
            return output
        return '<p> You uploaded an impermissible file type </p>' #redirect to preview page
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

#view the file user uploaded
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#record data and store into the database (cassandra) time, image_name, predict_number
@app.route('/uploads/record')
def data_record():
    predict=re.findall(r"\d+\.?\d*",output)
    os.system('python database_connect.py '+filename+' '+predict[0])
    return "data stored"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
    #app.run()
