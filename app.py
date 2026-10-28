import streamlit as st
import requests
import pandas as pd

st.title("Σύγκριση Δαπανών Διαύγειας")

# Επιλογή έτους
year = st.sidebar.selectbox("Επιλογή Έτους", [2026, 2025, 2024, 2023, 2022], index=1)

# Εισαγωγή ονομάτων φορέων
default_orgs = ["Δήμος Αθηναίων", "Δήμος Θεσσαλονίκης", "Δήμος Πατρέων"]
orgs_input = st.sidebar.text_area("Φορείς (χωρισμένοι με κόμμα)", ", ".join(default_orgs))
orgs_list = [org.strip() for org in orgs_input.split(",") if org.strip()]

# Συνάρτηση για λήψη δεδομένων από τη Διαύγεια API
@st.cache_data(ttl=3600)
def fetch_diavgeia_data(org_name, year_val):
    base_url = "https://diavgeia.gov.gr/api/search"
    
    from_date = f"{year_val}-01-01"
    to_date = f"{year_val}-12-31"
    
    params = {
        "q": f'org:"{org_name}"',
        "from": from_date,
        "to": to_date,
        "type": "ΔΑΠΑΝΗ",
        "size": 50
    }
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            try:
                return response.json()
            except:
                return None
        else:
            return None
    except:
            return None

# Κουμπί εκκίνησης σύγκρισης
if st.button("Σύγκριση Φορέων"):
    all_data = []
    
    for org in orgs_list:
        st.write(f"Αναζήτηση δεδομένων για: **{org}**...")
        data = fetch_diavgeia_data(org, year)
        
        if data and "decisions" in data:
            decisions = data["decisions"]
            total_amount = 0
            count = len(decisions)
            
            for d in decisions:
                # Προσπάθεια ανάγνωσης ποσού αν υπάρχει
                amount = d.get("amount", 0)
                if amount:
                    total_amount += float(amount)
            
            all_data.append({
                "Φορέας": org,
                "Πλήθος Αποφάσεων Δαπανών": count,
                "Συνολικό Πσό (€)": total_amount
            })
        else:
            all_data.append({
                "Φορέας": org,
                "Πλήθος Αποφάσεων Δαπανών": 0,
                "Συνολικό Πσό (€)": 0
            })
            
    if all_data:
        df = pd.DataFrame(all_data)
        st.subheader(f"Αποτελέσματα για το έτος {year}")
        st.dataframe(df)
        
        # Γράφημα
        if "Συνολικό Πσό (€)" in df.columns and df["Συνολικό Πσό (€)"].sum() > 0:
            st.bar_chart(df.set_index("Φορέας")["Συνολικό Πσό (€)"])
