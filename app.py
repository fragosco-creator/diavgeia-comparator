import streamlit as st
import pandas as pd

st.title("Σύγκριση Δαπανών Διαύγειας")

# Επιλογή έτους
year = st.sidebar.selectbox("Επιλογή Έτους", [2026, 2025, 2024, 2023, 2022], index=1)

# Εισαγωγή ονομάτων φορέων
default_orgs = ["Δήμος Αθηναίων", "Δήμος Θεσσαλονίκης", "Δήμος Πατρέων"]
orgs_input = st.sidebar.text_area("Φορείς (χωρισμένοι με κόμμα)", ", ".join(default_orgs))
orgs_list = [org.strip() for org in orgs_input.split(",") if org.strip()]

# Κουμπί εκκίνησης σύγκρισης
if st.button("Σύγκριση Φορέων"):
    st.write(f"Ανάλυση δεδομένων για το έτος {year}...")
    
    # Δεδομένα επίδειξης βασισμένα σε πραγματικές τάξεις μεγέθους δαπανών των δήμων
    mock_data = {
        "Δήμος Αθηναίων": {"count": 1420, "amount": 48500000.0},
        "Δήμος Θεσσαλονίκης": {"count": 980, "amount": 31200000.0},
        "Δήμος Πατρέων": {"count": 650, "amount": 18400000.0},
    }
    
    all_data = []
    for org in orgs_list:
        # Αν υπάρχει στους βασικούς δήμους, παίρνουμε τα στοιχεία, αλλιώς τυχαία νούμερα για δοκιμή
        if org in mock_data:
            c = mock_data[org]["count"]
            amt = mock_data[org]["amount"]
        else:
            c = 500
            amt = 15000000.0
            
        all_data.append({
            "Φορέας": org,
            "Πλήθος Αποφάσεων Δαπανών": c,
            "Συνολικό Ποσό (€)": amt
        })
        
    df = pd.DataFrame(all_data)
    st.subheader(f"Συγκριτικά Αποτελέσματα Δαπανών ({year})")
    st.dataframe(df)
    
    # Γράφημα
    st.bar_chart(df.set_index("Φορέας")["Συνολικό Ποσό (€)"])
