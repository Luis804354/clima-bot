from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

estado_espera = {}

# Texto del menú principal (solo se define una vez)
def menu_principal(nombre):
    return (
        f"¡Hola {nombre}! ¿En qué puedo ayudarte?\n"
        "1. Instalación\n"
        "2. Mantenimiento\n"
        "3. Carga de gas\n"
        "4. Venta de equipo minisplit\n"
        "5. Contacto\n"
        "6. Equipos usados"
    )

confirmacion = "\n\n¿Tienes otra duda? (Responde **sí** o **no**)"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "").strip().lower()
    nombre = data.get("nombre", "Cliente")

    # Si está en estado de confirmación
    if nombre in estado_espera and estado_espera[nombre] == "confirmacion":
        respuesta = user_msg

        if respuesta in ["si", "sí", "s"]:
            reply = menu_principal(nombre)
        elif respuesta in ["no", "n"]:
            reply = f"🙏 Gracias {nombre} por utilizar Clima Bot. Esperamos tu mensaje por WhatsApp (opción 5). ¡Buen día!"
        else:
            reply = menu_principal(nombre)

        estado_espera.pop(nombre)
        return jsonify({"reply": reply})

    # Opciones (usamos un diccionario para evitar varios elif)
    opciones = {
        "1": "💡 Instalación de minisplit: $1,600 MXN hasta $1,900 MXN (varía dependiendo la ubicación).",
        "instalacion": "💡 Instalación de minisplit: $1,600 MXN hasta $1,900 MXN (varía dependiendo la ubicación).",
        "instalación": "💡 Instalación de minisplit: $1,600 MXN hasta $1,900 MXN (varía dependiendo la ubicación).",

        "2": "🔧 Mantenimiento completo desde $800 MXN por unidad (puede aumentar según ubicación).",
        "mantenimiento": "🔧 Mantenimiento completo desde $800 MXN por unidad (puede aumentar según ubicación).",

        "3": "⛽ Carga de gas R410A o R22: desde $850 MXN (varía según capacidad y ubicación).",
        "carga de gas": "⛽ Carga de gas R410A o R22: desde $850 MXN (varía según capacidad y ubicación).",

        "4": "🛒 Venta de equipo minisplit: contamos con equipo BAIR 1 tonelada 110V frío/calor nuevo $6,900 MXN (precio con instalación). Pregunta también por nuestros equipos usados en venta.",
        "venta de equipo": "🛒 Venta de equipo minisplit: contamos con equipo BAIR 1 tonelada 110V frío/calor nuevo $6,900 MXN (precio con instalación). Pregunta también por nuestros equipos usados en venta.",
        "venta de equipo minisplit": "🛒 Venta de equipo minisplit: contamos con equipo BAIR 1 tonelada 110V frío/calor nuevo $6,900 MXN (precio con instalación). Pregunta también por nuestros equipos usados en venta.",

        "5": "Whatsapp da clic: <a href='https://wa.me/6648095987' target='_blank'>6648095987</a>",
        "contacto": "Whatsapp da clic: <a href='https://wa.me/6648095987' target='_blank'>6648095987</a>",
        "whatsapp": "Whatsapp da clic: <a href='https://wa.me/6648095987' target='_blank'>6648095987</a>",

        # Nueva opción 6
        "6": "Whatsapp da clic: <a href='https://wa.me/6641869369' target='_blank'>6641869369</a>",
        "equipos usados": "Whatsapp da clic: <a href='https://wa.me/6641869369' target='_blank'>6641869369</a>"
    }

    if user_msg in opciones:
        reply = opciones[user_msg] + confirmacion
        estado_espera[nombre] = "confirmacion"
    elif user_msg == "hola":
        reply = menu_principal(nombre)
    else:
        reply = "Lo siento, no entendí eso. Por favor responde con un número del 1 al 6 o 'hola' para el menú."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
