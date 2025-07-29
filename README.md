---

## 🔍 Escáner Automático de Red con Nmap y Resolución de IPs

Este script en Python analiza una URL para extraer su dominio, obtener las IPs asociadas (públicas y privadas), verificar conectividad básica, y realizar escaneos de puertos/servicios con **Nmap**, todo de forma automatizada.

---

### 🧠 Características principales

* 🌐 **Extracción de dominio** desde una URL.
* 🧠 **Resolución de IPs** (DNS del sistema y servidor público con `dig`).
* 🧪 **Clasificación de IPs**: clase A/B/C, pública o privada.
* 📡 **Verificación de conectividad** vía `ping` y conexión HTTPS (puerto 443).
* 🚀 **Escaneo de puertos y servicios** con Nmap (`-p-`, `-sS`, `-sCV`).
* 💾 **Opciones para guardar salida** parseada (`-Og`) y cruda (`-GC`) en archivos.
* 🛠️ Compatible con sistemas **Windows, Linux y macOS** (requiere adaptaciones mínimas en Windows).
* 📋 Interfaz de línea de comandos con `argparse`.

---

## ⚠️ Advertencia Legal

> Este script ejecuta escaneos de red que pueden ser considerados intrusivos.
> **Úsalo únicamente en sistemas de tu propiedad o con autorización explícita.**

---

## 📦 Requisitos

### General

* Python 3.8 o superior
* Acceso a internet
* Permisos de administrador/root (especialmente en Linux)
* Herramientas instaladas:

  * [`nmap`](https://nmap.org/) (debe estar disponible en el PATH)
  * [`dig`](https://bind9.readthedocs.io/en/latest/dig.html) (solo en Linux/macOS)

### Windows

* Visual Studio Code (VSCode)
* Extensión de Python instalada en VSCode
* Instalar `nmap` para Windows desde: [https://nmap.org/download.html](https://nmap.org/download.html)

  * Agrega la carpeta de instalación (`C:\Program Files (x86)\Nmap`) a tu **PATH del sistema**
* `dig` no está disponible por defecto en Windows → el script aún funciona, pero resolverá IPs solo mediante `socket.gethostbyname_ex`.

---

## ▶️ Cómo usarlo en **Windows con Visual Studio Code**

1. **Clona el repositorio** o descarga el archivo `escaner_auto.py`.

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

2. **Abre la carpeta en VSCode**
   Selecciona `Archivo > Abrir carpeta...` y elige el directorio donde está el script.

3. **Abre una terminal integrada**
   `Ctrl + ñ` o `Terminal > Nueva terminal`.

4. **Ejecuta el script** con Python. Por ejemplo:

```bash
python escaner_auto.py https://example.com -Og salida.txt -GC
```

---

## 🛠️ Opciones de ejecución

```bash
python escaner_auto.py [URL] [opciones]
```

### Parámetros:

| Opción            | Descripción                                                 |
| ----------------- | ----------------------------------------------------------- |
| `url`             | URL objetivo, por ejemplo `https://example.com/login`       |
| `-a`, `--auto`    | Modo automático (omite interacción por consola)             |
| `-Og archivo.txt` | Guarda salida **parseada** en archivo de texto              |
| `-GC`             | Guarda salida **cruda** del escaneo Nmap en `info_nmap.txt` |

---

## 🧪 Ejemplo de ejecución

```bash
python escaner_auto.py https://example.com -Og resultado.txt -GC
```

```
🔗 URL: https://example.com
🌐 Dominio: example.com
📡 IPs encontradas: 93.184.216.34
 - 🧠 IP: 93.184.216.34 → Clase: Clase A, Tipo: Pública, Origen: Pública, Conectividad: Ping, HTTPS
...
```

---

## 📁 Archivos generados

| Archivo         | Contenido                      |
| --------------- | ------------------------------ |
| `resultado.txt` | Salida interpretada y legible  |
| `info_nmap.txt` | Salida cruda generada por Nmap |

---

## ❓ Preguntas comunes

### ¿Puedo ejecutar este script en Windows sin permisos de administrador?

Sí, aunque ciertos escaneos (como `-sS`) pueden requerir permisos elevados o fallar si Nmap no tiene privilegios suficientes.

### ¿Qué pasa si no tengo `dig` en Windows?

El script sigue funcionando, pero solo podrá resolver IPs usando métodos locales (`socket.gethostbyname_ex`).

---

## 📜 Licencia

Distribuido bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

---
