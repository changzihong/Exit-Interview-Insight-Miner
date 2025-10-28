import streamlit as st
import pandas as pd
import random
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="🧠 Exit Interview Insight Miner", page_icon="💬", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #d2f8d2 0%, #b2ebf2 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        font-size: 2.8em;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00796b, #004d40);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #004d40;
        margin-bottom: 1.5em;
    }
    .card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .insight {
        background-color: #e0f2f1;
        border-left: 6px solid #26a69a;
        padding: 10px 15px;
        border-radius: 5px;
        margin-top: 10px;
        font-weight: 500;
    }
    .footer {
        text-align: center;
        color: #004d40;
        font-size: 0.9em;
        margin-top: 40px;
        opacity: 0.8;
    }
    #spinner {
        display: none;
        text-align: center;
        margin-top: 20px;
        font-size: 1.1em;
        color: #00796b;
    }
    .remove-btn {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 5px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.9em;
    }
    .remove-btn:hover {
        background-color: #d32f2f;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='title'>🧠 Exit Interview Insight Miner</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered insight dashboard for HR Business Partners & Talent Leaders</div>", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎛️ Filter Options")
department = st.sidebar.selectbox("Department", ["All", "Sales", "HR", "Engineering", "Finance"])
manager = st.sidebar.selectbox("Manager", ["All", "Alice Tan", "John Lim", "Siti Rahman", "David Wong"])
sentiment_filter = st.sidebar.select_slider("Sentiment", ["Negative", "Neutral", "Positive"])

# --- INITIAL DATA ---
initial_data = pd.DataFrame({
    "Employee": ["Ali", "John", "Siti", "Raj", "Mei", "Hafiz"],
    "Department": ["Sales", "HR", "Engineering", "Finance", "Sales", "Engineering"],
    "Manager": ["Alice Tan", "John Lim", "Siti Rahman", "David Wong", "Alice Tan", "Siti Rahman"],
    "Exit_Reason": [
        "Manager was unsupportive and stressful environment.",
        "Better salary offer elsewhere.",
        "Wanted career growth opportunities.",
        "Workload was too high.",
        "Low commission rates.",
        "Toxic manager and lack of teamwork."
    ],
    "Sentiment": ["Negative", "Neutral", "Positive", "Negative", "Neutral", "Negative"]
})

# --- SESSION STATE ---
if "exit_data" not in st.session_state:
    st.session_state.exit_data = initial_data.copy()

# --- FILTERING ---
df = st.session_state.exit_data
filtered_df = df.copy()
if department != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department]
if manager != "All":
    filtered_df = filtered_df[filtered_df["Manager"] == manager]
if sentiment_filter != "Neutral":
    filtered_df = filtered_df[filtered_df["Sentiment"] == sentiment_filter]

# --- DISPLAY TABLE WITH REMOVE BUTTON ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📋 Exit Interview Responses (Filtered View)")
st.write("If employee changes mind after discussion, click **'Remove After Discussion'** below:")

for idx, row in filtered_df.iterrows():
    with st.expander(f"👤 {row['Employee']} — {row['Department']} Dept"):
        st.write(f"**Manager:** {row['Manager']}")
        st.write(f"**Reason for Exit:** {row['Exit_Reason']}")
        st.write(f"**Sentiment:** {row['Sentiment']}")
        if st.button(f"🗑️ Remove After Discussion — {row['Employee']}", key=f"remove_{idx}"):
            st.session_state.exit_data = st.session_state.exit_data.drop(idx)
            st.success(f"✅ {row['Employee']} decided to stay. Removed from exit list.")
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# --- JAVASCRIPT LOADING EFFECT ---
st.markdown("""
<script>
function showSpinner(){
  const spinner = document.getElementById("spinner");
  spinner.style.display = "block";
  const text = "🤖 Mining insights from employee feedback...";
  let i = 0;
  function typeWriter() {
    if (i < text.length) {
      spinner.innerHTML = text.substring(0, i+1);
      i++;
      setTimeout(typeWriter, 50);
    }
  }
  typeWriter();
  setTimeout(()=>{spinner.innerHTML = "✅ Analysis complete! Generating insights...";}, 3000);
  setTimeout(()=>{spinner.style.display = "none";}, 5500);
}
</script>
<div id="spinner"></div>
""", unsafe_allow_html=True)

# --- RUN ANALYSIS BUTTON ---
if st.button("🚀 Run AI Insight Miner"):
    st.markdown("<script>showSpinner();</script>", unsafe_allow_html=True)
    with st.spinner("Running sentiment & theme analysis..."):
        time.sleep(4)

    # --- SIMULATED AI OUTPUT ---
    themes = ["Toxic management", "Low pay satisfaction", "Career growth issues", "Overwork fatigue"]
    selected_themes = random.sample(themes, 2)
    sentiment_score = random.randint(65, 95)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 💡 AI Insight Summary")
    st.markdown(f"<div class='insight'>Top Themes: {selected_themes[0]} | {selected_themes[1]}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>Average Sentiment Score: <b>{sentiment_score}% Positive</b></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='insight'>🧾 Executive Summary:<br>
        Recent exit interviews indicate <b>{selected_themes[0].lower()}</b> and 
        <b>{selected_themes[1].lower()}</b> as top turnover drivers. 
        Recommend targeted manager coaching and pay benchmarking.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- DEPARTMENT SUMMARY ---
summary_data = {
    "Department": ["Sales", "HR", "Engineering", "Finance"],
    "Avg Sentiment (%)": [62, 75, 68, 70],
    "Top Issue": ["Low commission", "Pay", "Career growth", "Workload"],
    "Resignation Trend": ["⬆ Increasing", "⬇ Decreasing", "⬆ Increasing", "➡ Stable"]
}
summary_df = pd.DataFrame(summary_data)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📊 Department-Level Summary (Demo)")
st.table(summary_df)
st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div class='footer'>© 2025 HR Analytics Demo | Built with ❤️ in Streamlit</div>", unsafe_allow_html=True)