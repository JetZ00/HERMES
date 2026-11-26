
# HERMES v0.1 — OSINT Tool

  **Autor:** Manuel Mera ([@JetZ00](https://github.com/JetZ00))  
  **Formación:** Estudiante de Ingeniería del Software — Universidad de Málaga   
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
### Problemas de activación del entorno virtual en Windows

En algunos equipos Windows, PowerShell puede impedir la activación del entorno virtual porque la ejecución de scripts está deshabilitada.

Al ejecutar:

```powershell
.\mi_python\Scripts\Activate.ps1
```

Puede aparecer el siguiente error:

```text
PSSecurityException: UnauthorizedAccess
La ejecución de scripts está deshabilitada en este sistema.
```

**Solución 1: Permitir temporalmente la ejecución de scripts**

En PowerShell, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después, activar nuevamente el entorno virtual:

```powershell
.\mi_python\Scripts\Activate.ps1
```

Este cambio afecta únicamente a la sesión actual de PowerShell. Al cerrar la terminal, deja de aplicarse. Se recomienda utilizarlo únicamente con scripts de confianza.

**Solución 2: Ejecutar HERMES sin activar el entorno virtual (recomendada)**

No es obligatorio activar el entorno virtual para utilizarlo. Podemos ejecutar directamente su intérprete de Python:

```powershell
.\mi_python\Scripts\python.exe -m pip install -r requirements.txt
.\mi_python\Scripts\python.exe main.py google.com
```

Esta opción permite instalar las dependencias y ejecutar HERMES sin modificar la política de ejecución de PowerShell.

**Nota:** Este comportamiento es una restricción de PowerShell, no un error del código de HERMES. Su activación y compatibilidad con diferentes entornos Windows podrán revisarse en futuras versiones.

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
