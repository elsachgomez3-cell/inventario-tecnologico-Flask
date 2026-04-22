from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "inventario_secret"

def get_db():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row
    return conn

# LISTAR
@app.route('/')
def index():
    db = get_db()
    productos = db.execute("SELECT * FROM productos").fetchall()
    db.close()
    return render_template("index.html", productos=productos)

# registrar nuevo
@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        categoria = request.form['categoria'].strip()
        precio = request.form['precio']
        stock = request.form['stock']

        if not nombre or not categoria:
            flash("Todos los campos son obligatorios")
            return redirect(url_for('nuevo'))

        if float(precio) < 0 or int(stock) < 0:
            flash("Valores inválidos")
            return redirect(url_for('nuevo'))

        db = get_db()
        db.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (nombre, categoria, precio, stock)
        )
        db.commit()
        db.close()

        flash("Producto agregado correctamente")
        return redirect(url_for('index'))

    return render_template("nuevo.html")

# EDITAR
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    db = get_db()

    if request.method == 'POST':
        db.execute("""
        UPDATE productos
        SET nombre=?, categoria=?, precio=?, stock=?
        WHERE id=?
        """, (
            request.form['nombre'],
            request.form['categoria'],
            request.form['precio'],
            request.form['stock'],
            id
        ))

        db.commit()
        db.close()
        flash("Producto actualizado")
        return redirect(url_for('index'))

    producto = db.execute("SELECT * FROM productos WHERE id=?", (id,)).fetchone()
    db.close()

    return render_template("editar.html", producto=producto)

# ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    db = get_db()
    db.execute("DELETE FROM productos WHERE id=?", (id,))
    db.commit()
    db.close()

    flash("Producto eliminado")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)