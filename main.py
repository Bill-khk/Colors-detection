import os

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
bootstrap = Bootstrap5(app)


class uploadIMGForm(FlaskForm):
    photo = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = uploadIMGForm()
    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)  # Secure the filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # Save the file
        file.close()
        file_url = url_for('static', filename=f'uploads/{filename}')
        # Get the colors
        colors = get_color(f'./{file_url}')
        print(colors)
        return render_template('index.html', form=form, image=file_url, colors=colors)
    return render_template('index.html', form=form)


def get_color(image_url):
    img = Image.open(image_url)
    img_array = np.array(img)
    reshaped_array = img_array.reshape(-1, 3)
    model = KMeans(n_clusters=10, random_state=42).fit(reshaped_array)
    colour_palette = np.uint8(model.cluster_centers_) # Get centroid from the model
    # Display the color palette as an image
    # plt.imshow([colour_palette])
    # plt.show()
    return colour_palette

if __name__ == "__main__":
    app.run()
