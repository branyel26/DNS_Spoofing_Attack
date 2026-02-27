# DNS Spoofing Attack - Envenenamiento DNS

## Descripción

Este proyecto demuestra un ataque de **DNS Spoofing (Envenenamiento DNS)** utilizando Python y Scapy. El ataque redirige las consultas DNS de un dominio específico hacia una IP controlada por el atacante, permitiendo ataques de tipo Man-in-the-Middle (MITM).

## Topología de Red

![Topología GNS3](Topologia_GNS3.png)

## Entorno del Laboratorio

| Dispositivo | Dirección IP | Función |
|-------------|--------------|---------|
| **Ubuntu (Atacante)** | `10.14.89.5` | Estación de Ataque (MITM / DNS Faker) |
| **Kali (Víctima)** | `10.14.89.4` | Objetivo / Víctima |
| **Router** | `10.14.89.1` | Gateway de la red |
| **Switch** | N/A | Nodo de Red (Capa 2) |

- **Segmento de Red:** 10.14.89.0/26 (Rango útil: .1 a .62)
- **Interfaz del atacante:** `ens3`

## Pre-requisitos

Para que este ataque funcione, primero se debe realizar un **ARP Spoofing** para posicionarse como Man-in-the-Middle entre la víctima y el gateway. Esto se logró con Bettercap:

```bash
# En Bettercap
set arp.spoof.targets 10.14.89.4
set arp.spoof.fullduplex true
arp.spoof on
```

## Requisitos

- Python 3.x
- Scapy (`pip install scapy`)
- Permisos de superusuario (root)
- Posicionamiento MITM previo (ARP Spoofing)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/DNS_Spoofing_Attack.git
cd DNS_Spoofing_Attack

# Instalar dependencias
pip install scapy
```

## Uso

```bash
sudo python3 DNS_Spoofing.py
```

## Cómo Funciona el Ataque

### Paso 1: Posicionamiento MITM
Antes de ejecutar el script, se debe realizar ARP Spoofing para interceptar el tráfico entre la víctima y el gateway.

### Paso 2: Interceptar Consultas DNS
El script escucha en la interfaz de red especificada (`ens3`) filtrando tráfico UDP en el puerto 53 (DNS).

### Paso 3: Detectar el Dominio Objetivo
Cuando se detecta una consulta DNS para `itla.edu.do`, el script captura el paquete.

### Paso 4: Construir Respuesta Falsa
El script construye una respuesta DNS falsa que incluye:
- **ID de transacción:** Copiado del paquete original para que la víctima lo acepte
- **Registro A:** Apunta al IP del atacante (`10.14.89.5`)
- **TTL:** Tiempo de vida del registro en caché

### Paso 5: Enviar Respuesta Maliciosa
La respuesta falsa se envía antes que la respuesta legítima del servidor DNS real.

## Verificación del Ataque

Desde la máquina víctima (Kali):

```bash
nslookup itla.edu.do
```

**Resultado esperado:** La dirección IP devuelta será `10.14.89.5` (IP del atacante) en lugar de la IP legítima.

## Flujo del Ataque

```
┌─────────────┐       DNS Query       ┌─────────────┐
│   Víctima   │ ───────────────────▶ │  Atacante   │
│ 10.14.89.4  │                      │ 10.14.89.5  │
└─────────────┘                      └─────────────┘
                                            │
                    Respuesta Falsa         │
                    (IP: 10.14.89.5)        │
┌─────────────┐ ◀───────────────────────────┘
│   Víctima   │
│ 10.14.89.4  │
└─────────────┘
```

## Mitigaciones

- **DNSSEC:** Implementar firmas digitales en respuestas DNS
- **DNS sobre HTTPS (DoH):** Cifrar consultas DNS
- **DNS sobre TLS (DoT):** Cifrar comunicaciones DNS
- **Dynamic ARP Inspection (DAI):** Prevenir ARP Spoofing en switches
- **DHCP Snooping:** Validar mensajes DHCP en la red

## Estructura del Proyecto

```
DNS_Spoofing_Attack/
├── DNS_Spoofing.py      # Script principal del ataque
├── Topologia_GNS3.png   # Diagrama de la topología de red
└── README.md            # Esta documentación
```

## Tecnologías Utilizadas

- **Python 3**
- **Scapy** - Manipulación de paquetes de red
- **GNS3** - Simulador de red
- **VMware** - Virtualización

---

## Descargo de Responsabilidad

> **⚠️ AVISO IMPORTANTE**
> 
> Este script fue desarrollado **exclusivamente con fines educativos** como parte del laboratorio de la materia **Seguridad de Redes** en el **Instituto Tecnológico de Las Américas (ITLA)**.
> 
> El uso de estas herramientas en redes sin autorización explícita es **ilegal** y puede conllevar consecuencias legales severas.
> 
> **Estudiante:** Branyel Pérez  
> **Matrícula:** 2024-1489  
> **Docente:** Jonathan Rondón  
> **Institución:** Instituto Tecnológico de Las Américas (ITLA)
