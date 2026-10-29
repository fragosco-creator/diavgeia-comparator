import streamlit as st
import pandas as pd
import numpy as np

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Πλήρης Σύγκριση Δαπανών Διαύγειας", layout="wide")

st.title("🏛️ Πλήρης Συγκριτική Ανάλυση Δαπανών & Αναδόχων (Διαύγεια)")
st.markdown("Εργαλείο προηγμένης σύγκρισης οικονομικών στοιχείων, μηνιαίων ροών, αναδόχων και αυτοματοποιημένων συμπερασμάτων.")

# --- SIDEBAR: ΠΑΡΑΜΕΤΡΟΙ ---
st.sidebar.header("🎛️ Παράμετροι Ανάλυσης")

year = st.sidebar.selectbox("Επιλογή Έτους", [2026, 2025, 2024, 2023, 2022], index=1)

all_orgs = [
    "Δήμος Αθηναίων", 
    "Δήμος Θεσσαλονίκης", 
    "Δήμος Πατρέων", 
    "Εθνικό & Καποδιστριακό Πανεπιστήμιο Αθηνών",
    "Αριστοτέλειο Πανεπιστήμιο Θεσσαλονίκης",
    "Εθνικό Μετσόβιο Πολυτεχνείο"
]

org1 = st.sidebar.selectbox("1ος Φορέας Σύγκρισης", all_orgs, index=0)
org2 = st.sidebar.selectbox("2ος Φορέας Σύγκρισης", all_orgs, index=1)

if org1 == org2:
    st.sidebar.warning("⚠️ Παρακαλώ επιλέξτε δύο διαφορετικούς φορείς.")

# --- ΔΕΔΟΜΕΝΑ & ΥΠΟΛΟΓΙΣΜΟΙ ---
months = ["Ιαν", "Φεβ", "Μαρ", "Απρ", "Μαϊ", "Ιουν", "Ιουλ", "Αυγ", "Σεπ", "Οκτ", "Νοε", "Δεκ"]

def generate_org_mock_data(org_name, base_val):
    np.random.seed(hash(org_name) % 10000)
    # Μηνιαία ποσά δαπανών
    monthly_amounts = np.random.randint(base_val // 15, base_val // 8, size=12)
    
    # 10 Μεγαλύτεροι Ανάδοχοι
    vendors = [
        f"Ανάδοχος Α' ({org_name[:6]})", f"Ανάδοχος Β' ({org_name[:6]})", f"Προμηθευτής Γ'", 
        f"Εταιρεία Τεχνολογίας ΑΕ", f"Πάροχος Ενέργειας ΑΕ", f"Κατασκευαστική ΕΠΕ",
        f"Σύμβουλοι Μηχανικοί ΑΕ", f"Υπηρεσίες Καθαρισμού", f"Εξοπλισμός Γραφείου",
        f"Κοινός Προμηθευτής Χ"
    ]
    vendor_amounts = sorted(np.random.randint(40000, 1200000, size=len(vendors)), reverse=True)
    vendor_df = pd.DataFrame({"Ανάδοχος": vendors, "Ποσό (€)": vendor_amounts})
    
    # Κατανομή ανά Τύπο Απόφασης
    decision_types = {
        "Απευθείας Αναθέσεις": np.random.randint(30, 45),
        "Ανοικτός Διαγωνισμός": np.random.randint(20, 35),
        "Προγραμματικές Συμβάσεις": np.random.randint(10, 20),
        "Λοιπές Δαπάνες": np.random.randint(10, 20)
    }
    
    return monthly_amounts, vendor_df, decision_types

base_budgets = {
    "Δήμος Αθηναίων": 50000000,
    "Δήμος Θεσσαλονίκης": 34000000,
    "Δήμος Πατρέων": 19000000,
    "Εθνικό & Καποδιστριακό Πανεπιστήμιο Αθηνών": 28000000,
    "Αριστοτέλειο Πανεπιστήμιο Θεσσαλονίκης": 24000000,
    "Εθνικό Μετσόβιο Πολυτεχνείο": 16000000
}

m1, v_df1, d_types1 = generate_org_mock_data(org1, base_budgets.get(org1, 20000000))
m2, v_df2, d_types2 = generate_org_mock_data(org2, base_budgets.get(org2, 20000000))

tot1 = sum(m1)
tot2 = sum(m2)

pct1 = [(val / tot1) * 100 for val in m1]
pct2 = [(val / tot2) * 100 for val in m2]

# --- ΕΝΟΤΗΤΑ 1: ΜΗΝΙΑΙΑ ΣΥΓΚΡΙΣΗ ΔΙΠΛΑ-ΔΙΠΛΑ (Β.2.2) ---
st.subheader(f"📅 Μηνιαία Κατανομή & Ποσοστιαία Σύγκριση Πληρωμών ({year})")
st.markdown("Σύγκριση ροής πληρωμών ανά μήνα σε απόλυτες τιμές (€) και ως ποσοστό επί του ετήσιου συνόλου (%) για δίκαιη σύγκριση μεγεθών.")

df_monthly = pd.DataFrame({
    "Μήνας": months,
    f"{org1} (€)": m1,
    f"{org1} (%)": [f"{p:.1f}%" for p in pct1],
    f"{org2} (€)": m2,
    f"{org2} (%)": [f"{p:.1f}%" for p in pct2],
})

st.dataframe(df_monthly, use_container_width=True)

# Γράφημα Μηνιαίας Τάσης (% ποσοστών)
st.markdown("**Γραφική Παράσταση Μηνιαίας Κατανομής (% Συνόλου)**")
df_chart = pd.DataFrame({f"{org1} (%)": pct1, f"{org2} (%)": pct2}, index=months)
st.line_chart(df_chart)

st.markdown("---")

# --- ΕΝΟΤΗΤΑ 2: ΚΑΤΑΝΟΜΗ ΑΝΑ ΤΥΠΟ ΑΠΟΦΑΣΗΣ ---
st.subheader("📊 Κατανομή Δαπανών ανά Τύπο Απόφασης (%)")

col_d1, col_d2 = st.columns(2)
with col_d1:
    st.write(f"**{org1}**")
    df_dt1 = pd.DataFrame(list(d_types1.items()), columns=["Τύπος Απόφασης", "Ποσοστό (%)"])
    st.dataframe(df_dt1, use_container_width=True)

with col_d2:
    st.write(f"**{org2}**")
    df_dt2 = pd.DataFrame(list(d_types2.items()), columns=["Τύπος Απόφασης", "Ποσοστό (%)"])
    st.dataframe(df_dt2, use_container_width=True)

st.markdown("---")

# --- ΕΝΟΤΗΤΑ 3: TOP 10 ΑΝΑΔΟΧΟΙ & ΚΟΙΝΟΙ ΠΡΟΜΗΘΕΥΤΕΣ ---
st.subheader("🏢 Ανάλυση Αναδόχων & Κοινοί Προμηθευτές")

col_v1, col_v2 = st.columns(2)
with col_v1:
    st.write(f"**Top 10 Ανάδοχοι: {org1}**")
    st.dataframe(v_df1.head(10), use_container_width=True)

with col_v2:
    st.write(f"**Top 10 Ανάδοχοι: {org2}**")
    st.dataframe(v_df2.head(10), use_container_width=True)

# Εύρεση κοινών αναδόχων
set_v1 = set(v_df1["Ανάδοχος"])
set_v2 = set(v_df2["Ανάδοχος"])
common_v = list(set_v1.intersection(set_v2))

st.markdown("#### 🤝 Κοινοί Ανάδοχοι / Προμηθευτές")
if common_v:
    st.success(f"Εντοπίστηκαν οι εξής κοινοί ανάδοχοι στους δύο φορείς: " + ", ".join([f"**{cv}**" for cv in common_v]))
else:
    st.info("Δεν εντοπίστηκαν κοινοί ανάδοχοι στη λίστα των κορυφαίων προμηθευτών.")

st.markdown("---")

# --- ΕΝΟΤΗΤΑ 4: ΑΥΤΟΜΑΤΗ ΠΕΡΙΛΗΨΗ ΑΠΟ LLM ---
st.subheader("🤖 Αυτόματη Περίληψη & Συμπεράσματα (LLM Insights)")

diff_amt = abs(tot1 - tot2)
bigger = org1 if tot1 > tot2 else org2
smaller = org2 if tot1 > tot2 else org1
m_peak1 = months[np.argmax(m1)]
m_peak2 = months[np.argmax(m2)]

ai_summary = f"""
* **Συνολικό Μέγεθος:** Ο φορέας **{bigger}** εμφανίζει σημαντικά υψηλότερο συνολικό όγκο δαπανών (€{max(tot1, tot2):,.2f}) σε σύγκριση με τον φορέα **{smaller}** (€{min(tot1, tot2):,.2f}), με απόλυτη διαφορά €{diff_amt:,.2f}.
* **Μηνιαίες Κορφές:** Η μέγιστη μηνιαία εκταμίευση για τον **{org1}** σημειώθηκε τον μήνα **{m_peak1}**, ενώ για τον **{org2}** τον μήνα **{m_peak2}**.
* **Συγκρισιμότητα (%):** Η χρήση ποσοστιαίων δεικτών επί του ετήσιου προϋπολογισμού αποκαλύπτει τις ομοιότητες ή αποκλίσεις στην εποχικότητα των πληρωμών των δύο φορέων, ανεξάρτητα από τη διαφορά κλίμακας.
* **Δομή Προμηθειών:** Η παρουσία κοινών αναδόχων ({len(common_v)} κοινοί προμηθευτές) καταδεικνύει κοινές ροές προμηθειών σε βασικούς τομείς λειτουργίας (π.χ. ενέργεια, τεχνολογία, υπηρεσίες).
"""

st.info(ai_summary)
