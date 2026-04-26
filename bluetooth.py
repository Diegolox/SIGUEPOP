import json
import time
import serial
from serial.tools import list_ports

TIEMPO_ESPERA_RESPUESTA = 4.0


def _es_puerto_bluetooth(port_info):
    texto = f"{port_info.device} {port_info.description} {port_info.hwid}".lower()
    patrones = [
        "bluetooth",
        "bthenum",
        "standard serial over bluetooth link",
    ]
    return any(patron in texto for patron in patrones)



def listar_puertos_bluetooth():
    puertos = []
    for port in list_ports.comports():
        if _es_puerto_bluetooth(port):
            puertos.append({
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid,
            })
    return puertos



def _resolver_puerto_bluetooth(config):
    puerto = str(config.get("COM", "")).strip()
    if puerto:
        return puerto

    puertos_bt = listar_puertos_bluetooth()
    if puertos_bt:
        return puertos_bt[0]["device"]

    return ""



def conectar_bluetooth(config):
    try:
        puerto_bt = _resolver_puerto_bluetooth(config)
        baudrate = int(str(config.get("BAUDRATE", "115200")).strip())
        mac = str(config.get("MAC", "")).strip()

        if not puerto_bt:
            puertos_bt = listar_puertos_bluetooth()
            if puertos_bt:
                lista = ", ".join(p["device"] for p in puertos_bt)
                return False, None, f"No se ha indicado COM Bluetooth. Detectados: {lista}"
            return False, None, "No se ha encontrado ningún puerto Bluetooth SPP. Empareja primero el ESP32 en Windows."

        ser = serial.Serial(puerto_bt, baudrate=baudrate, timeout=0.25, write_timeout=1)
        time.sleep(1.5)
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        texto_mac = f" | MAC={mac}" if mac else ""
        return True, ser, f"Bluetooth conectado en {puerto_bt}{texto_mac} | BAUDRATE={baudrate}"

    except Exception as e:
        return False, None, f"Error al conectar por Bluetooth: {e}"



def desconectar_bluetooth(ser):
    try:
        if ser is not None and ser.is_open:
            ser.close()
            return True, "Bluetooth desconectado correctamente"
        return True, "Bluetooth ya estaba desconectado"

    except Exception as e:
        return False, f"Error al desconectar Bluetooth: {e}"



def _crear_payload(config):
    return {
        "MAC": str(config.get("MAC", "")).strip(),
        "KD": float(str(config.get("KD", "0.0")).strip()),
        "KP": float(str(config.get("KP", "0.0")).strip()),
        "KI": float(str(config.get("KI", "0.0")).strip()),
        "Kv": float(str(config.get("Kv", "0.0")).strip()),
        "Kvi": float(str(config.get("Kvi", "0.0")).strip()),
        "Vbase": float(str(config.get("Vbase", "0.0")).strip()),
        "Volantazo": float(str(config.get("Volantazo", "0.0")).strip()),
        "Umbral": float(str(config.get("Umbral", "0.0")).strip()),
    }



def enviar_datos_bluetooth(ser, config, timeout_respuesta=TIEMPO_ESPERA_RESPUESTA):
    try:
        if ser is None or not ser.is_open:
            return False, "No hay conexión Bluetooth activa", True

        payload = _crear_payload(config)
        mensaje = json.dumps(payload) + "\n"

        ser.reset_input_buffer()
        ser.write(mensaje.encode("utf-8"))
        ser.flush()

        inicio = time.monotonic()
        respuestas = []

        while (time.monotonic() - inicio) < timeout_respuesta:
            if ser.in_waiting > 0:
                respuesta = ser.readline().decode("utf-8", errors="ignore").strip()
                if respuesta:
                    respuestas.append(respuesta)
                    time.sleep(0.1)
                    while ser.in_waiting > 0:
                        extra = ser.readline().decode("utf-8", errors="ignore").strip()
                        if extra:
                            respuestas.append(extra)
                    return True, " | ".join(respuestas), False
            time.sleep(0.05)

        if ser.is_open:
            ser.close()
        return False, f"No se recibió respuesta del ESP32 en {int(timeout_respuesta)} segundos. Bluetooth desconectado.", True

    except Exception as e:
        try:
            if ser is not None and ser.is_open:
                ser.close()
        except Exception:
            pass
        return False, f"Error al enviar datos por Bluetooth: {e}", True
