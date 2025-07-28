from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

estado_espera = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "").strip().lower()
    nombre = data.get("nombre", "Cliente")

    if nombre in estado_espera and estado_espera[nombre] == "confirmacion":
        respuesta = user_msg
        
        if respuesta in ["si", "sí", "s"]:
            reply = (
                f"¡Perfecto {nombre}! ¿En qué puedo ayudarte?\n"
                "1. Instalación\n"
                "2. Mantenimiento\n"
                "3. Carga de gas\n"
                "4. Venta de equipo minisplit\n"
                "5. Contacto"
            )
            estado_espera.pop(nombre)
        elif respuesta in ["no", "n"]:
            reply = f"🙏 Gracias {nombre} por utilizar Clima Bot. Esperamos tu mensaje por WhatsApp (opcion 5). ¡Buen día!"
            estado_espera.pop(nombre)
        else:
            # Si no es sí ni no, mostramos el menú sin insistir
            reply = (
                f"Entendido, {nombre}. ¿En qué puedo ayudarte?\n"
                "1. Instalación\n"
                "2. Mantenimiento\n"
                "3. Carga de gas\n"
                "4. Venta de equipo minisplit\n"
                "5. Contacto"
            )
            estado_espera.pop(nombre)

        return jsonify({"reply": reply})

    if user_msg in ["1", "instalacion", "instalación"]:
        reply = "💡 Instalación de minisplit: $1,600 MXN hasta $1,900 MXN (varía dependiendo la ubicación).\n\n¿Tienes otra duda? (Responde **sí** o **no**)"
        estado_espera[nombre] = "confirmacion"
    elif user_msg in ["2", "mantenimiento"]:
        reply = "🔧 Mantenimiento completo desde $800 MXN por unidad (puede aumentar según ubicación).\n\n¿Tienes otra duda? (Responde **sí** o **no**)"
        estado_espera[nombre] = "confirmacion"
    elif user_msg in ["3", "carga de gas"]:
        reply = "⛽ Carga de gas R410A o R22: desde $850 MXN (varía según capacidad y ubicación).\n\n¿Tienes otra duda? (Responde **sí** o **no**)"
        estado_espera[nombre] = "confirmacion"
    elif user_msg in ["4", "venta de equipo", "venta de equipo minisplit"]:
        reply = "🛒 Venta de equipo minisplit: contamos con equipo BAIR 1 tonelada 110V frío/calor nuevo $6,900 MXN (precio con instalación), pregunta tambien por nuestros equipos usados en venta.\n\n¿Tienes otra duda? (Responde **sí** o **no**)"
        estado_espera[nombre] = "confirmacion"
    elif user_msg in ["5", "contacto", "whatsapp"]:
        reply = (
            "Whatsapp da clic: <a href='https://wa.me/6648095987' target='_blank'>6648095987</a>\n\n"
            "¿Tienes otra duda? (Responde **sí** o **no**)"
        )
        estado_espera[nombre] = "confirmacion"
    elif user_msg == "hola":
        reply = (
            f"¡Hola {nombre}! ¿En qué puedo ayudarte?\n"
            "1. Instalación\n"
            "2. Mantenimiento\n"
            "3. Carga de gas\n"
            "4. Venta de equipo minisplit\n"
            "5. Contacto"
        )
    else:
        reply = "Lo siento, no entendí eso. Por favor responde con un número del 1 al 5 o 'hola' para el menú."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
