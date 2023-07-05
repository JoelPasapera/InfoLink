import requests
import socket
import whois
import urllib.parse
import tkinter as tk
from tkinter import messagebox
import pyperclip

# las primeras variables son las fuertes. las variables qeu usan la librerias o modulos. hay que ver que variables usan directamente las librerias, solo las que tienen conexion directa con la libreria., las variables en las try y direccion_ip son variables fuertes. el mantenimiento en un codig ocon pocas variables debiles es mas rapido.


def obtener_resultados():
    enlace = entrada_url.get()
    url = enlace
    # Enviar una solicitud HTTP al sitio web
    response = requests.get(url)
    # Verificar si se recibe una respuesta
    if response.status_code == 200:
        print("El sitio web existe")
    else:
        messagebox.showwarning("Advertencia", f"no existe una web llamada {enlace}")
    if not enlace.startswith("http"):
        enlace = "http://" + enlace
    try:
        url_parseada = urllib.parse.urlparse(enlace)
        parametros = urllib.parse.parse_qs(url_parseada.query)
        parametros_codificados = urllib.parse.urlencode(parametros, doseq=True)
        url_formateada = urllib.parse.urlunparse(
            (
                url_parseada.scheme,
                url_parseada.netloc,
                url_parseada.path,
                url_parseada.params,
                parametros_codificados,
                url_parseada.fragment,
            )
        )
        respuesta = requests.get(
            url_formateada
        )  # valores asignados son errores mas encontrados
        url_original = respuesta.url
        dominio = url_original.split("/")[2]
        direccion_ip = socket.gethostbyname(dominio)
        dominio_label.config(text="Dominio: " + dominio)
        direccion_ip_label.config(text="Dirección IP: " + direccion_ip)
        direccion_real_label.config(text="Dirección real: " + respuesta.url)
        informacion_whois = whois.whois(dominio)
        if informacion_whois.registrar:
            propietario_label.config(
                text="Propietario del dominio: " + informacion_whois.registrar
            )
        else:
            propietario_label.config(
                text="No se encontró información sobre el propietario del dominio."
            )
        if informacion_whois.city and informacion_whois.country:
            ubicacion_label.config(
                text="Ubicación del servidor: "
                + informacion_whois.city
                + ", "
                + informacion_whois.country
            )
        else:
            ubicacion_label.config(
                text="No se encontró información sobre la ubicación del servidor."
            )
        if informacion_whois.name:
            propietario_nombre_label.config(
                text="Información sobre el propietario del nombre de dominio: "
                + informacion_whois.name
            )
        else:
            propietario_nombre_label.config(
                text="No se encontró información sobre el propietario del nombre de dominio."
            )
        # Agregar el contenido del análisis al portapapeles
        contenido_analisis = (
            dominio_label.cget("text")
            + "\n"
            + direccion_ip_label.cget("text")
            + "\n"
            + direccion_real_label.cget("text")
            + "\n"
            + propietario_label.cget("text")
            + "\n"
            + ubicacion_label.cget("text")
            + "\n"
            + propietario_nombre_label.cget("text")
        )
        pyperclip.copy(contenido_analisis)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", str(e))


ventana = tk.Tk()
ventana.title("Obtener información de una URL")
ventana.geometry("800x600+250+50")

url_label = tk.Label(ventana, text="Ingresa la URL:")
url_label.pack()

entrada_url = tk.Entry(ventana)
entrada_url.pack()

boton_obtener = tk.Button(
    ventana, text="Obtener resultados", command=obtener_resultados
)
boton_obtener.pack()

dominio_label = tk.Label(ventana, text="")
dominio_label.pack()

direccion_ip_label = tk.Label(ventana, text="")
direccion_ip_label.pack()

direccion_real_label = tk.Label(ventana, text="")
direccion_real_label.pack()

propietario_label = tk.Label(ventana, text="")
propietario_label.pack()

ubicacion_label = tk.Label(ventana, text="")
ubicacion_label.pack()

propietario_nombre_label = tk.Label(ventana, text="")
propietario_nombre_label.pack()

# Agregar el botón para copiar el contenido del análisis al portapapeles
boton_copiar = tk.Button(
    ventana,
    text="Copiar resultado",
    command=lambda: pyperclip.copy(
        dominio_label.cget("text")
        + "\n"
        + direccion_ip_label.cget("text")
        + "\n"
        + direccion_real_label.cget("text")
        + "\n"
        + propietario_label.cget("text")
        + "\n"
        + ubicacion_label.cget("text")
        + "\n"
        + propietario_nombre_label.cget("text")
    ),
)
boton_copiar.pack()

ventana.mainloop()

dominio = url_original.split("/")[2]
print(whois.whois(dominio))
print(entrada_url.get())
print("hola")
