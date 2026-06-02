from app import create_app, db
from app.models.moto import Motocicleta
from app.models.marca import Marca
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.tipo_documento import TipoDocumento
from app.models.rol import Rol
from app.models.factura import Factura
from app.models.detalle_factura import DetalleFactura
from app.models.metodo_pago import MetodoPago
from app.models.entrega import Entrega

app = create_app('default')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Conexion exitosa - tablas listas')
    app.run(debug=True)
