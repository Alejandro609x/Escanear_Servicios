# 🔍 Escáner Automático de Servicios y Puertos con Nmap

Este repositorio contiene un **script avanzado de análisis de red** en Python que permite escanear servicios y puertos abiertos asociados a una URL o dominio, resolviendo todas las IPs (privadas y públicas) y ejecutando un análisis automatizado con **Nmap**.

---

## 🎯 Objetivo del proyecto

Este script fue creado con el propósito de:

* 🔍 Analizar automáticamente **una URL o dominio**
* 🌐 Resolver **todas las IPs asociadas** (públicas y privadas)
* 🧠 Clasificar IPs según su **clase (A/B/C)** y si son **públicas o privadas**
* 📶 Verificar la **conectividad** de cada IP (Ping y conexión HTTPS)
* 🔎 Realizar escaneos automáticos con **Nmap** para:

  * Detectar **puertos abiertos** (`-p- --open -sS`)
  * Identificar **servicios y versiones** (`-sCV`)
* 💾 Permitir guardar la salida **parseada** y **cruda** en archivos

> Este script es ideal para **auditorías internas de red**, **reconocimiento pasivo y activo**, y **pruebas de seguridad autorizadas**.

---

## ⚠️ Aviso legal

> **Este script realiza escaneos de red y servicios.**
> Úsalo **únicamente en sistemas de tu propiedad** o con autorización explícita.
> No nos hacemos responsables del uso indebido.

---

## 📥 Cómo descargarlo y usarlo

### 🔗 Repositorio oficial:

**[https://github.com/Alejandro609x/Escanear\_Servicios](https://github.com/Alejandro609x/Escanear_Servicios)**

---

### ✅ Instrucciones paso a paso

#### 1. Descargar el repositorio

**Opción A: Clonar con Git**

```bash
git clone https://github.com/Alejandro609x/Escanear_Servicios.git
cd Escanear_Servicios
```

**Opción B: Descargar como ZIP**

1. Ve a [https://github.com/Alejandro609x/Escanear\_Servicios](https://github.com/Alejandro609x/Escanear_Servicios)
2. Haz clic en el botón verde `Code` > `Download ZIP`
3. Extrae el archivo ZIP
4. Abre la carpeta `Escanear_Servicios`

---

#### 2. Requisitos

* ✅ Python 3.8 o superior
* ✅ `nmap` instalado y en el PATH
* 🔎 (Linux/macOS) `dig` instalado (opcional pero recomendado)
* ⚠️ Linux/macOS: Ejecutar como `root` para escaneo SYN (`-sS`)
* 💻 Windows: Ejecutar como administrador para evitar restricciones

---

### 💻 Uso en **Windows con Visual Studio Code**

1. Instala Python desde [python.org](https://www.python.org/downloads/)
2. Instala [Visual Studio Code](https://code.visualstudio.com/) + extensión de Python
3. Descarga o clona el repositorio
4. Abre la carpeta `Escanear_Servicios` en VSCode
5. Abre una terminal (`Ctrl + ñ`)
6. Ejecuta:

```bash
python escaner_servicios.py https://ejemplo.com -Og salida.txt -GC
```

---

### 🧪 Ejecución general

```bash
python escaner_servicios.py https://dominio.com -Og salida.txt -GC
```

En Linux/macOS:

```bash
sudo python3 escaner_servicios.py https://dominio.com -Og salida.txt -GC
```

---

### 📌 Argumentos disponibles

| Opción            | Descripción                                                       |
| ----------------- | ----------------------------------------------------------------- |
| `url`             | URL o dominio a analizar (ej. `https://example.com`)              |
| `-a`, `--auto`    | Modo automático (omite la interacción por consola)                |
| `-Og archivo.txt` | Guarda la **salida parseada** del análisis en un archivo de texto |
| `-GC`             | Guarda la **salida cruda** de Nmap en `info_nmap.txt`             |

---

### 📁 Archivos generados

| Archivo         | Descripción                                                |
| --------------- | ---------------------------------------------------------- |
| `salida.txt`    | Resultado limpio y organizado del análisis (si usas `-Og`) |
| `info_nmap.txt` | Resultado crudo de Nmap (si usas `-GC`)                    |

---

## 🧠 ¿Qué hace exactamente el script?

### Paso a paso:

1. 📥 **Extrae el dominio** de una URL
2. 🌐 **Resuelve las IPs** del dominio:

   * Por métodos locales (DNS del sistema)
   * Por `dig` con servidor público (8.8.8.8)
3. 🧩 **Clasifica cada IP**:

   * Por clase (A, B, C)
   * Por tipo (Pública o Privada)
4. 📡 **Verifica conectividad**:

   * Hace ping a la IP
   * Intenta conexión al puerto 443 (HTTPS)
5. 🚀 **Escanea la IP con Nmap**:

   * Encuentra todos los puertos abiertos (`-p- --open -sS`)
   * Detecta servicios y versiones (`-sCV`)
6. 📝 **Muestra y guarda los resultados** si se indicaron los parámetros `-Og` y `-GC`

---

## 📷 Ejemplo de salida

![Resultado de nmap -sn](/Imagenes/Resultado.png)

---
