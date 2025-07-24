from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Función para guardar mensajes (opción 5)
def guardar_mensaje(nombre, mensaje):
    ruta = "mensajes.txt"
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"Nombre: {nombre}\nMensaje: {mensaje}\n---\n")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "").strip().lower()
    nombre = data.get("nombre", "Cliente")

    if user_msg in ["1", "instalacion", "instalación"]:
        reply = "💡 Instalación de minisplit: $1,600 MXN hasta $1,900 MXN (varía dependiendo la ubicación)."
    elif user_msg in ["2", "mantenimiento"]:
        reply = "🔧 Mantenimiento completo desde $800 MXN por unidad (puede aumentar según ubicación)."
    elif user_msg in ["3", "carga de gas"]:
        reply = "⛽ Carga de gas R410A o R22: desde $850 MXN (varía según capacidad y ubicación)."
    elif user_msg in ["4", "venta de equipo", "venta de equipo minisplit"]:
        reply = "🛒 Venta de equipo minisplit: contamos con equipo BAIR 1 tonelada 110V frío/calor $6,900 MXN (precio con instalación)."
    elif user_msg in ["5", "otra consulta", "consulta"]:
        reply = "Por favor escribe tu mensaje y nos pondremos en contacto contigo lo antes posible."
    elif user_msg.startswith("mensaje:"):
        texto = user_msg[len("mensaje:"):].strip()
        guardar_mensaje(nombre, texto)
        reply = f"✅ Gracias, hemos recibido tu mensaje: \"{texto}\". Te contactaremos pronto."
    elif user_msg == "hola":
        reply = (
            f"¡Hola {nombre}! ¿En qué puedo ayudarte?\n"
            "1. Instalación\n"
            "2. Mantenimiento\n"
            "3. Carga de gas\n"
            "4. Venta de equipo minisplit\n"
            "5. Otra consulta"
        )
    else:
        reply = "Lo siento, no entendí eso. Por favor responde con un número del 1 al 5 o 'hola' para el menú."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
