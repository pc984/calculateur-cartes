import streamlit as st

def calcul_potentiel(population, entreprises, agents, commerces, seniors, 
                     taux_adoption_b2c, moy_b2c, 
                     taux_adoption_b2b, moy_b2b, 
                     taux_adoption_b2g_agents, moy_b2g, 
                     taux_adoption_seniors, moy_seniors, 
                     taux_adhesion_commerces, nb_cartes_par_entreprise):
    
    potentiel_b2c = population * (taux_adoption_b2c / 100) * moy_b2c
    potentiel_b2b = entreprises * (taux_adoption_b2b / 100) * nb_cartes_par_entreprise * moy_b2b
    potentiel_b2g_agents = agents * (taux_adoption_b2g_agents / 100) * moy_b2g
    potentiel_b2g_seniors = seniors * (taux_adoption_seniors / 100) * moy_seniors
    
    total_potentiel = potentiel_b2c + potentiel_b2b + potentiel_b2g_agents + potentiel_b2g_seniors
    commerces_adhérents = commerces * (taux_adhesion_commerces / 100)
    
    return potentiel_b2c, potentiel_b2b, potentiel_b2g_agents, potentiel_b2g_seniors, total_potentiel, commerces_adhérents

st.title("💳 Calculateur du Potentiel de Vente des Cartes Cadeaux Locales")

col1, col2 = st.columns(2)

with col1:
    population = st.number_input("Population", min_value=0, value=20000)
    entreprises = st.number_input("Nombre d'entreprises", min_value=0, value=500)
    agents = st.number_input("Nombre d'agents municipaux", min_value=0, value=300)
    seniors = st.number_input("Nombre de seniors (60 ans et +)", min_value=0, value=4000)
    commerces = st.number_input("Nombre de commerces", min_value=0, value=100)
    
    moy_b2c = st.number_input("Montant moyen B2C (€)", min_value=0.0, value=50.0)
    moy_b2b = st.number_input("Montant moyen B2B (€)", min_value=0.0, value=70.0)
    nb_cartes_par_entreprise = st.number_input("Nombre moyen de cartes par entreprise", min_value=1, value=10)
    moy_b2g = st.number_input("Montant moyen B2G (€)", min_value=0.0, value=50.0)
    moy_seniors = st.number_input("Montant moyen Seniors (€)", min_value=0.0, value=50.0)

with col2:
    taux_adoption_b2c = st.slider("Taux d'adoption B2C (%)", 0.0, 100.0, 2.0)
    taux_adoption_b2b = st.slider("Taux d'adoption B2B (%)", 0.0, 100.0, 5.0)
    taux_adoption_b2g_agents = st.slider("Taux d'adoption B2G - Agents (%)", 0.0, 100.0, 30.0)
    taux_adoption_seniors = st.slider("Taux d'adoption B2G - Seniors (%)", 0.0, 100.0, 20.0)
    taux_adhesion_commerces = st.slider("Taux d'adhésion des commerces (%)", 0.0, 100.0, 50.0)

potentiel_b2c, potentiel_b2b, potentiel_b2g_agents, potentiel_b2g_seniors, total_potentiel, commerces_adhérents = calcul_potentiel(
    population, entreprises, agents, commerces, seniors,
    taux_adoption_b2c, moy_b2c, 
    taux_adoption_b2b, moy_b2b, 
    taux_adoption_b2g_agents, moy_b2g,
    taux_adoption_seniors, moy_seniors,
    taux_adhesion_commerces, nb_cartes_par_entreprise
)

with col2:
    st.markdown(
        f"""
        <div style="background-color: white; padding: 10px; border-radius: 5px; color: black;">
            <h3>📊 Résultats</h3>
            <p><b>💰 Potentiel B2C :</b> {potentiel_b2c:,.2f} €</p>
            <p><b>🏢 Potentiel B2B :</b> {potentiel_b2b:,.2f} €</p>
            <p><b>🏛️ Potentiel B2G - Agents :</b> {potentiel_b2g_agents:,.2f} €</p>
            <p><b>👴 Potentiel B2G - Seniors :</b> {potentiel_b2g_seniors:,.2f} €</p>
            <p><b>🔹 Potentiel Total :</b> {total_potentiel:,.2f} €</p>
            <p><b>🏪 Nombre de commerçants adhérents :</b> {commerces_adhérents:.0f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("---")
st.subheader("📂 Calcul automatique à partir d'un fichier CSV")

uploaded_file = st.file_uploader("Importer un fichier CSV avec les colonnes : Commune, Population, Entreprises, Agents, Seniors, Commerces", type=["csv"])

if uploaded_file is not None:
    import pandas as pd

    df = pd.read_csv(uploaded_file)

    results = []
    for _, row in df.iterrows():
        try:
            b2c, b2b, b2g_a, b2g_s, total, commercants = calcul_potentiel(
                row["Population"], row["Entreprises"], row["Agents"], row["Commerces"], row["Seniors"],
                taux_adoption_b2c, moy_b2c,
                taux_adoption_b2b, moy_b2b,
                taux_adoption_b2g_agents, moy_b2g,
                taux_adoption_seniors, moy_seniors,
                taux_adhesion_commerces, nb_cartes_par_entreprise
            )
            results.append({
                "Commune": row["Commune"],
                "💰 Potentiel B2C (€)": round(b2c, 2),
                "🏢 Potentiel B2B (€)": round(b2b, 2),
                "🏛️ Potentiel B2G - Agents (€)": round(b2g_a, 2),
                "👴 Potentiel B2G - Seniors (€)": round(b2g_s, 2),
                "🔹 Potentiel Total (€)": round(total, 2),
                "🏪 Commerçants adhérents": round(commercants)
            })
        except Exception as e:
            st.warning(f"Erreur sur la commune {row.get('Commune', 'inconnue')} : {e}")

    result_df = pd.DataFrame(results)
    st.dataframe(result_df)

    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger les résultats", csv, "potentiel_cartes_par_commune.csv", "text/csv")
