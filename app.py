import customtkinter as ctk
import tkinter as tk
from tkinter import END

from files import load_config, save_config
from bluetooth import (
    conectar_bluetooth,
    desconectar_bluetooth,
    enviar_datos_bluetooth,
    listar_puertos_bluetooth,
)


class App(ctk.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)

        self.title("SIGUEPOP")
        self.geometry("860x780")
        self.resizable(False, False)

        config = load_config()

        self.kd_var = ctk.StringVar(value=config["KD"])
        self.kp_var = ctk.StringVar(value=config["KP"])
        self.ki_var = ctk.StringVar(value=config["KI"])
        self.kv_var = ctk.StringVar(value=config["Kv"])
        self.kvi_var = ctk.StringVar(value=config["Kvi"])
        self.vbase_var = ctk.StringVar(value=config["Vbase"])
        self.volantazo_var = ctk.StringVar(value=config["Volantazo"])
        self.umbral_var = ctk.StringVar(value=config["Umbral"])

        self.mac_var = ctk.StringVar(value=config["MAC"])
        self.com_var = ctk.StringVar(value=config["COM"])
        self.baudrate_var = ctk.StringVar(value=config["BAUDRATE"])

        self.sock_bt = None
        self.conectado = False
        self.estado_conexion = "inicio"

        self.crear_widgets()
        self.cargar_icono()
        self.actualizar_estado_visual("inicio")
        self.actualizar_lista_puertos_bt(mostrar_log=False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.escribir_log("Aplicación iniciada")
        self.escribir_log("Modo: Bluetooth Serial (SPP)")

    def cargar_icono(self):
        try:
            self.iconbitmap("icono.ico")
            self.escribir_log("Icono cargado correctamente")
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
            if hasattr(self, "terminal"):
                self.escribir_log(f"No se pudo cargar el icono: {e}")

    def crear_widgets(self):
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(padx=0, pady=8, fill="x")

        self.btn_conectar = ctk.CTkButton(
            frame_botones,
            text="Conectar BT",
            command=self.conectar,
        )
        self.btn_conectar.grid(row=0, column=0, padx=10, pady=10)

        self.btn_desconectar = ctk.CTkButton(
            frame_botones,
            text="Desconectar BT",
            command=self.desconectar,
        )
        self.btn_desconectar.grid(row=0, column=1, padx=10, pady=10)

        self.btn_buscar_bt = ctk.CTkButton(
            frame_botones,
            text="Buscar BT",
            command=self.actualizar_lista_puertos_bt,
        )
        self.btn_buscar_bt.grid(row=0, column=2, padx=10, pady=10)

        self.btn_limpiar = ctk.CTkButton(
            frame_botones,
            text="Limpiar terminal",
            command=self.limpiar_terminal,
        )
        self.btn_limpiar.grid(row=0, column=3, padx=10, pady=10)

        self.btn_enviar = ctk.CTkButton(
            frame_botones,
            text="ENVIAR",
            command=self.enviar_datos_boton,
        )
        self.btn_enviar.grid(row=0, column=4, padx=10, pady=10)

        frame_estado = ctk.CTkFrame(self, fg_color="transparent")
        frame_estado.pack(pady=6)

        bg_color = self._apply_appearance_mode(self.cget("fg_color"))

        self.canvas_estado = tk.Canvas(
            frame_estado,
            width=22,
            height=22,
            highlightthickness=0,
            bg=bg_color,
        )
        self.canvas_estado.pack(side="left", padx=(0, 8))

        self.circulo_estado = self.canvas_estado.create_oval(
            2, 2, 20, 20,
            fill="gray",
            outline="",
        )

        self.label_estado = ctk.CTkLabel(frame_estado, text="Estado: Inicio")
        self.label_estado.pack(side="left")

        frame_const = ctk.CTkFrame(self)
        frame_const.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(frame_const, text="Kd :").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.kd_var, width=180).grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame_const, text="Kp :").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.kp_var, width=180).grid(row=1, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame_const, text="Ki :").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.ki_var, width=180).grid(row=2, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame_const, text="Kv :").grid(row=0, column=2, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.kv_var, width=180).grid(row=0, column=3, padx=10, pady=8)

        ctk.CTkLabel(frame_const, text="Kvi :").grid(row=1, column=2, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.kvi_var, width=180).grid(row=1, column=3, padx=10, pady=8)

        ctk.CTkLabel(frame_const, text="Vbase :").grid(row=2, column=2, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.vbase_var, width=180).grid(row=2, column=3, padx=10, pady=8)

        ctk.CTkLabel(frame_const, text="Volantazo :").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.volantazo_var, width=180).grid(row=3, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame_const, text="Umbral :").grid(row=3, column=2, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_const, textvariable=self.umbral_var, width=180).grid(row=3, column=3, padx=10, pady=8)

        self.btn_guardar_const = ctk.CTkButton(
            frame_const,
            text="Guardar constantes",
            command=self.guardar_constantes,
        )
        self.btn_guardar_const.grid(row=0, column=4, rowspan=4, padx=15, pady=8)

        frame_cfg = ctk.CTkFrame(self)
        frame_cfg.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(frame_cfg, text="MAC BT :").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_cfg, textvariable=self.mac_var, width=220).grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame_cfg, text="COM BT :").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_cfg, textvariable=self.com_var, width=220).grid(row=1, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame_cfg, text="BAUDRATE :").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkEntry(frame_cfg, textvariable=self.baudrate_var, width=220).grid(row=2, column=1, padx=10, pady=8)

        self.combo_puertos_bt = ctk.CTkComboBox(
            frame_cfg,
            values=["Sin detectar"],
            width=280,
            command=self.seleccionar_puerto_bt,
        )
        self.combo_puertos_bt.grid(row=0, column=2, padx=15, pady=8, rowspan=2)
        self.combo_puertos_bt.set("Sin detectar")

        self.btn_guardar_cfg = ctk.CTkButton(
            frame_cfg,
            text="Guardar config",
            command=self.guardar_config,
        )
        self.btn_guardar_cfg.grid(row=0, column=3, rowspan=3, padx=15, pady=8)

        frame_terminal = ctk.CTkFrame(self)
        frame_terminal.pack(padx=20, pady=12, fill="both", expand=True)

        ctk.CTkLabel(frame_terminal, text="Terminal / Log").pack(pady=(8, 4))

        self.terminal = ctk.CTkTextbox(frame_terminal, width=500, height=260)
        self.terminal.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    def actualizar_estado_visual(self, estado):
        self.estado_conexion = estado

        if estado == "inicio":
            color = "gray"
            texto = "Estado: Inicio"
        elif estado == "conectado":
            color = "green"
            texto = "Estado: Bluetooth conectado"
        elif estado == "desconectado":
            color = "red"
            texto = "Estado: Bluetooth desconectado"
        else:
            color = "gray"
            texto = "Estado: Desconocido"

        self.canvas_estado.itemconfig(self.circulo_estado, fill=color)
        self.label_estado.configure(text=texto)

    def escribir_log(self, texto):
        self.terminal.insert(END, texto + "\n")
        self.terminal.see(END)

    def limpiar_terminal(self):
        self.terminal.delete("1.0", END)

    def obtener_config_actual(self):
        return {
            "MAC": self.mac_var.get().strip(),
            "COM": self.com_var.get().strip(),
            "BAUDRATE": self.baudrate_var.get().strip(),
            "KD": self.kd_var.get().strip(),
            "KP": self.kp_var.get().strip(),
            "KI": self.ki_var.get().strip(),
            "Kv": self.kv_var.get().strip(),
            "Kvi": self.kvi_var.get().strip(),
            "Vbase": self.vbase_var.get().strip(),
            "Volantazo": self.volantazo_var.get().strip(),
            "Umbral": self.umbral_var.get().strip(),
        }

    def guardar_constantes(self):
        data = load_config()
        data.update({
            "KD": self.kd_var.get().strip(),
            "KP": self.kp_var.get().strip(),
            "KI": self.ki_var.get().strip(),
            "Kv": self.kv_var.get().strip(),
            "Kvi": self.kvi_var.get().strip(),
            "Vbase": self.vbase_var.get().strip(),
            "Volantazo": self.volantazo_var.get().strip(),
            "Umbral": self.umbral_var.get().strip(),
        })

        try:
            save_config(data)
            self.escribir_log(
                "Constantes guardadas: "
                f"Kd={data['KD']} | "
                f"Kp={data['KP']} | "
                f"Ki={data['KI']} | "
                f"Kv={data['Kv']} | "
                f"Kvi={data['Kvi']} | "
                f"Vbase={data['Vbase']} | "
                f"Volantazo={data['Volantazo']} | "
                f"Umbral={data['Umbral']}"
            )
        except Exception as e:
            self.escribir_log(f"Error guardando constantes: {e}")

    def guardar_config(self):
        data = load_config()
        data.update({
            "MAC": self.mac_var.get().strip(),
            "COM": self.com_var.get().strip(),
            "BAUDRATE": self.baudrate_var.get().strip(),
        })

        try:
            save_config(data)
            self.escribir_log(
                "Configuración guardada: "
                f"MAC={data['MAC']} | "
                f"COM={data['COM']} | "
                f"BAUDRATE={data['BAUDRATE']}"
            )
        except Exception as e:
            self.escribir_log(f"Error guardando config: {e}")

    def actualizar_lista_puertos_bt(self, mostrar_log=True):
        puertos = listar_puertos_bluetooth()

        if puertos:
            valores = [f"{p['device']} | {p['description']}" for p in puertos]
            self.combo_puertos_bt.configure(values=valores)

            puerto_actual = self.com_var.get().strip()
            seleccion = next((v for v in valores if v.startswith(puerto_actual + " ") or v.startswith(puerto_actual + "|")), valores[0])
            self.combo_puertos_bt.set(seleccion)

            if mostrar_log:
                lista = ", ".join(p["device"] for p in puertos)
                self.escribir_log(f"Puertos Bluetooth detectados: {lista}")
        else:
            self.combo_puertos_bt.configure(values=["Sin detectar"])
            self.combo_puertos_bt.set("Sin detectar")
            if mostrar_log:
                self.escribir_log("No se han detectado puertos Bluetooth SPP.")

    def seleccionar_puerto_bt(self, valor):
        if valor and valor != "Sin detectar":
            puerto = valor.split("|")[0].strip()
            self.com_var.set(puerto)
            self.escribir_log(f"Puerto Bluetooth seleccionado: {puerto}")

    def _marcar_desconectado(self, mensaje=None):
        self.sock_bt = None
        self.conectado = False
        self.actualizar_estado_visual("desconectado")
        if mensaje:
            self.escribir_log(mensaje)

    def enviar_datos_boton(self):
        config_actual = self.obtener_config_actual()

        mensaje_enviado = (
            "Enviado -> "
            f"KD={config_actual['KD']} | "
            f"KP={config_actual['KP']} | "
            f"KI={config_actual['KI']} | "
            f"Kv={config_actual['Kv']} | "
            f"Kvi={config_actual['Kvi']} | "
            f"Vbase={config_actual['Vbase']} | "
            f"Volantazo={config_actual['Volantazo']} | "
            f"Umbral={config_actual['Umbral']}"
        )
        self.escribir_log(mensaje_enviado)

        ok, mensaje, conexion_cerrada = enviar_datos_bluetooth(self.sock_bt, config_actual)

        if ok:
            self.escribir_log(f"ESP32 -> {mensaje}")
        else:
            if conexion_cerrada:
                self._marcar_desconectado(mensaje)
            else:
                self.escribir_log(f"Fallo al enviar: {mensaje}")

    def conectar(self):
        config_actual = self.obtener_config_actual()

        ok, sock_bt, mensaje = conectar_bluetooth(config_actual)

        if ok:
            self.sock_bt = sock_bt
            self.conectado = True
            self.actualizar_estado_visual("conectado")
            self.escribir_log(mensaje)
        else:
            self.sock_bt = None
            self.conectado = False
            self.actualizar_estado_visual("desconectado")
            self.escribir_log(mensaje)

    def desconectar(self):
        ok, mensaje = desconectar_bluetooth(self.sock_bt)

        if ok:
            self.sock_bt = None
            self.conectado = False
            self.actualizar_estado_visual("desconectado")
            self.escribir_log(mensaje)
        else:
            self.escribir_log(mensaje)

    def on_closing(self):
        if self.sock_bt is not None:
            try:
                if self.sock_bt.is_open:
                    self.sock_bt.close()
            except Exception:
                pass
        self.destroy()



def lanzar_app():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    lanzar_app()
