import socket
import argparse
import ipaddress
import platform
import subprocess
import re
import os

def obtener_dominio(url):
    if not url.startswith("http"):
        url = "http://" + url
    dominio = re.findall(r"https?://([^/]+)", url)
    return dominio[0] if dominio else None

def resolver_ips_locales(dominio):
    try:
        _, _, ip_list = socket.gethostbyname_ex(dominio)
        return list(set(ip_list))
    except socket.gaierror:
        return []

def resolver_ips_publicas_con_dig(dominio):
    try:
        resultado = subprocess.run(["dig", "+short", dominio, "@8.8.8.8"], stdout=subprocess.PIPE, text=True, check=True)
        ips = resultado.stdout.strip().split("\n")
        return [ip for ip in ips if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    except Exception:
        return []

def explicar_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        primer_octeto = int(ip.split('.')[0])
        clase = (
            'Clase A' if primer_octeto < 128 else
            'Clase B' if primer_octeto < 192 else
            'Clase C' if primer_octeto < 224 else
            'Clase D (Multicast)' if primer_octeto < 240 else
            'Clase E (Experimental)'
        )
        tipo = 'Privada' if ip_obj.is_private else 'Pública'
        return f"Clase: {clase}, Tipo: {tipo}"
    except ValueError:
        return "IP inválida"

def verificar_conectividad_ping(ip):
    sistema = platform.system()
    comando = ["ping", "-n", "1", ip] if sistema == "Windows" else ["ping", "-c", "1", ip]
    try:
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return resultado.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
    except Exception:
        return False

def verificar_conectividad_https(ip):
    try:
        with socket.create_connection((ip, 443), timeout=3):
            return True
    except Exception:
        return False

def ejecutar_y_parsear_nmap(ip, guardar_crudo=False, ruta_crudo="info_nmap.txt"):
    nmap_results = []
    crudo = []

    nmap_results.append(f"\n🔍 Escaneando puertos abiertos en: {ip}")
    nmap_full_scan_cmd = ["nmap", "-p-", "--open", "-sS", "--min-rate", "5000", "-vvv", "-n", "-Pn", ip]
    try:
        full_scan_output = subprocess.run(
            nmap_full_scan_cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=300
        )
        crudo.append(f"\n\n########## ESCANEO COMPLETO DE PUERTOS - {ip} ##########\n")
        crudo.append(full_scan_output.stdout)

        open_ports = re.findall(r"(\d+)/tcp\s+open", full_scan_output.stdout)
        if not open_ports:
            nmap_results.append("   ❌ No se encontraron puertos abiertos.")
            return "\n".join(nmap_results)

        nmap_results.append(f"   ✅ Puertos abiertos: {', '.join(open_ports)}")

        ports_str = ",".join(open_ports)
        nmap_service_scan_cmd = ["nmap", "-sCV", "-p", ports_str, "-n", "-Pn", ip]
        nmap_results.append(f"\n🔧 Detectando servicios y versiones en puertos: {ports_str}...")

        service_scan_output = subprocess.run(
            nmap_service_scan_cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=600
        )
        crudo.append(f"\n\n########## DETECCIÓN DE SERVICIOS - {ip} ##########\n")
        crudo.append(service_scan_output.stdout)

        service_lines = re.findall(r"(\d+)/tcp\s+(open)\s+([^\s]+)\s*(.*)", service_scan_output.stdout)
        if not service_lines:
            nmap_results.append("   ⚠️ No se pudieron interpretar los servicios.")
        else:
            nmap_results.append(f"\n🧪 Servicios detectados:")
            for port, _, service, version_info in service_lines:
                desc = f"{service} {version_info.strip()}" if version_info.strip() else service
                nmap_results.append(f"     • Puerto {port}: {desc}")

        if guardar_crudo:
            with open(ruta_crudo, "a", encoding="utf-8") as f:
                f.write("\n".join(crudo) + "\n")

    except FileNotFoundError:
        nmap_results.append("   ❌ Nmap no está instalado o no está en PATH.")
    except subprocess.TimeoutExpired:
        nmap_results.append("   ⏱️ El escaneo Nmap excedió el tiempo permitido.")
    except subprocess.CalledProcessError as e:
        nmap_results.append(f"   ❌ Error durante el escaneo Nmap: {e}")
    except Exception as e:
        nmap_results.append(f"   ❌ Error inesperado: {e}")

    return "\n".join(nmap_results)

def analizar_url(url, guardar_crudo=False):
    salida = []
    dominio = obtener_dominio(url)
    if not dominio:
        return "❌ No se pudo extraer el dominio desde la URL.\n"

    salida.append(f"🔗 URL: {url}")
    salida.append(f"🌐 Dominio: {dominio}")

    ips_locales = resolver_ips_locales(dominio)
    ips_publicas = resolver_ips_publicas_con_dig(dominio)
    todas_ips = list(set(ips_locales + ips_publicas))

    salida.append(f"📡 IPs encontradas: {', '.join(todas_ips) if todas_ips else 'Ninguna'}")

    if not todas_ips:
        salida.append("❌ No se pudo resolver ninguna IP.")
        return "\n".join(salida)

    for ip in todas_ips:
        explicacion = explicar_ip(ip)
        origen = []
        if ip in ips_locales:
            origen.append("Interna")
        if ip in ips_publicas:
            origen.append("Pública")

        ping_ok = verificar_conectividad_ping(ip)
        https_ok = verificar_conectividad_https(ip)

        conectividad = []
        if ping_ok:
            conectividad.append("Ping")
        if https_ok:
            conectividad.append("HTTPS")
        if not conectividad:
            conectividad.append("Ninguna")

        salida.append(f" - 🧠 IP: {ip} → {explicacion}, Origen: {', '.join(origen)}, Conectividad: {', '.join(conectividad)}")

    salida.append("\n" + "="*70)
    salida.append("--- INICIANDO ESCANEOS AUTOMÁTICOS DE SERVICIOS CON NMAP ---")
    salida.append("⚠️ ¡Asegúrate de tener permiso explícito para escanear el objetivo!")
    salida.append("="*70)

    if os.name != "nt" and os.geteuid() != 0:
        salida.append("\n❌ ERROR: El script NO se está ejecutando como root.")
        salida.append("   Ejecuta el script con: sudo python3 escaner_auto.py https://ejemplo.com")
    else:
        for ip in todas_ips:
            salida.append(f"\n{'#'*60}")
            salida.append(f"### 🔬 Analizando servicios para la IP: {ip} ###")
            salida.append(f"{'#'*60}")
            salida.append(ejecutar_y_parsear_nmap(ip, guardar_crudo))
            salida.append(f"{'#'*60}")
            salida.append(f"### ✅ Análisis finalizado para: {ip} ###\n")

    salida.append("="*70)
    salida.append("--- FIN DE LOS ESCANEOS AUTOMÁTICOS DE NMAP ---")
    salida.append("="*70)

    return "\n".join(salida) + "\n"

def main():
    parser = argparse.ArgumentParser(
        description="🔍 Escáner automático de red para analizar URLs, IPs y servicios con Nmap.",
        epilog="Ejemplo: sudo python3 escaner_auto.py https://ejemplo.com -Og salida.txt -GC"
    )
    parser.add_argument("url", nargs="?", help="URL a analizar (ej: https://ejemplo.com)")
    parser.add_argument("-a", "--auto", action="store_true", help="Modo automático (sin preguntar)")
    parser.add_argument("-Og", metavar="archivo", help="Guardar salida parseada en archivo de texto")
    parser.add_argument("-GC", action="store_true", help="Guardar salida cruda de Nmap en 'info_nmap.txt'")
    args = parser.parse_args()

    url = args.url
    if not url and not args.auto:
        url = input("Introduce la URL (ej: https://ejemplo.com/login): ").strip()

    if not url:
        print("❌ No se proporcionó una URL.")
        return

    print("\n" + "="*70)
    print("⚠️  ADVERTENCIA: Este script realiza escaneos con Nmap automáticamente")
    print("  - Asegúrate de contar con permiso explícito.")
    print("  - Ejecuta como root o administrador.")
    print("  - Los escaneos pueden tardar varios minutos.")
    print("="*70 + "\n")

    resultado = analizar_url(url, guardar_crudo=args.GC)
    print(resultado)

    if args.Og:
        try:
            with open(args.Og, "w", encoding="utf-8") as f:
                f.write(resultado)
            print(f"💾 Resultado parseado guardado en: {args.Og}")
        except Exception as e:
            print(f"❌ Error al guardar archivo: {e}")

    if args.GC:
        print("📂 Salida cruda de Nmap guardada en: info_nmap.txt")

if __name__ == "__main__":
    main()