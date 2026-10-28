import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Σύγκριση Δαπανών Φορέων Διαύγειας", layout="wide")

st.title("🏛️ Dashboard Σύγκρισης Δαπανών Φορέων (Διαύγεια)")
st.markdown("Συγκρίνετε τις συνολικές δαπάνες διαφορετικών φορέων από το Open Data API της Διαύγειας.")

# Πλαϊνή μπάρα (Sidebar) για τις ρυθμίσεις του χρήστη
st.sidebar.header("Παράμετροι Αναζήτησης")

# Εισαγωγή ονομάτων φορέων (χωρισμένα με κόμμα)
default_orgs = "ΥΠΟΥΡΓΕΙΟ ΥΓΕΙΑΣ, ΥΠΟΥΡΓΕΙΟ ΠΑΙΔΕΙΑΣ, ΘΡΗΣΚΕΥΜΑΤΩΝ ΚAI ΑΘΛΗΤΙΣΜΟΥ"
orgs_input = st.sidebar.text_area("Φορείς (χωρισμένοι με κόμμα)", default_orgs)
orgs_list = [org.strip() for org in orgs_input.split(",") if org.strip()]

# Επιλογή έτους
year = st.sidebar.selectbox("Επιλογή Έτους", [2026, 2025, 2024, 2023, 2022], index=1)

# Συνάρτηση για λήψη δεδομένων από τη Διαύγεια API
@st.cache_data(ttl=3600)
def fetch_diavgeia_data(org_name, year_val):
    base_url = "https://diavgeia.gov.gr/api/search"
    
    # Ορισμός ημερομηνιών για το έτος
    from_date = f"{year_val}-01-01"
    to_date = f"{year_val}-12-31"
    
    params = {
        "q": f'org:"{org_name}"',
        "from": from_date,
        "to": to_date,
        "type": "ΔΑΠΑΝΗ",
        "size": 100  # Αριθμός εγγραφών ανά κλήση
    }
    
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            decisions = data.get("decisions", [])
            
            total_amount = 0.0
            count = len(decisions)
            
            for d in decisions:
                # Εύρεση ποσού από τα extrafields της απόφασης
                extra_fields = d.get("extraFields", {})
                # Συνήθως το ποσό βρίσκεται σε πεδία όπως amount ή financial
                amount = float(extra_fields.get("amount", 0)) if extra_fields.get("amount") else 0.0
                total_amount += amount
                
            return {"Φορέας": org_name, "Συνολικό Ποσό (€)": total_amount, "Αριθμός Δαπανών": count}
        else:
            return {"Φορέας": org_name, "Συνολικό Ποσό (€)": 0.0, "Αριθμός Δαπανών": 0}
    except Exception as e:
        st.error(f''An error occurred for {org_name}: {e}'')
        return {"Φορέας": org_name, "Συνολικό Ποσό (€)": 0.0, "Αριθμός Δαπανών": 0}

# Κουμπί εκτέλεσης ανάλυσης
if st.sidebar.button("Εκτέλεση Σύγκρισης", type="primary"):
    if not orgs_list:
        st.warning("Παρακαλώ εισάγετε τουλάχιστον έναν φορέα.")
    else:
        with st.spinner("Ανάκτηση δεδομένων από το API της Διαύγειας..."):
            results = []
            for org in orgs_list:
                res = fetch_diavgeia_data(org, year)
                results.append(res)
            
            df = pd.DataFrame(results)
            
            # Εμφάνιση βασικών μετρικών
            st.subheader(f"📊 Αποτελέσματα Σύγκρισης για το έτος {year}")
            
            # Πίνακας δεδομένων
            st.dataframe(df, use_container_width=True)
            
            # Δημιουργία γραφήματος με Plotly
            if not df.empty and df["Συνολικό Ποσό (€)"].sum() > 0:
                fig = px.bar(
                    df, 
                    x="Φορέας", 
                    y="Συνολικό Ποσό (€)", 
                    text="Συνολικό Ποσό (€)",
                    color="Φορέας",
                    title=f"Συγκριτικό Δαπανών Φορέων ({year})"
                )
                fig.update_traces(texttemplate='%{text:,.2f} €', textposition='outside')
                fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Δεν βρέθηκαν οικονομικά στοιχεία για τους επιλεγμένους φορείς με τα τρέχοντα κριτήρια.")
else:
    st.info("👈 Ορίστε τους φορείς στην αριστερή μπάρα και πατήστε **«Εκτέλεση Σύγκρισης»**.")
