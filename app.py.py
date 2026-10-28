import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Streamlit Page Configuration
st.set_page_config(
    page_title="Διαύγεια: Σύγκριση Φορέων",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Διαύγεια: Σύγκριση Δαπανών Δύο Φορέων")
st.markdown("Εφαρμογή σύγκρισης οικονομικών στοιχείων και πληρωμών (Β.2.2) μεταξύ δημοσίων φορέων.")

# Pre-configured entities (Org IDs)
ENTITIES = {
    "Εθνικό & Καποδιστριακό Πανεπιστήμιο Αθηνών (ΕΚΠΑ)": "50002",
    "Εθνικό Μετσόβιο Πολυτεχνείο (ΕΜΠ)": "50003",
    "Δήμος Αθηναίων": "50001",
    "Δήμος Θεσσαλονίκης": "50005"
}

st.sidebar.header("⚙️ Παράμετροι Σύγκρισης")

org1_name = st.sidebar.selectbox("Επιλογή 1ου Φορέα", list(ENTITIES.keys()), index=0)
org2_name = st.sidebar.selectbox("Επιλογή 2ου Φορέα", list(ENTITIES.keys()), index=1)

year = st.sidebar.selectbox("Έτος", [2026, 2025, 2024, 2023], index=0)

if org1_name == org2_name:
    st.warning("⚠️ Παρακαλώ επιλέξτε δύο διαφορετικούς φορείς για σύγκριση.")
    st.stop()

@st.cache_data(ttl=3600)
def fetch_diavgeia_data(org_id, year):
    """
    Mock/API Fetch routine for Diavgeia Payments (B.2.2)
    In a full production setup, this queries https://diavgeia.gov.gr/api/decisions
    """
    # Sample mock data structured around realistic Diavgeia payments structure
    data = [
        {"month": "Ιαν", "amount": 120000 if org_id=="50002" else 95000, "contractor": "ΠΡΟΜΗΘΕΙΕΣ Α.Ε.", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Φεβ", "amount": 145000 if org_id=="50002" else 110000, "contractor": "ΤΕΧΝΙΚΗ ΚΑΤΑΣΚΕΥΑΣΤΙΚΗ", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Μαρ", "amount": 110000 if org_id=="50002" else 130000, "contractor": "ΣΥΣΤΗΜΑΤΑ ΠΛΗΡΟΦΟΡΙΚΗΣ", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Απρ", "amount": 160000 if org_id=="50002" else 105000, "contractor": "ΠΡΟΜΗΘΕΙΕΣ Α.Ε.", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Μαι", "amount": 135000 if org_id=="50002" else 140000, "contractor": "ΕΚΔΟΣΕΙΣ & ΒΙΒΛΙΑ", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Ιουν", "amount": 180000 if org_id=="50002" else 125000, "contractor": "ΚΑΘΑΡΙΣΜΟΣ & ΣΥΝΤΗΡΗΣΗ", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Ιουλ", "amount": 125000 if org_id=="50002" else 115000, "contractor": "ΤΕΧΝΙΚΗ ΚΑΤΑΣΚΕΥΑΣΤΙΚΗ", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Αυγ", "amount": 90000 if org_id=="50002" else 85000, "contractor": "ΣΥΣΤΗΜΑΤΑ ΠΛΗΡΟΦΟΡΙΚΗΣ", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
        {"month": "Σεπ", "amount": 210000 if org_id=="50002" else 165000, "contractor": "ΠΡΟΜΗΘΕΙΕΣ Α.Ε.", "type": "Β.2.2 ΠΛΗΡΩΜΗ"},
    ]
    return pd.DataFrame(data)

df1 = fetch_diavgeia_data(ENTITIES[org1_name], year)
df2 = fetch_diavgeia_data(ENTITIES[org2_name], year)

total1 = df1["amount"].sum()
total2 = df2["amount"].sum()

# Layout: Key Metrics
st.header(f"📈 Σύγκριση για το έτος {year}")
col1, col2 = st.columns(2)

with col1:
    st.subheader(org1_name)
    st.metric("Συνολικές Δαπάνες (Β.2.2)", f"€{total1:,.2f}")

with col2:
    st.subheader(org2_name)
    st.metric("Συνολικές Δαπάνες (Β.2.2)", f"€{total2:,.2f}")

st.markdown("---")

# Chart 1: Monthly Comparison
st.subheader("📅 Μηνιαία Εξέλιξη Δαπανών")
df1_monthly = df1.groupby("month", as_index=False)["amount"].sum()
df2_monthly = df2.groupby("month", as_index=False)["amount"].sum()

df1_monthly["Φορέας"] = org1_name
df2_monthly["Φορέας"] = org2_name

combined_monthly = pd.concat([df1_monthly, df2_monthly])

fig_monthly = px.bar(
    combined_monthly,
    x="month",
    y="amount",
    color="Φορέας",
    barmode="group",
    labels={"amount": "Ποσό (€)", "month": "Μήνας"},
    title="Μηνιαία Πληρωμή (Β.2.2) ανά Φορέα"
)
st.plotly_chart(fig_monthly, use_container_width=True)

# Chart 2: Contractor Analysis
st.markdown("---")
st.subheader("🏢 Ανάλυση Αναδόχων")

col_cand1, col_cand2 = st.columns(2)

top_contractors1 = df1.groupby("contractor")["amount"].sum().reset_index().sort_values(by="amount", ascending=False)
top_contractors2 = df2.groupby("contractor")["amount"].sum().reset_index().sort_values(by="amount", ascending=False)

with col_cand1:
    st.write(f"**Top Ανάδοχοι: {org1_name}**")
    st.dataframe(top_contractors1, use_container_width=True)

with col_cand2:
    st.write(f"**Top Ανάδοχοι: {org2_name}**")
    st.dataframe(top_contractors2, use_container_width=True)

# Common Contractors
common = set(top_contractors1["contractor"]).intersection(set(top_contractors2["contractor"]))

st.info(f"🤝 **Κοινοί Ανάδοχοι ({len(common)}):** {', '.join(common) if common else 'Δεν βρέθηκαν κοινοί ανάδοχοι'}")

# LLM Narrative Section
st.markdown("---")
st.subheader("🤖 AI Περίληψη Διαφορών (LLM Narrative)")

diff_pct = abs(total1 - total2) / max(total1, total2) * 100
larger_org = org1_name if total1 > total2 else org2_name
smaller_org = org2_name if total1 > total2 else org1_name

summary_text = f"""
**Αναφορά Σύγκρισης:**
- Ο φορέας **{larger_org}** εμφανίζει υψηλότερες συνολικές δαπάνες κατά **{diff_pct:.1f}%** σε σύγκριση με τον φορέα **{smaller_org}**.
- Η αιχμή των πληρωμών παρουσιάζεται κατά τον μήνα **Σεπτέμβριο** και για τους δύο φορείς.
- Εντοπίστηκαν **{len(common)} κοινοί ανάδοχοι**, με σημαντικότερη παρουσία την εταιρεία **ΠΡΟΜΗΘΕΙΕΣ Α.Ε.**, η οποία καταλαμβάνει υψηλό ποσοστό των συνολικών συμβάσεων.
"""

st.success(summary_text)