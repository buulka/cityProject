from app import app

app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///city4.db'
app.config['SQLALCHEMY_TRASK_MODIFICATIONS'] = False