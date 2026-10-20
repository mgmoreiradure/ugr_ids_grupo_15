"""
App Streamlit — Predicción de Churn en Telecomunicaciones
TP de Ingeniería del Software — UGR Lic. en Ciencia de Datos (CCC)

Uso local:
    streamlit run app.py

Despliegue:
    Streamlit Community Cloud → https://share.streamlit.io
"""
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ---------- Configuración de página ----------
st.set_page_config(
    page_title="Predictor de Churn — Telco",
    page_icon="📞",
    layout="centered",
)

# ---------- Carga del modelo (cacheada) ----------
@st.cache_resource
def cargar_modelo(path: str = "modelo_churn.joblib"):
    artefacto = joblib.load(path)
    return artefacto["model"], artefacto["columns"], artefacto.get("model_name", "modelo")


modelo, columnas_modelo, nombre_modelo = cargar_modelo()

# ---------- Encabezado ----------
st.title("📞 Predictor de fuga de clientes (Churn)")
st.caption(
    "TP de Ingeniería del Software — Lic. en Ciencia de Datos (UGR). "
    f"Modelo subyacente: **{nombre_modelo}**."
)

st.markdown(
    "Ingresá los datos del cliente para estimar la **probabilidad de que cancele el servicio**. "
    "Un valor alto permite priorizarlo en campañas de retención."
)

# ---------- Formulario ----------
with st.form("formulario_cliente"):
    st.subheader("🧑 Datos demográficos")
    c1, c2 = st.columns(2)
    gender = c1.selectbox("Género", ["Female", "Male"])
    senior = c2.selectbox("¿Es adulto mayor?", ["No", "Yes"])
    partner = c1.selectbox("¿Tiene pareja?", ["No", "Yes"])
    dependents = c2.selectbox("¿Tiene personas a cargo?", ["No", "Yes"])

    st.subheader("📅 Contrato")
    c1, c2 = st.columns(2)
    tenure = c1.slider("Antigüedad como cliente (meses)", 0, 72, 12)
    contract = c2.selectbox("Tipo de contrato", ["Month-to-month", "One year", "Two year"])
    paperless = c1.selectbox("Facturación digital", ["Yes", "No"])
    payment = c2.selectbox(
        "Método de pago",
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
    )

    st.subheader("📶 Servicios")
    c1, c2, c3 = st.columns(3)
    phone = c1.selectbox("Línea telefónica", ["Yes", "No"])
    multiple = c2.selectbox("Múltiples líneas", ["No", "Yes"])
    internet = c3.selectbox("Internet", ["DSL", "Fiber optic", "No"])

    c1, c2, c3 = st.columns(3)
    online_sec = c1.selectbox("Seguridad online", ["No", "Yes"])
    online_bak = c2.selectbox("Backup online", ["No", "Yes"])
    dev_prot = c3.selectbox("Protección de equipos", ["No", "Yes"])

    c1, c2, c3 = st.columns(3)
    tech_sup = c1.selectbox("Soporte técnico", ["No", "Yes"])
    stream_tv = c2.selectbox("Streaming TV", ["No", "Yes"])
    stream_mv = c3.selectbox("Streaming Películas", ["No", "Yes"])

    st.subheader("💲 Cargos")
    c1, c2 = st.columns(2)
    monthly = c1.number_input("Cargo mensual (USD)", min_value=0.0, max_value=200.0, value=70.0, step=1.0)
    total = c2.number_input("Cargo total acumulado (USD)", min_value=0.0, value=float(monthly * max(tenure, 1)), step=10.0)

    submit = st.form_submit_button("🔮 Predecir", type="primary", use_container_width=True)


# ---------- Lógica de predicción ----------
def construir_feature_vector(datos: dict) -> pd.DataFrame:
    """Replica el preprocesamiento del training."""
    df = pd.DataFrame([datos])
    # One-hot encoding con drop_first (igual que en el training)
    df_enc = pd.get_dummies(df, drop_first=True, dtype=int)
    # Alinear columnas al orden/espacio del modelo
    df_enc = df_enc.reindex(columns=columnas_modelo, fill_value=0)
    return df_enc


if submit:
    datos_cliente = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": online_sec,
        "OnlineBackup": online_bak,
        "DeviceProtection": dev_prot,
        "TechSupport": tech_sup,
        "StreamingTV": stream_tv,
        "StreamingMovies": stream_mv,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
    }

    X_cliente = construir_feature_vector(datos_cliente)
    prob_churn = float(modelo.predict_proba(X_cliente)[0, 1])

    # Clasificación de riesgo.
    # Umbrales calibrados sobre la distribución real de predicciones del modelo
    # (entrenado con class_weight="balanced", por lo que las probabilidades
    # están desplazadas respecto a la base natural 73/27):
    #   • BAJO   (< 0.40): por debajo de la media de predicciones del dataset.
    #   • MEDIO  (0.40–0.60): zona de incertidumbre, requiere seguimiento.
    #   • ALTO   (≥ 0.60): clientes claramente por encima de la media de riesgo.
    if prob_churn >= 0.60:
        nivel, color, emoji = "ALTO", "red", "🚨"
    elif prob_churn >= 0.40:
        nivel, color, emoji = "MEDIO", "orange", "⚠️"
    else:
        nivel, color, emoji = "BAJO", "green", "✅"

    st.divider()
    st.subheader("📊 Resultado")
    c1, c2 = st.columns([1, 2])
    c1.metric("Probabilidad de churn", f"{prob_churn:.1%}")
    c2.markdown(f"### {emoji} Riesgo **:{color}[{nivel}]**")
    st.progress(prob_churn)

    # Interpretabilidad: top features del modelo (globales)
    with st.expander("🔍 Variables más influyentes del modelo (importancia global)"):
        if hasattr(modelo, "feature_importances_"):
            imp = (
                pd.Series(modelo.feature_importances_, index=columnas_modelo)
                .sort_values(ascending=False)
                .head(10)
            )
            st.bar_chart(imp)
        else:
            st.info("Este modelo no expone importancia de variables.")

    # Recomendación de acción
    st.divider()
    st.subheader("🎯 Acción sugerida")
    if nivel == "ALTO":
        st.error(
            "**Contactar al cliente en las próximas 48 h.** Ofrecer upgrade a contrato anual "
            "o descuento sobre el cargo mensual. Priorizar en la cola del equipo de retención."
        )
    elif nivel == "MEDIO":
        st.warning(
            "**Monitorear próximas interacciones.** Enviar encuesta de satisfacción y, si hay "
            "reclamos recientes, incluir en campaña de retención suave (ej. beneficios digitales)."
        )
    else:
        st.success(
            "**Cliente estable.** No requiere acción inmediata. Considerar oportunidades de "
            "cross-sell/upsell si corresponde."
        )

# ---------- Footer ----------
st.divider()
st.caption("Dataset: IBM Telco Customer Churn · Metodología: CRISP-DM · Stack: scikit-learn + Streamlit")
