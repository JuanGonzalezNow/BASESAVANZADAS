from app import create_app, db
from app.models.moto import Motocicleta

app = create_app('default')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Conexión exitosa — tablas listas")
    app.run(debug=True)