from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_casita_tom_2026"

USUARIOS_FILE = "usuarios.txt"

# Bases de Datos Dinámicas en Memoria para Productos y Servicios con tus enlaces reales
PRODUCTOS = [
    {"id": 1, "nombre": "Pack x3 Cuadernos Loro", "precio": 12.00, "imagen": "https://production-tailoy-repo-magento-statics.s3.amazonaws.com/imagenes/872x872/productos/i/c/u/cuaderno-deluxe-80h-cuadriculado-sol-70g-naranja-loro-49540007-default-1.jpg", "categoria": "cuadernos", "destacado": True},
    {"id": 2, "nombre": "Mochila Ergonómica Escolar", "precio": 45.00, "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&auto=format&fit=crop", "categoria": "mochilas", "destacado": True},
    {"id": 3, "nombre": "Caja de Colores x24 Faber-Castell", "precio": 8.00, "imagen": "https://production-tailoy-repo-magento-statics.s3.amazonaws.com/imagenes/872x872/productos/i/c/o/color-acuare-x-24l-fab-367-default-1.jpg", "categoria": "colores", "destacado": True},
    {"id": 4, "nombre": "Cuaderno Anillado A4 Standford", "precio": 6.50, "imagen": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=500&auto=format&fit=crop", "categoria": "cuadernos", "destacado": True},
    {"id": 5, "nombre": "Mochila Juvenil Porta Laptop", "precio": 65.00, "imagen": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=500&auto=format&fit=crop", "categoria": "mochilas", "destacado": True},
    {"id": 6, "nombre": "Plumones Escolares x12 Delgado", "precio": 5.50, "imagen": "https://minisope.vtexassets.com/arquivos/ids/205441-1600-1600?v=638016573638470000&width=1600&height=1600&aspect=true", "categoria": "colores", "destacado": True},
    {"id": 7, "nombre": "Cartucheras", "precio": 15.00, "imagen": "https://danaperu.com/wp-content/uploads/2022/05/cartucheras-publicitarias-dana-peru-1.jpg", "categoria": "utiles", "destacado": True},
    {"id": 8, "nombre": "Tijera Escolar punta roma", "precio": 2.50, "imagen": "https://erp.papeleradeloriente.pe/static/media/imagenes/producto/HVISle0Y1IJeGUTv-zoom.jpg", "categoria": "utiles", "destacado": True},
    {"id": 9, "nombre": "Gomas en Barra Uhu 40g", "precio": 4.00, "imagen": "https://erp.papeleradeloriente.pe/static/media/imagenes/producto/oLQqS4n3vNtOL865-zoom.jpg", "categoria": "gomas", "destacado": True},
    {"id": 10, "nombre": "Regla de Metal 30cm", "precio": 3.00, "imagen": "https://erp.papeleradeloriente.pe/static/media/imagenes/producto/sQGCBGdwACbDwdDn-zoom.jpg", "categoria": "utiles", "destacado": False},
    {"id": 11, "nombre": "Lapiceros Pilot G2", "precio": 10.50, "imagen": "https://erp.papeleradeloriente.pe/static/media/imagenes/producto/psl8ZyPVJDgooOBq-zoom.jpg", "categoria": "utiles", "destacado": False},
    {"id": 12, "nombre": "Corrector en Cinta", "precio": 4.50, "imagen": "https://distribuidoranavarrete.com.pe/wp-content/uploads/1079999.jpg", "categoria": "utiles", "destacado": False},
    {"id": 13, "nombre": "Block de Notas Post-it", "precio": 6.00, "imagen": "https://www.realisaprint.es/actualidad/wp-content/uploads/2023/09/bloc-de-notas1.jpg", "categoria": "utiles", "destacado": False},
    {"id": 14, "nombre": "Calculadora Científica Casio", "precio": 48.00, "imagen": "https://erp.papeleradeloriente.pe/static/media/imagenes/producto/veGi28tFSBquEr5c-zoom.jpg", "categoria": "utiles", "destacado": False}
]

SERVICIOS = [
    {"id": 1, "nombre": "Impresiones Láser A4 (B/N)", "precio": 0.50, "descripcion": "Impresión de alta velocidad para documentos."},
    {"id": 2, "nombre": "Anillado Espiral Doble", "precio": 5.00, "descripcion": "Empastado de cuadernos o monografías."},
    {"id": 3, "nombre": "Plastificado de Carnets", "precio": 3.50, "descripcion": "Protección total brillante para documentos."}
]

def obtener_usuarios():
    usuarios = []
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                linea_limpia = linea.strip()
                if linea_limpia and "," in linea_limpia:
                    u, c = linea_limpia.split(",", 1)
                    usuarios.append({"usuario": u, "contrasena": c})
    return usuarios

def guardar_usuarios(lista_usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        for user in lista_usuarios:
            f.write(f"{user['usuario']},{user['contrasena']}\n")

@app.route("/")
def index():
    query = request.args.get("q", "").strip().lower()
    if query:
        productos_filtrados = [p for p in PRODUCTOS if query in p["nombre"].lower() or query in p["categoria"].lower()]
        busqueda_activa = True
    else:
        productos_filtrados = [p for p in PRODUCTOS if p["destacado"]]
        busqueda_activa = False
    return render_template("index.html", productos=productos_filtrados, servicios=SERVICIOS, query=query, busqueda_activa=busqueda_activa)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        contrasena = request.form["contrasena"].strip()
        usuarios = obtener_usuarios()
        if any(u["usuario"] == usuario for u in usuarios):
            flash("El usuario ya existe", "danger")
            return redirect(url_for("registro"))
        usuarios.append({"usuario": usuario, "contrasena": contrasena})
        guardar_usuarios(usuarios)
        flash("¡Registro exitoso!", "success")
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        contrasena = request.form["contrasena"].strip()
        usuarios = obtener_usuarios()
        
        if usuario == "admin" and contrasena == "admin123":
            session["usuario"] = "Admin" # Nombre que se mostrará
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
            
        for u in usuarios:
            if u["usuario"] == usuario and u["contrasena"] == contrasena:
                session["usuario"] = usuario # Nombre del cliente
                session["is_admin"] = False
                return redirect(url_for("index"))
        flash("Credenciales incorrectas", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Panel administrativo centrado (Dashboard)
@app.route("/admin")
def admin_dashboard():
    if not session.get("usuario") or not session.get("is_admin"):
        flash("Acceso restringido solo para administradores.", "danger")
        return redirect(url_for("login"))
        
    return render_template(
        "admin.html", 
        productos=PRODUCTOS, 
        servicios=SERVICIOS, 
        usuarios=obtener_usuarios(),
        total_productos=len(PRODUCTOS),
        total_servicios=len(SERVICIOS),
        total_usuarios=len(obtener_usuarios())
    )

# CRUD: PRODUCTOS (CREAR, ELIMINAR, EDITAR PRECIO)
@app.route("/admin/producto/crear", methods=["POST"])
def crear_producto():
    nuevo_id = max([p["id"] for p in PRODUCTOS], default=0) + 1
    PRODUCTOS.append({
        "id": nuevo_id,
        "nombre": request.form["nombre"],
        "precio": float(request.form["precio"]),
        "imagen": request.form["imagen"] or "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=500",
        "categoria": request.form["categoria"],
        "destacado": "destacado" in request.form
    })
    flash("Producto creado con éxito", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/producto/eliminar/<int:id>")
def eliminar_producto(id):
    global PRODUCTOS
    PRODUCTOS = [p for p in PRODUCTOS if p["id"] != id]
    flash("Producto eliminado del inventario", "warning")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/producto/editar-precio/<int:id>", methods=["POST"])
def editar_precio_producto(id):
    nuevo_precio = float(request.form["nuevo_precio"])
    for p in PRODUCTOS:
        if p["id"] == id:
            p["precio"] = nuevo_precio
            flash(f"Precio de '{p['nombre']}' actualizado a S/. {nuevo_precio:.2f}", "success")
            break
    return redirect(url_for("admin_dashboard"))

# CRUD: SERVICIOS
@app.route("/admin/servicio/crear", methods=["POST"])
def crear_servicio():
    nuevo_id = max([s["id"] for s in SERVICIOS], default=0) + 1
    SERVICIOS.append({
        "id": nuevo_id,
        "nombre": request.form["nombre"],
        "precio": float(request.form["precio"]),
        "descripcion": request.form["descripcion"]
    })
    flash("Servicio agregado con éxito", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/servicio/eliminar/<int:id>")
def eliminar_servicio(id):
    global SERVICIOS
    SERVICIOS = [s for s in SERVICIOS if s["id"] != id]
    flash("Servicio retirado", "warning")
    return redirect(url_for("admin_dashboard"))

# CRUD: Clientes txt
@app.route("/admin/cliente/eliminar/<string:username>")
def eliminar_cliente(username):
    usuarios = obtener_usuarios()
    usuarios = [u for u in usuarios if u["usuario"] != username]
    guardar_usuarios(usuarios)
    flash(f"Cliente {username} eliminado de usuarios.txt", "danger")
    return redirect(url_for("admin_dashboard"))

# Carrito de ventas
@app.route("/agregar-carrito/<int:producto_id>")
def agregar_carrito(producto_id):
    if "carrito" not in session: session["carrito"] = {}
    carrito = session["carrito"]
    producto = next((p for p in PRODUCTOS if p["id"] == producto_id), None)
    if producto:
        id_str = str(producto_id)
        if id_str in carrito: carrito[id_str]["cantidad"] += 1
        else:
            carrito[id_str] = {"nombre": producto["nombre"], "precio": producto["precio"], "imagen": producto["imagen"], "cantidad": 1}
        session["carrito"] = carrito
        session.modified = True
    return redirect(url_for("index"))

@app.route("/carrito")
def ver_carrito():
    carrito = session.get("carrito", {})
    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())
    return render_template("carrito.html", carrito=carrito, total=total)

@app.route("/limpiar-carrito")
def limpiar_carrito():
    session.pop("carrito", None)
    return redirect(url_for("ver_carrito"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)