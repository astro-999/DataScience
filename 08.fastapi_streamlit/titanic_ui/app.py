import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Titanic Insight Engine",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = "http://127.0.0.1:8000"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: #f5f7fa;
    color: #1a1a2e;
}

/* Hide sidebar and its toggle button entirely */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 24px !important;
    border: 1px solid #e8ecf0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    box-shadow: 0 6px 24px rgba(79,70,229,0.14);
    transform: translateY(-3px);
}
div[data-testid="stMetricLabel"] > div {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #6b7280 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
div[data-testid="stMetricValue"] > div {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #4f46e5 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: #ffffff !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: opacity 0.2s ease, transform 0.2s ease;
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-2px); }

hr { border-color: #e8ecf0 !important; }

h2, h3 { color: #111827 !important; font-weight: 700 !important; }

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub { font-size: 1rem; color: #6b7280; margin-bottom: 24px; }
</style>
""", unsafe_allow_html=True)

# ── Chart palette & shared layout ─────────────────────────────────────────────
PALETTE = ["#4f46e5", "#7c3aed", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"]
CHART_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#374151"),
    margin=dict(l=10, r=10, t=46, b=10),
)

# ── Cached API helpers ────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def api_get(endpoint: str):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def api_post(endpoint: str, payload: dict):
    try:
        r = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


# ── Hero header ───────────────────────────────────────────────────────────────
hdr_col, btn_col = st.columns([8, 1])
with hdr_col:
    st.markdown('<p class="hero-title">🚢 Titanic Insight Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Exploratory data analysis and survival prediction from the 1912 Titanic passenger records.</p>', unsafe_allow_html=True)
with btn_col:
    st.write("")
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

# ── KPI Metrics ───────────────────────────────────────────────────────────────
summary = api_get("/stats/summary")
if summary:
    c1, c2, c3 = st.columns(3)
    c1.metric("🛟 Survival Rate", f"{summary['survival_rate']}%")
    c2.metric("🎂 Average Age", f"{summary['avg_age']} yrs")
    c3.metric("🧳 Total Passengers", f"{summary['total_passengers']:,}")
else:
    st.error("⚠️ Cannot reach the FastAPI backend on port 8000. Run: `uv run fastapi dev api.py --port 8000`")

st.divider()
st.markdown("### 📊 Survival Analysis")

# ── Row 1 ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    data = api_get("/analysis/survival-by-class")
    if data:
        df_cls = pd.DataFrame(data)
        df_cls["Class"] = df_cls["Pclass"].map({1: "1st Class", 2: "2nd Class", 3: "3rd Class"})
        fig = px.bar(
            df_cls, x="Class", y="Survived",
            title="Survival Rate by Ticket Class",
            color="Class",
            color_discrete_sequence=PALETTE,
            text_auto=".0%",
            labels={"Survived": "Survival Rate"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_yaxes(tickformat=".0%", range=[0, 1.15])
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig)

with col2:
    data = api_get("/analysis/survival-by-sex")
    if data:
        df_sex = pd.DataFrame(data)
        df_sex["Gender"] = df_sex["Sex"].str.capitalize()
        fig = px.pie(
            df_sex, values="Survived", names="Gender",
            title="Survival Distribution by Gender",
            hole=0.55,
            color_discrete_sequence=[PALETTE[0], PALETTE[2]],
        )
        fig.update_traces(textposition="outside", textinfo="label+percent")
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig)

# ── Row 2 ─────────────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    data = api_get("/analysis/age-dist")
    if data:
        fig = px.histogram(
            data["ages"], nbins=30,
            title="Passenger Age Distribution",
            color_discrete_sequence=[PALETTE[0]],
            labels={"value": "Age", "count": "Count"},
        )
        fig.update_traces(marker_line_color="white", marker_line_width=0.5)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig)

with col4:
    data = api_get("/analysis/survival-by-port")
    if data:
        df_port = pd.DataFrame(data)
        df_port["Port"] = df_port["Embarked"].map(
            {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}
        )
        fig = px.bar(
            df_port, x="Port", y="Survived",
            title="Survival Rate by Port of Embarkation",
            color="Port",
            color_discrete_sequence=PALETTE,
            text_auto=".0%",
            labels={"Survived": "Survival Rate"},
        )
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_yaxes(tickformat=".0%", range=[0, 1.15])
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig)

st.divider()

# ── Predictor ─────────────────────────────────────────────────────────────────
st.markdown("### 🔮 Survival Predictor")
st.markdown("Enter passenger details to estimate their probability of survival.")

with st.form("predict_form"):
    p1, p2, p3 = st.columns(3)

    with p1:
        pclass = st.selectbox(
            "Ticket Class", [1, 2, 3],
            format_func=lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd'} Class",
        )
        sex = st.radio("Gender", ["male", "female"], horizontal=True)

    with p2:
        age   = st.slider("Age", 0, 100, 28)
        sibsp = st.number_input("Siblings / Spouses Aboard", 0, 10, 0)

    with p3:
        parch     = st.number_input("Parents / Children Aboard", 0, 10, 0)
        st.write("")
        submitted = st.form_submit_button("Run Prediction →", use_container_width=True)

if submitted:
    payload = {"Pclass": pclass, "Sex": sex, "Age": age, "SibSp": sibsp, "Parch": parch}
    res = api_post("/predict", payload)

    if res:
        prob  = res.get("survival_probability", 0)
        clr   = "#10b981" if prob >= 0.5 else "#ef4444"

        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(prob * 100, 1),
            delta={"reference": 50, "suffix": "%"},
            title={"text": "Survival Probability", "font": {"size": 18, "family": "Inter", "color": "#374151"}},
            gauge={
                "axis": {"range": [0, 100], "ticksuffix": "%", "tickcolor": "#9ca3af"},
                "bar": {"color": clr},
                "bgcolor": "#f3f4f6",
                "bordercolor": "#e8ecf0",
                "steps": [
                    {"range": [0, 50],   "color": "#fee2e2"},
                    {"range": [50, 100], "color": "#d1fae5"},
                ],
                "threshold": {
                    "line": {"color": "#374151", "width": 3},
                    "thickness": 0.8,
                    "value": 50,
                },
            },
        ))
        fig_g.update_layout(
            height=300,
            margin=dict(l=30, r=30, t=60, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig_g)

        if prob >= 0.5:
            st.balloons()
            st.success(f"✅ Likely to Survive — confidence **{prob:.1%}**")
        else:
            st.error(f"❌ Unlikely to Survive — survival probability **{prob:.1%}**")
    else:
        st.warning("⚠️ Prediction service unavailable. Ensure the API is running.")