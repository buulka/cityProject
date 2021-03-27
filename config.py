from app import app

app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///city6.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
