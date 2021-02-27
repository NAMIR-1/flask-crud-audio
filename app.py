from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test3.db'
db = SQLAlchemy(app)


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer)
    host = db.Column(db.String(100))
    participants = db.Column(db.String(1500))
    author = db.Column(db.String(100))
    narrator = db.Column(db.String(100))
    audiotype = db.Column(db.String(50), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file_name = request.form['name']
        duration = request.form['duration']
        host = request.form['host']
        participants = request.form['participants']
        author = request.form['author']
        narrator = request.form['narrator']

        audiotype = request.form['audiotype']
        if audiotype == 'song':
            new_file = Files(name=file_name, audiotype=audiotype, duration=duration)
        elif audiotype == 'audiobook':
            new_file = Files(name=file_name, audiotype=audiotype, duration=duration, author=author, narrator=narrator)
        elif audiotype == 'podcast':
            new_file = Files(name=file_name, audiotype=audiotype, duration=duration, host=host, participants=participants)
        else:
            redirect('/')


        try:
            db.session.add(new_file)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your file'

    else:
        files = Files.query.order_by(Files.date_updated).all()
        return render_template('index.html', files=files)




@app.route('/delete/<int:id>')
def delete(id):
    file_to_delete = Files.query.filter_by(id=id).first()
    try:
        db.session.delete(file_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that file'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    file = Files.query.get_or_404(id)

    if request.method == 'POST':
        file.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your file'

    else:
        return render_template('update.html', file=file)


if __name__ == "__main__":
    app.run(debug=True)