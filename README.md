<div align="center">

# HelpDesk AI ⚙️

### Base de conocimiento local impulsada por IA y RAG (Retrieval-Augmented Generation)

[![Next.js](https://img.shields.io/badge/Next.js_16-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Ollama](https://img.shields.io/badge/Ollama_AI-FFFFFF?style=for-the-badge&logo=ollama&logoColor=black)](https://ollama.com/)
[![Podman](https://img.shields.io/badge/Podman_Compose-892CA0?style=for-the-badge&logo=podman&logoColor=white)](https://podman.io/)

</div>

---

## 📋 Descripción General

**HelpDesk AI** es una aplicación de base de conocimiento local impulsada por Inteligencia Artificial y la arquitectura RAG (Retrieval-Augmented Generation). Permite a los usuarios cargar manuales técnicos en formato PDF, procesarlos de manera local y realizar consultas en lenguaje natural, obteniendo respuestas precisas basadas estrictamente en los documentos proporcionados.

Diseñado con un enfoque de privacidad y eficiencia, todo el procesamiento vectorial y de inferencia LLM se ejecuta localmente a través de contenedores, optimizado para entornos con restricciones de hardware (como sistemas con 8 GB de RAM).

---

## 🚀 Características Principales

* **Procesamiento de Documentos:** Extracción y fragmentación automática de texto desde archivos PDF.
* **Búsqueda Semántica:** Generación de embeddings locales para buscar el contexto más relevante dentro de los manuales.
* **Generación Aumentada (RAG):** Respuestas contextualizadas con citas directas al documento de origen utilizando un LLM ligero.
* **Privacidad Total:** 100% autohospedado, sin llamadas a APIs externas de IA.
* **Arquitectura Contenerizada:** Despliegue unificado mediante Podman Compose.

---

## 🏗️ Arquitectura y Stack Tecnológico

| Capa | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Frontend** | Next.js 16 + React | Interfaz de usuario (App Router) y subida de documentos |
| **Estilos & UI** | Tailwind CSS | Diseño responsivo e interactivo |
| **Backend API** | Python + FastAPI | API RESTful, procesamiento de PDFs (PyPDF) y orquestación RAG (LangChain) |
| **ORM & Datos** | SQLAlchemy + Alembic | Persistencia relacional y migraciones de base de datos |
| **Base de Datos** | PostgreSQL + pgvector | Almacenamiento de metadatos y vectores matemáticos de texto |
| **Motor de IA** | Ollama | Ejecución de modelos locales (`qwen2.5:0.5b` y `nomic-embed-text`) |
| **Infraestructura** | Podman Compose + WSL2 | Orquestación de contenedores en Windows |

---

## 📋 Requisitos Previos

* **Podman Desktop** instalado y configurado con WSL2.
* Al menos **8 GB de memoria RAM** (Se recomienda cerrar aplicaciones en segundo plano durante la inferencia para evitar problemas de OOM en WSL).
* **Git**.

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd HelpDesk-AI
```

### 2. Levantar la infraestructura

Inicia todos los servicios en segundo plano utilizando Podman Compose:

```bash
podman compose up -d
```

### 3. Inicializar la Base de Datos

Ejecuta las migraciones de Alembic dentro del contenedor del backend para construir la estructura relacional (`documents`, etc.):

```bash
podman exec -it helpdesk_backend alembic upgrade head
```

### 4. Descargar los Modelos de IA locales

Instruye a Ollama para que descargue los modelos necesarios para los embeddings y la generación de texto:

```bash
podman exec -it helpdesk_ollama ollama pull nomic-embed-text
podman exec -it helpdesk_ollama ollama pull qwen2.5:0.5b
```

---

## 🖥️ Uso

1. Abre tu navegador web e ingresa a `http://localhost:8080`.
2. Utiliza el botón **"+ Subir Manual (PDF)"** para cargar un documento a la base de conocimiento.
3. Espera a que el sistema indique que el procesamiento ha finalizado.
4. En la barra inferior, escribe una pregunta relacionada con el manual (ej. *"¿Cuál es el principio SSS?"*) y haz clic en **"Consultar AI"**.

---

## 🛑 Solución de Problemas Frecuentes

* **Error `exit status 0xffffffff
