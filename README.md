
# HERMES v0.1 — OSINT Tool

  **Autor:** Manuel Mera ([@JetZ0](https://github.com/JetZ00))  
  **Formación:** Estudiante de Ingeniería del Software — Universidad de Málaga  
  **Colaborador:** Un amable asistente de IA, ChatGPT (GPT-6)  
  **Tipo:** Proyecto personal y educativo  
  **Tecnología:** Python

## Descripción general

HERMES es una herramienta OSINT desarrollada en Python
para recopilar información pública sobre dominios.

## Objetivo educativo

He desarrollado esta herramienta apoyándome en los conocimientos adquiridos durante mis estudios de Ingeniería del Software, especialmente en la asignatura de Redes y Servicios Distribuidos, y con la colaboración de un asistente de inteligencia artificial.

Mi objetivo es aprender sobre el desarrollo de herramientas OSINT en Python y explorar, de cara al futuro, cómo dirigir y colaborar con agentes de inteligencia artificial en el desarrollo de software.

Es mi primera herramienta relacionada con este ámbito y, sin duda, supone un antes y un después en mi formación como ingeniero.

Sin embargo, no desarrollo HERMES con fines laborales. Sinceramente, no tengo la certeza de que, en el futuro, muchos de nuestros trabajos no terminen siendo realizados por sistemas autónomos.

Entonces, ¿para qué?

**Para aprender, pensar y jugar.**

Si se pincha el globo, recordemos cómo se inflaba; así, la vocación del informático será eterna =)

## Funcionalidades

  ### DNS Intelligence
  - Validación básica de dominios ASCII.
  - Consulta de registros A (IPv4).
  - Consulta de registros AAAA (IPv6).
  - Consulta de registros MX.
  - Consulta de registros NS.
  - Consulta de registros TXT.
  - Gestión de errores de resolución DNS.
  - Exportación de resultados a JSON.
  - Fecha de consulta en UTC.

  ### RDAP Intelligence

- Descubrimiento automático de servidores RDAP mediante el registro oficial de IANA.
- Consulta de información pública de registro de dominios.
- Identificación del registrador.
- Obtención de fechas de creación, expiración y última modificación, cuando estén disponibles.
- Consulta de estados del dominio.
- Identificación de servidores de nombres.
- Gestión básica de errores HTTP y de conexión.
- Integración de los resultados RDAP y DNS en un único informe JSON.

## Requisitos
- Python 3.10 o superior.
- Biblioteca dnspython.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/JetZ00/HERMES.git
cd HERMES
```

Crear un entorno virtual:

```bash
python -m venv mi_python
```

Activarlo en Windows PowerShell:

```powershell
.\mi_python\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Uso

Ejecutar:

```bash
python main.py example.com
```

HERMES mostrará los registros DNS encontrados
y guardará un informe en la carpeta `results/`.

## Testing

Para ejecutar las pruebas automáticas:

```bash
python -m unittest discover -s tests -v
```

La batería actual contiene 21 tests.

## Estructura de los informes

Cada informe incluye:

- Dominio consultado.
- Fecha y hora de consulta en UTC.
- Tipos de registros DNS consultados.
- Estado de cada consulta.
- Registros obtenidos.

## Limitaciones actuales

- Solo admite dominios ASCII.
- No realiza consultas RDAP.
- Las consultas DNS dependen de la conectividad de red.

## Próximas funcionalidades

- RDAP Intelligence.
- Información sobre registradores.
- Fechas de registro y expiración, cuando estén disponibles.
- Mejoras de la interfaz de terminal.

## Aviso

HERMES está diseñado para consultar información
pública de dominios con fines educativos y de
investigación OSINT.
