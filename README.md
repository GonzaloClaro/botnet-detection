# JARM en la Red Chilena

Proyecto de investigación en ciberseguridad que aplica fingerprinting TLS mediante **JARM** para identificar posibles servidores de Comando y Control (C2) activos en dominios de la red chilena.

El trabajo completo está documentado en el informe incluido: [`Uso de Jarm en dominios de la red chilena.pdf`](./Uso%20de%20Jarm%20en%20dominios%20de%20la%20red%20chilena.pdf)

---

## ¿Qué es JARM?

[JARM](https://github.com/salesforce/jarm) es una herramienta de fingerprinting TLS activa desarrollada por el equipo de seguridad de Salesforce. Funciona enviando 10 saludos TLS cuidadosamente construidos a un servidor y analizando las respuestas para generar un hash de 62 caracteres que identifica de forma única la implementación SSL/TLS del servidor.

Este fingerprint es útil porque distintos frameworks de C2 (Cobalt Strike, Metasploit, Mythic, Sliver, etc.) dejan firmas TLS características y reproducibles, independientemente del dominio o IP que usen.

---

## Flujo del Proyecto

```
1. Escaneo JARM de dominios chilenos
        ↓
   resultado_jarm.csv
        ↓
2. Conversión de lista C2 conocida (C2.txt → Servidores_C2.csv)
        ↓ raw_txt_to_csv.py
   Servidores_C2.csv
        ↓
3. Cruce de fingerprints (inner join)
        ↓ jarm_chile.py
   Botnets_red_chilena.csv
```

### Paso 1 – Escaneo JARM

Se ejecutó la herramienta JARM original sobre una lista de dominios `.cl` y dominios activos en la red chilena, generando el archivo `resultado_jarm.csv` con columnas:

| Dominio | IP | JARM | TLS 1…10 |
|---|---|---|---|

### Paso 2 – Preparar la lista de C2 conocidos

El archivo `C2.txt` contiene una tabla de fingerprints JARM de herramientas C2 y red team conocidas (Cobalt Strike, Metasploit, Mythic, Sliver, Merlin, EvilGinx2, etc.), recopilada desde fuentes públicas de threat intelligence.

```bash
python raw_txt_to_csv.py
# Genera: Servidores_C2.csv
```

### Paso 3 – Detección de C2 en la red chilena

```bash
python jarm_chile.py
# Genera: Botnets_red_chilena.csv
```

El script:
- Filtra dominios sin conexión o con fingerprint nulo
- Realiza un **inner join** entre los fingerprints escaneados y la base de C2 conocidos
- Exporta los matches con dominio, IP, hash JARM, herramienta C2 identificada y fecha

---

## Archivos

| Archivo | Descripción |
|---|---|
| `jarm_chile.py` | Script principal de detección (cruce de fingerprints) |
| `raw_txt_to_csv.py` | Convierte `C2.txt` a CSV procesable |
| `C2.txt` | Lista de fingerprints JARM de C2/red team tools conocidas |
| `Uso de Jarm en dominios de la red chilena.pdf` | Informe completo del estudio |

### Archivos generados (no incluidos en el repo)

| Archivo | Descripción |
|---|---|
| `resultado_jarm.csv` | Output del escaneo JARM sobre dominios chilenos |
| `Servidores_C2.csv` | Lista C2 convertida a CSV |
| `Botnets_red_chilena.csv` | Resultado final: matches detectados |

---

## Dependencias

```bash
pip install pandas
```

También se requiere la herramienta [JARM](https://github.com/salesforce/jarm) para realizar el escaneo inicial de dominios.

---

## Contexto

Este proyecto fue desarrollado con fines de investigación y defensa. El objetivo es demostrar cómo el fingerprinting TLS puede ser utilizado como técnica de **threat hunting** pasiva para identificar infraestructura maliciosa activa en redes específicas, sin necesidad de acceso a los sistemas objetivo.

> **Nota:** JARM solo identifica la implementación TLS. Un match no confirma actividad maliciosa por sí solo; debe correlacionarse con otros indicadores de compromiso (IoCs).

---

## Referencias

- [JARM – Salesforce Security](https://github.com/salesforce/jarm)
- [C2-JARM fingerprint list](https://github.com/cedowens/C2-JARM)
- [Introducción a JARM – Salesforce Engineering Blog](https://engineering.salesforce.com/easily-identify-malicious-servers-on-the-internet-with-jarm-e095edac525a/)
