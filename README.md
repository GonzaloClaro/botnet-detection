# JARM on the Chilean Network

A cybersecurity research project that applies TLS fingerprinting via **JARM** to identify potential Command and Control (C2) servers active among domains in the Chilean network.

The full study is documented in the included report: [`Uso de Jarm en dominios de la red chilena.pdf`](./Uso%20de%20Jarm%20en%20dominios%20de%20la%20red%20chilena.pdf)

---

## What is JARM?

[JARM](https://github.com/salesforce/jarm) is an active TLS fingerprinting tool developed by the Salesforce security team. It works by sending 10 specially crafted TLS handshakes to a server and hashing the responses to produce a unique 62-character fingerprint that identifies the server's SSL/TLS implementation.

This fingerprint is valuable because different C2 frameworks (Cobalt Strike, Metasploit, Mythic, Sliver, etc.) leave characteristic and reproducible TLS signatures, regardless of the domain or IP they are hosted on.

---

## Project Workflow

```
1. JARM scan of Chilean domains
        ↓
   resultado_jarm.csv
        ↓
2. Convert known C2 list (C2.txt → Servidores_C2.csv)
        ↓ raw_txt_to_csv.py
   Servidores_C2.csv
        ↓
3. Fingerprint cross-reference (inner join)
        ↓ jarm_chile.py
   Botnets_red_chilena.csv
```

### Step 1 – JARM Scan

The JARM tool was run against a list of `.cl` domains and other hosts active in the Chilean network, producing `resultado_jarm.csv` with the following columns:

| Domain | IP | JARM | TLS 1…10 |
|---|---|---|---|

### Step 2 – Prepare the known C2 list

`C2.txt` contains a table of JARM fingerprints for well-known C2 and red team tools (Cobalt Strike, Metasploit, Mythic, Sliver, Merlin, EvilGinx2, etc.), sourced from public threat intelligence.

```bash
python raw_txt_to_csv.py
# Produces: Servidores_C2.csv
```

### Step 3 – C2 Detection in the Chilean Network

```bash
python jarm_chile.py
# Produces: Botnets_red_chilena.csv
```

The script:
- Filters out domains that failed to resolve or returned a null JARM hash
- Performs an **inner join** between the scanned fingerprints and the known C2 database
- Exports matches with domain, IP, JARM hash, identified C2 tool, and timestamp

---

## Files

| File | Description |
|---|---|
| `jarm_chile.py` | Main detection script (fingerprint cross-reference) |
| `raw_txt_to_csv.py` | Converts `C2.txt` to a processable CSV |
| `C2.txt` | JARM fingerprint list of known C2/red team tools |
| `Uso de Jarm en dominios de la red chilena.pdf` | Full research report |

### Generated files (not included in repo)

| File | Description |
|---|---|
| `resultado_jarm.csv` | Output from the JARM scan over Chilean domains |
| `Servidores_C2.csv` | Known C2 list converted to CSV |
| `Botnets_red_chilena.csv` | Final output: detected matches |

---

## Dependencies

```bash
pip install pandas
```

The [JARM](https://github.com/salesforce/jarm) tool is also required to perform the initial domain scan.

---

## Context

This project was developed for research and defensive purposes. The goal is to demonstrate how TLS fingerprinting can be used as a passive **threat hunting** technique to identify malicious infrastructure active within specific networks, without requiring direct access to target systems.

> **Note:** JARM identifies TLS implementations only. A fingerprint match alone does not confirm malicious activity — it should be correlated with other indicators of compromise (IoCs).

---

## References

- [JARM – Salesforce Security](https://github.com/salesforce/jarm)
- [C2-JARM fingerprint list](https://github.com/cedowens/C2-JARM)
- [Introducing JARM – Salesforce Engineering Blog](https://engineering.salesforce.com/easily-identify-malicious-servers-on-the-internet-with-jarm-e095edac525a/)
