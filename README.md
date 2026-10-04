# PsicoTurnos MVP

API backend para gestionar solicitudes de turnos de psicomotricidad. El MVP utiliza **FastAPI**, **Google Gemini** para extraer información de las solicitudes y **MongoDB Atlas** para la persistencia de datos.

Repositorio: https://github.com/Bianca-GY/psicoturnos-mvp

## 1. Historias de Usuario

### HU-01 — Solicitar un turno

**Como** paciente o familiar de un paciente,
**quiero** enviar una solicitud de turno indicando mi nombre y la necesidad de atención,
**para** que el sistema pueda analizar la solicitud y registrar los datos relevantes.

#### Criterios de Aceptación — Gherkin

```gherkin
Característica: Crear una solicitud de turno

Escenario: Registrar correctamente una solicitud
  Dado que la API está disponible
  Y el servicio de IA devuelve correctamente los datos de la solicitud
  Cuando envío un POST a /appointments/ con el nombre del paciente y la descripción de la necesidad
  Entonces la API debe responder con código 200
  Y debe devolver un identificador del turno
  Y el estado del turno debe ser "Confirmado"
  Y los datos deben quedar persistidos en MongoDB Atlas
```

### HU-02 — Consultar estadísticas de turnos

**Como** profesional o administrador,
**quiero** consultar la cantidad total de turnos y su distribución por tipo de consulta,
**para** obtener una visión resumida de las solicitudes registradas.

#### Criterios de Aceptación — Gherkin

```gherkin
Característica: Consultar estadísticas de turnos

Escenario: Obtener estadísticas de las solicitudes registradas
  Dado que existen solicitudes de turnos almacenadas
  Cuando consulto GET /appointments/stats/
  Entonces la API debe responder con código 200
  Y debe informar el total de solicitudes
  Y debe informar la cantidad de solicitudes por tipo de consulta
```

## 2. Arquitectura

```text
                    +----------------+
                    |    Cliente     |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |    FastAPI     |
                    |    REST API    |
                    +---+--------+---+
                        |        |
                        v        v
                +---------+  +----------------+
                | Gemini  |  | MongoDB Atlas  |
                |   IA    |  | Persistencia   |
                +---------+  +----------------+
```

La aplicación mantiene una separación básica de responsabilidades:

* `app/main.py`: expone los endpoints de la API.
* `app/services/ai_service.py`: encapsula la integración con Google Gemini.
* `app/database.py`: encapsula el acceso asíncrono a MongoDB Atlas.
* `app/config.py`: centraliza la configuración y las variables de entorno.
* `tests/`: contiene las pruebas automatizadas.

### Fase 5 — Arquitectura Cloud

Para un despliegue inicial en producción conviene utilizar un modelo **PaaS (Platform as a Service)** para la API, acompañado de **MongoDB Atlas** como base de datos gestionada.

El modelo PaaS permite desplegar la aplicación FastAPI sin administrar directamente máquinas virtuales, sistemas operativos, actualizaciones y buena parte de la infraestructura. También facilita la configuración de variables de entorno, los reinicios y el escalado de la aplicación.

MongoDB Atlas complementa este enfoque proporcionando una base de datos gestionada en la nube, evitando que la aplicación tenga que administrar directamente la infraestructura del servidor de base de datos.

Un enfoque **Serverless** también sería posible, especialmente si la aplicación evolucionara hacia funciones independientes y ejecución bajo demanda. Sin embargo, para este MVP la API está diseñada como una aplicación FastAPI tradicional, por lo que PaaS resulta una alternativa más sencilla y adecuada.

**IaaS (Infrastructure as a Service)** proporcionaría mayor control sobre servidores y configuración de infraestructura, pero implicaría mayores tareas de administración y mantenimiento, que no son necesarias para este proyecto.

## 3. Requisitos

* Python 3.12 o superior compatible con las dependencias.
* Una cuenta de MongoDB Atlas y un clúster.
* Un usuario de base de datos de MongoDB.
* Una clave de API de Google Gemini.

La aplicación utiliza el cliente asíncrono de PyMongo para comunicarse con MongoDB.

## 4. Configuración local

### 4.1 Clonar el repositorio

```bash
git clone https://github.com/Bianca-GY/psicoturnos-mvp.git
cd psicoturnos-mvp
```

### 4.2 Crear el entorno virtual

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4.4 Configurar las variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
MONGODB_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/?appName=Cluster0
MONGODB_DB_NAME=psicoturnos
MONGODB_COLLECTION_NAME=appointments
GEMINI_API_KEY=<tu-clave-de-gemini>
```

**No subir el archivo `.env` a GitHub.** El archivo está excluido mediante `.gitignore`.

### 4.5 Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La documentación interactiva de FastAPI estará disponible en:

```text
http://127.0.0.1:8000/docs
```

## 5. Persistencia

La aplicación utiliza **MongoDB Atlas** como motor de persistencia.

Los turnos se almacenan en la colección `appointments` de la base de datos `psicoturnos`.

La implementación utiliza `AsyncMongoClient`, permitiendo realizar las operaciones de persistencia de manera asíncrona y compatible con FastAPI.

Durante las pruebas automatizadas, las operaciones de base de datos se reemplazan mediante mocks. De esta manera, los tests no necesitan conectarse a MongoDB Atlas ni utilizar credenciales reales.

## 6. Calidad, seguridad y pruebas

Las herramientas utilizadas para el control de calidad y seguridad son:

* **Flake8**: análisis estático y control de estilo.
* **Bandit**: análisis básico de seguridad del código Python.
* **Pytest**: ejecución de las pruebas automatizadas.

Para ejecutar las verificaciones localmente:

```bash
flake8 app tests
```

```bash
bandit -r app -ll
```

```bash
pytest -q
```

La suite de pruebas mockea tanto el servicio de inteligencia artificial como las operaciones de MongoDB. Esto permite ejecutar las pruebas sin depender de servicios externos.

## 7. Integración Continua y Shift Left

El proyecto utiliza **GitHub Actions** mediante el archivo:

```text
.github/workflows/ci.yml
```

El pipeline se ejecuta automáticamente ante:

* `push`
* `pull_request`

El workflow realiza las siguientes tareas:

1. Descarga el código del repositorio.
2. Configura Python 3.12.
3. Instala las dependencias.
4. Ejecuta Flake8.
5. Ejecuta Bandit.
6. Ejecuta Pytest.

El objetivo es aplicar el enfoque **Shift Left**, detectando problemas de calidad, seguridad y funcionamiento lo antes posible dentro del ciclo de desarrollo, antes de integrar cambios a la rama principal.

## 8. Flujo GitHub Flow

El desarrollo se organiza mediante una rama principal y ramas secundarias para implementar correcciones o nuevas funcionalidades.

Ejemplo:

```bash
git checkout -b feature/mongodb-atlas
```

Realizar los cambios y luego:

```bash
git add .
git commit -m "feat: conectar persistencia con MongoDB Atlas"
```

Subir la rama:

```bash
git push -u origin feature/mongodb-atlas
```

Luego se crea un **Pull Request** hacia `main`.

El pipeline de GitHub Actions debe finalizar correctamente antes de integrar los cambios a la rama principal.

## 9. Endpoints principales

| Método | Endpoint               | Descripción                        |
| ------ | ---------------------- | ---------------------------------- |
| GET    | `/`                    | Verifica que la API esté operativa |
| POST   | `/appointments/`       | Crea una solicitud de turno        |
| GET    | `/appointments/stats/` | Devuelve estadísticas de turnos    |

## 10. Estructura principal del proyecto

```text
psicoturnos-mvp/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   ├── models.py
│   └── services/
│       ├── __init__.py
│       └── ai_service.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_tdd_feature.py
├── .gitignore
├── README.md
└── requirements.txt
```
