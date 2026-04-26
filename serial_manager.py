import json
import serial
import time


def conectar_serial(config):
    try:
        puerto_com = config["COM"].strip()
        baudrate = int(config["BAUDRATE"])

        ser = serial.Serial(puerto_com, baudrate=baudrate, timeout=0.5)
        time.sleep(2)
        ser.reset_input_buffer()

        return True, ser, f"Conectado a {puerto_com} | BAUDRATE={baudrate}"

    except Exception as e:
        return False, None, f"Error al conectar: {e}"


def desconectar_serial(ser):
    try:
        if ser is not None and ser.is_open:
            ser.close()
            return True, "Desconectado correctamente"
        return True, "Ya estaba desconectado"

    except Exception as e:
        return False, f"Error al desconectar: {e}"


def enviar_datos(ser, config):
    try:
        if ser is None or not ser.is_open:
            return False, "No hay conexión serie activa"

        datos = {
            "MAC": str(config["MAC"]),
            "COM": str(config["COM"]),
            "BAUDRATE": int(config["BAUDRATE"]),
            "KD": float(config["KD"]),
            "KP": float(config["KP"]),
            "KI": float(config["KI"]),
            "Kv": float(config["Kv"]),
            "Kvi": float(config["Kvi"]),
            "Vbase": float(config["Vbase"]),
            "Volantazo": float(config["Volantazo"]),
            "Umbral": float(config["Umbral"])
        }

        mensaje = json.dumps(datos) + "\n"

        ser.write(mensaje.encode("utf-8"))
        ser.flush()

        time.sleep(0.2)

        respuestas = []
        while ser.in_waiting > 0:
            respuesta = ser.readline().decode("utf-8", errors="ignore").strip()
            if respuesta:
                respuestas.append(respuesta)

        if respuestas:
            return True, " | ".join(respuestas)

        return True, "Datos enviados correctamente"

    except Exception as e:
        return False, f"Error al enviar datos: {e}"