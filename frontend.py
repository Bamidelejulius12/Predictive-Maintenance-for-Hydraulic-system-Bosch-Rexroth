import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bosch Rexroth — Predictive Maintenance",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE = "http://localhost:8000/"

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0c10;
    color: #e2e8f0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 3rem 3rem; max-width: 1400px; }

/* ── Masthead ── */
.masthead {
    border-bottom: 1px solid #1e2530;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
}
.masthead-title {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #94a3b8;
}
.masthead-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #475569;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}
.masthead-timestamp {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #334155;
    letter-spacing: 0.08em;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent;
    border-bottom: 1px solid #1e2530;
    margin-bottom: 2.5rem;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
    padding: 0.75rem 2rem !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #e2e8f0 !important;
    border-bottom: 2px solid #3b82f6 !important;
    background: transparent !important;
}

/* ── Section labels ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.75rem;
    border-left: 2px solid #3b82f6;
    padding-left: 0.75rem;
}

/* ── Stat cards ── */
.stat-card {
    background: #0f1318;
    border: 1px solid #1e2530;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.5rem;
}
.stat-value {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    color: #e2e8f0;
}
.stat-unit {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #475569;
    margin-top: 0.3rem;
}

/* ── Status badges ── */
.badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border: 1px solid;
    margin-top: 0.75rem;
}
.badge-critical { color: #ef4444; border-color: #ef4444; background: rgba(239,68,68,0.08); }
.badge-warning  { color: #f97316; border-color: #f97316; background: rgba(249,115,22,0.08); }
.badge-caution  { color: #eab308; border-color: #eab308; background: rgba(234,179,8,0.08);  }
.badge-normal   { color: #22c55e; border-color: #22c55e; background: rgba(34,197,94,0.08);  }

/* ── Result block ── */
.result-block {
    background: #0f1318;
    border: 1px solid #1e2530;
    border-left: 3px solid #3b82f6;
    padding: 2rem 2.5rem;
    margin-top: 2rem;
}
.result-rul {
    font-size: 4rem;
    font-weight: 800;
    color: #e2e8f0;
    line-height: 1;
}
.result-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

/* ── Input overrides ── */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: #0f1318 !important;
    border: 1px solid #1e2530 !important;
    border-radius: 0 !important;
    color: #e2e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 0 !important;
    color: #3b82f6 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #3b82f6 !important;
    color: #0a0c10 !important;
}

/* ── Divider ── */
hr { border-color: #1e2530 !important; margin: 2rem 0 !important; }

/* ── Alert overrides ── */
.stAlert { border-radius: 0 !important; border-left-width: 3px !important; }

/* ── Dataframe ── */
.stDataFrame { font-family: 'DM Mono', monospace !important; font-size: 0.78rem !important; }

/* ── Metric ── */
[data-testid="metric-container"] {
    background: #0f1318;
    border: 1px solid #1e2530;
    padding: 1.25rem 1.5rem;
}
[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#0f1318",
    font=dict(family="DM Mono, monospace", color="#94a3b8", size=11),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor="#1e2530", linecolor="#1e2530", zerolinecolor="#1e2530"),
    yaxis=dict(gridcolor="#1e2530", linecolor="#1e2530", zerolinecolor="#1e2530"),
)

def get_status(rul_hours: float) -> tuple[str, str]:
    if rul_hours <= 24:   return "CRITICAL",  "badge-critical"
    if rul_hours <= 72:   return "WARNING",   "badge-warning"
    if rul_hours <= 168:  return "CAUTION",   "badge-caution"
    return                       "NORMAL",    "badge-normal"

def get_status_color(rul_hours: float) -> str:
    if rul_hours <= 24:  return "#ef4444"
    if rul_hours <= 72:  return "#f97316"
    if rul_hours <= 168: return "#eab308"
    return "#22c55e"

def call_predict(payload: dict) -> dict:
    return requests.post(f"{API_BASE}/predict", json=payload, timeout=30).json()

def call_train() -> dict:
    return requests.post(f"{API_BASE}/train", timeout=600).json()

# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="masthead">
    <div>
        <div class="masthead-title">Bosch Rexroth — Hydraulic System Intelligence</div>
        <div class="masthead-sub">Predictive Maintenance Platform / RandomForest RUL Model</div>
    </div>
    <div class="masthead-timestamp">{datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_predict, tab_fleet, tab_model = st.tabs([
    "RUL Prediction",
    "Fleet Overview",
    "Model & Training",
])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — RUL PREDICTION
with tab_predict:

    col_form, col_gap, col_result = st.columns([5, 1, 6])

    with col_form:
        st.markdown('<div class="section-label">Machine Identification</div>', unsafe_allow_html=True)
        machine_id = st.text_input("Machine ID", value="HPU_01", label_visibility="visible")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Live Sensor Readings</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            pressure    = st.number_input("Pressure (bar)",     min_value=50.0,  max_value=400.0, value=120.0, step=0.1)
            flow        = st.number_input("Flow Rate (L/min)",  min_value=0.0,   max_value=500.0, value=85.0,  step=0.1)
            vibration_x = st.number_input("Vibration X (g)",    min_value=0.0,   max_value=5.0,   value=0.34,  step=0.01)
        with c2:
            temp        = st.number_input("Temperature (C)",    min_value=20.0,  max_value=120.0, value=51.0,  step=0.1)
            pump_rpm    = st.number_input("Pump RPM",           min_value=100.0, max_value=3000.0,value=1474.0,step=1.0)
            vibration_y = st.number_input("Vibration Y (g)",    min_value=0.0,   max_value=5.0,   value=0.34,  step=0.01)

        st.markdown("<br>", unsafe_allow_html=True)

        run_btn = st.button("Run Prediction", use_container_width=True)

    with col_result:
        st.markdown('<div class="section-label">Prediction Output</div>', unsafe_allow_html=True)

        if run_btn:
            with st.spinner(""):
                try:
                    payload = {
                        "machine_id":    machine_id,
                        "pressure_bar":  pressure,
                        "temp_celsius":  temp,
                        "flow_lpm":      flow,
                        "vibration_x_g": vibration_x,
                        "vibration_y_g": vibration_y,
                        "pump_rpm":      pump_rpm,
                    }
                    resp = call_predict(payload)

                    rul_h  = resp.get("rul_hours", 0)
                    rul_d  = rul_h / 24
                    status, badge_cls = get_status(rul_h)
                    color  = get_status_color(rul_h)

                    # RUL display
                    st.markdown(f"""
                    <div class="result-block" style="border-left-color: {color}">
                        <div class="result-sub">Remaining Useful Life</div>
                        <div class="result-rul" style="color:{color}">{rul_h:.1f}</div>
                        <div class="result-sub">hours &nbsp;/&nbsp; {rul_d:.1f} days</div>
                        <div><span class="badge {badge_cls}">{status}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Gauge chart
                    max_rul = 1000
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=rul_h,
                        number={"suffix": " h", "font": {"size": 28, "color": "#e2e8f0", "family": "Syne"}},
                        gauge={
                            "axis": {"range": [0, max_rul], "tickcolor": "#475569",
                                     "tickfont": {"size": 10, "family": "DM Mono"}},
                            "bar":  {"color": color, "thickness": 0.25},
                            "bgcolor": "#0f1318",
                            "bordercolor": "#1e2530",
                            "steps": [
                                {"range": [0,    24],  "color": "rgba(239,68,68,0.12)"},
                                {"range": [24,   72],  "color": "rgba(249,115,22,0.08)"},
                                {"range": [72,   168], "color": "rgba(234,179,8,0.06)"},
                                {"range": [168,  max_rul], "color": "rgba(34,197,94,0.04)"},
                            ],
                            "threshold": {
                                "line": {"color": color, "width": 2},
                                "thickness": 0.8,
                                "value": rul_h,
                            },
                        },
                    ))
                    fig.update_layout(**PLOTLY_LAYOUT, height=280)
                    st.plotly_chart(fig, use_container_width=True)

                    # Secondary metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Machine", machine_id)
                    m2.metric("Machine Age", f"{resp.get('machine_age_days', 0):.0f} d")
                    m3.metric("Since Maint.", f"{resp.get('days_since_last_maintenance', 0):.0f} d")

                    # Store in session history
                    if "history" not in st.session_state:
                        st.session_state["history"] = []
                    st.session_state["history"].append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "machine_id": machine_id,
                        "rul_hours": round(rul_h, 1),
                        "status": status,
                        "pressure_bar": pressure,
                        "temp_celsius": temp,
                        "pump_rpm": pump_rpm,
                    })

                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach API. Ensure the FastAPI server is running on localhost:8000.")
                except Exception as e:
                    st.error(f"Prediction error: {e}")
        else:
            st.markdown("""
            <div style="border:1px solid #1e2530; padding:3rem 2rem; text-align:center; margin-top:2rem;">
                <div style="font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.2em;
                            text-transform:uppercase; color:#334155;">
                    Enter sensor readings and run prediction
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Prediction history table
    if "history" in st.session_state and st.session_state["history"]:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Session History</div>', unsafe_allow_html=True)
        hist_df = pd.DataFrame(st.session_state["history"])
        st.dataframe(hist_df, use_container_width=True, hide_index=True)


#  TAB 2 — FLEET OVERVIEW
with tab_fleet:

    st.markdown('<div class="section-label">Fleet Batch Assessment</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-family:'DM Mono',monospace; font-size:0.78rem; color:#475569; margin-bottom:1.5rem;">
    Upload a CSV with columns: machine_id, pressure_bar, temp_celsius, flow_lpm,
    vibration_x_g, vibration_y_g, pump_rpm
    </p>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload fleet sensor CSV", type=["csv"], label_visibility="collapsed")

    if uploaded:
        fleet_df = pd.read_csv(uploaded)
        required = {"machine_id","pressure_bar","temp_celsius","flow_lpm",
                    "vibration_x_g","vibration_y_g","pump_rpm"}

        if not required.issubset(fleet_df.columns):
            st.error(f"Missing columns: {required - set(fleet_df.columns)}")
        else:
            if st.button("Assess Fleet", use_container_width=False):
                results = []
                progress = st.progress(0)
                for i, row in fleet_df.iterrows():
                    try:
                        resp = call_predict(row[list(required)].to_dict())
                        results.append({
                            "machine_id":   row["machine_id"],
                            "rul_hours":    round(resp.get("rul_hours", 0), 1),
                            "status":       get_status(resp.get("rul_hours", 0))[0],
                        })
                    except Exception:
                        results.append({"machine_id": row["machine_id"], "rul_hours": None, "status": "ERROR"})
                    progress.progress((i + 1) / len(fleet_df))

                results_df = pd.DataFrame(results).sort_values("rul_hours")
                st.session_state["fleet_results"] = results_df

    if "fleet_results" in st.session_state:
        res = st.session_state["fleet_results"]

        # Summary cards
        st.markdown("<br>", unsafe_allow_html=True)
        kc1, kc2, kc3, kc4 = st.columns(4)
        kc1.metric("Total Machines",  len(res))
        kc2.metric("Critical",        len(res[res["status"]=="CRITICAL"]))
        kc3.metric("Warning",         len(res[res["status"]=="WARNING"]))
        kc4.metric("Normal / Caution",len(res[res["status"].isin(["NORMAL","CAUTION"])]))

        st.markdown("<br>", unsafe_allow_html=True)
        fc1, fc2 = st.columns([3, 2])

        with fc1:
            st.markdown('<div class="section-label">RUL by Machine</div>', unsafe_allow_html=True)
            colors = [get_status_color(v) for v in res["rul_hours"].fillna(0)]
            fig_bar = go.Figure(go.Bar(
                x=res["machine_id"],
                y=res["rul_hours"],
                marker_color=colors,
                marker_line_width=0,
            ))
            fig_bar.update_layout(**PLOTLY_LAYOUT, height=320,
                                  xaxis_title="", yaxis_title="RUL (hours)")
            st.plotly_chart(fig_bar, use_container_width=True)

        with fc2:
            st.markdown('<div class="section-label">Status Distribution</div>', unsafe_allow_html=True)
            dist = res["status"].value_counts().reset_index()
            dist.columns = ["status", "count"]
            color_map = {
                "CRITICAL": "#ef4444", "WARNING": "#f97316",
                "CAUTION":  "#eab308", "NORMAL":  "#22c55e", "ERROR": "#64748b"
            }
            fig_pie = go.Figure(go.Pie(
                labels=dist["status"],
                values=dist["count"],
                marker_colors=[color_map.get(s, "#64748b") for s in dist["status"]],
                hole=0.55,
                textfont=dict(family="DM Mono", size=11),
            ))
            fig_pie.update_layout(**PLOTLY_LAYOUT, height=320,
                                  showlegend=True,
                                  legend=dict(font=dict(family="DM Mono", size=10)))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('<div class="section-label">Full Results</div>', unsafe_allow_html=True)
        st.dataframe(res, use_container_width=True, hide_index=True)

    else:
        st.markdown("""
        <div style="border:1px solid #1e2530; padding:4rem 2rem; text-align:center; margin-top:1rem;">
            <div style="font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.2em;
                        text-transform:uppercase; color:#334155;">
                Upload a CSV to begin fleet assessment
            </div>
        </div>
        """, unsafe_allow_html=True)



#  TAB 3 — MODEL & TRAINING

with tab_model:

    mc1, mc2 = st.columns([3, 2])

    with mc1:
        st.markdown('<div class="section-label">Model Information</div>', unsafe_allow_html=True)

        info = {
            "Model":         "RandomForestRegressor",
            "Registry Name": "RandomForest_RUL",
            "Stage":         "Latest",
            "Tracking":      "DagHub / MLflow",
            "Target":        "rul_hours",
            "n_estimators":  "300",
            "max_depth":     "12",
            "min_samples_leaf": "10",
        }
        for k, v in info.items():
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:0.6rem 0;
                        border-bottom:1px solid #1e2530;">
                <span style="font-family:'DM Mono',monospace; font-size:0.72rem;
                             color:#475569; letter-spacing:0.1em; text-transform:uppercase;">{k}</span>
                <span style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#e2e8f0;">{v}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Logged Metrics</div>', unsafe_allow_html=True)

        mm1, mm2, mm3 = st.columns(3)
        mm1.metric("RMSE",  "18.72 h")
        mm2.metric("MAE",   "14.48 h")
        mm3.metric("R²",    "0.891")

    with mc2:
        st.markdown('<div class="section-label">Retrain Model</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="font-family:'DM Mono',monospace; font-size:0.75rem; color:#475569;
                  line-height:1.7; margin-bottom:1.5rem;">
        Triggers the full training pipeline: feature engineering, model fit,
        MLflow logging, S3 artifact upload, and registry update.
        This may take several minutes.
        </p>
        """, unsafe_allow_html=True)

        if st.button("Trigger Retraining", use_container_width=True):
            with st.spinner("Training in progress..."):
                try:
                    resp = call_train()
                    st.success(resp.get("status", "Training complete."))
                except requests.exceptions.ConnectionError:
                    st.error("Cannot reach API server.")
                except Exception as e:
                    st.error(f"Training error: {e}")

    # Feature importance (static from last run — replace with live API call if desired)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Feature Groups</div>', unsafe_allow_html=True)

    features = {
        "vibration_magnitude_roll6": 0.142,
        "vibration_magnitude_lag1":  0.118,
        "machine_age_days":          0.104,
        "pressure_bar_roll6":        0.091,
        "pump_rpm_lag1":             0.083,
        "days_since_last_maintenance": 0.071,
        "temp_celsius_roll6":        0.064,
        "flow_lpm_lag3":             0.058,
        "vibration_x_g_lag6":        0.051,
        "pressure_bar_lag3":         0.044,
    }
    feat_df = pd.DataFrame(
        {"feature": list(features.keys()), "importance": list(features.values())}
    ).sort_values("importance")

    fig_feat = go.Figure(go.Bar(
        x=feat_df["importance"],
        y=feat_df["feature"],
        orientation="h",
        marker_color="#3b82f6",
        marker_line_width=0,
    ))
    fig_feat.update_layout(**PLOTLY_LAYOUT, height=360,
                           xaxis_title="Relative Importance", yaxis_title="")
    st.plotly_chart(fig_feat, use_container_width=True)

    st.markdown("""
    <p style="font-family:'DM Mono',monospace; font-size:0.68rem; color:#334155;
              letter-spacing:0.08em; margin-top:0.5rem;">
    Note: Feature importance values shown are illustrative. Connect /feature-importance
    endpoint to your FastAPI backend to display live values from the registered model.
    </p>
    """, unsafe_allow_html=True)