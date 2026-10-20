# TP Ingeniería del Software — UGR

Predicción de fuga de clientes (Churn) en una empresa de telecomunicaciones.
Metodología **CRISP-DM** aplicada sobre el dataset público **Telco Customer Churn** (IBM).

## Contenido del proyecto

| Archivo | Qué es |
|---|---|
| `UGR_IdS_TP.ipynb` | Notebook con las 6 fases de CRISP-DM resueltas. |
| `app.py` | Aplicación Streamlit con el formulario de predicción. |
| `modelo_churn.joblib` | Modelo Random Forest entrenado (listo para usar). |
| `Telco-Customer-Churn.csv` | Dataset de 7043 clientes. |
| `requirements.txt` | Dependencias de Python. |

---

## Paso a paso para la entrega

### 1 · Preparar la notebook

1. Abrir `UGR_IdS_TP.ipynb` en Jupyter o Google Colab.
2. **Completar los nombres de los 8 estudiantes** en la primera celda (donde dice `Estudiante 1 … Estudiante 8`).
3. Ejecutar la notebook **de arriba abajo** (`Cell → Run All` en Jupyter, o `Runtime → Run all` en Colab). Esto hace que las tablas y los gráficos queden guardados dentro del archivo.
4. Guardar el `.ipynb`.

> **Si usan Colab:** subir el `.csv` y el `modelo_churn.joblib` al entorno antes de correr, o cambiar la línea de carga del CSV para que lea de la URL (ya está contemplada en la Fase 2).

---

### 2 · Crear la cuenta y el repositorio en GitHub

Si no tenés cuenta en GitHub:

1. Entrar a <https://github.com/signup> y crear una cuenta (gratis).
2. Verificar el email.

Crear el repositorio:

1. Entrar a <https://github.com/new>
2. Completar:
   - **Repository name:** `tp-ids-churn` (o el nombre que quieran).
   - **Public** (tiene que ser público para que Streamlit Community Cloud lo pueda leer gratis).
   - **NO tildar** "Add a README" ni "Add .gitignore" (ya los traemos nosotros).
3. Click en **Create repository**.
4. GitHub les va a mostrar la URL del repo, algo como `https://github.com/TU-USUARIO/tp-ids-churn.git`. **Copiarla**, la vamos a usar en el próximo paso.

---

### 3 · Subir el proyecto a GitHub

Abrir una terminal en la carpeta del proyecto (`/home/mario/work/own/facu/ingenieria`) y ejecutar:

```bash
# 1) Inicializar git
git init

# 2) Configurar tu nombre y email (solo la primera vez)
git config user.name  "Tu Nombre"
git config user.email "tu@mail.com"

# 3) Agregar un .gitignore para no subir el venv ni archivos basura
cat > .gitignore <<'EOF'
.venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
.DS_Store
EOF

# 4) Agregar todos los archivos y hacer el primer commit
git add .
git commit -m "TP IdS: Predictor de Churn (CRISP-DM + Streamlit)"

# 5) Conectar con el repo remoto (reemplazar la URL por la tuya)
git branch -M main
git remote add origin https://github.com/TU-USUARIO/tp-ids-churn.git

# 6) Subir
git push -u origin main
```

> La primera vez te va a pedir usuario/token de GitHub. Si pide contraseña y falla:
> - Ir a <https://github.com/settings/tokens> → **Generate new token (classic)** → marcar el scope `repo` → generar → usar ese token como contraseña.

Verificar que el push funcionó: entrar a `https://github.com/TU-USUARIO/tp-ids-churn` y confirmar que están todos los archivos.

---

### 4 · Desplegar en Streamlit Community Cloud

1. Entrar a <https://share.streamlit.io/> y hacer click en **"Sign in with GitHub"**. Autorizar el acceso.
2. Click en **"New app"** (o **"Create app"**).
3. Completar:
   - **Repository:** `TU-USUARIO/tp-ids-churn`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL** *(opcional)*: elegir un slug como `tp-churn-ugr` → la app quedará en `https://tp-churn-ugr.streamlit.app`.
4. Click en **"Deploy"**.
5. Esperar ~2 minutos mientras Streamlit instala las dependencias (lee `requirements.txt` solo).
6. Cuando termine, van a ver la app en vivo. **Copiar la URL pública.**

> **Si falla el build:** mirar los logs que aparecen en la misma página; lo más común es que falte una dependencia en `requirements.txt`.

---

### 5 · Pegar el link del deploy en la notebook

1. Abrir `UGR_IdS_TP.ipynb`.
2. Buscar la **Fase 6** → sección *"Acceso al software desplegado"*.
3. Reemplazar `<PENDIENTE DE DESPLIEGUE>` por la URL copiada en el paso anterior.
4. Guardar.
5. Opcional: pushear el cambio al repo (`git add . && git commit -m "Add deploy URL" && git push`).

---

### 6 · (Opcional) Agregar capturas de pantalla

En la Fase 6 hay un bloque que referencia `imagenes/01_formulario.png`, etc.

1. Abrir la app desplegada en el navegador.
2. Sacar 3 capturas: formulario vacío, resultado de un cliente de alto riesgo, resultado de uno de bajo riesgo.
3. Crear una carpeta `imagenes/` en el proyecto, poner los PNG con esos nombres.
4. `git add imagenes/ && git commit -m "Add screenshots" && git push`.

---

### 7 · Entrega

Lo que se sube al aula virtual / se le pasa al profe:

- La notebook `UGR_IdS_TP.ipynb` (con los nombres completos y todas las celdas ejecutadas).
- El link a la app desplegada en Streamlit (`https://xxx.streamlit.app`).

El código fuente queda público en GitHub por si lo quieren revisar.

---

## Correr la app localmente (opcional, para probar antes de deployar)

```bash
# Crear venv y activar
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias (usar requirements.txt — versiones pinneadas)
pip install -r requirements.txt

# Levantar la app
streamlit run app.py
```

Streamlit va a abrir `http://localhost:8501` en el navegador.

> **Importante:** las versiones en `requirements.txt` están **pinneadas con `==`** (no `>=`). Esto es a propósito: el modelo `modelo_churn.joblib` fue serializado con scikit-learn 1.9.1 y los pickles de sklearn **no son forward-compatible** entre versiones mayores. Si alguien del grupo quiere trabajar con otras versiones, hay que **re-entrenar** el modelo y volver a guardar el `.joblib`.

---

## Troubleshooting

| Problema | Solución |
|---|---|
| `git push` pide contraseña y falla | Usar un **Personal Access Token** (ver paso 3). |
| `modelo_churn.joblib` muy grande para pushear | Pesa 11 MB → debería entrar sin problemas (límite de GitHub: 100 MB por archivo). Si falla, verificar que no se esté subiendo el `.venv/`. |
| Streamlit falla con `ModuleNotFoundError` | Agregar la librería faltante a `requirements.txt` y hacer push nuevamente. |
| La notebook no muestra gráficos en GitHub | Ejecutar todas las celdas en Jupyter/Colab antes de guardar, para que los outputs queden embebidos. |
