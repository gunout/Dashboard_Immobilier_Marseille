# dashboard_marseille.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import io
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Immobilier Marseille",
    page_icon="🏖️",
    layout="wide"
)

# --- Dictionnaire des principales communes de la Métropole Aix-Marseille-Provence ---
# NOTE : Marseille est dans le département 13 (Bouches-du-Rhône)
COMMUNES_MARSEILLE = {
    "13055": "Marseille",
    "13001": "Aix-en-Provence",
    "13002": "Arles",
    "13003": "Aubagne",
    "13004": "La Ciotat",
    "13005": "Marignane",
    "13006": "Istres",
    "13007": "Vitrolles",
    "13008": "Martigues",
    "13009": "Aubagne",
    "13010": "Cassis",
    "13011": "Allauch",
    "13012": "Septèmes-les-Vallons",
    "13013": "La Penne-sur-Huveaune",
    "13014": "Plan-de-Cuques",
    "13015": "Carry-le-Rouet",
    "13016": "Sausset-les-Pins",
    "13017": "Ensuès-la-Redonne",
    "13018": "Le Rove",
    "13019": "Châteauneuf-les-Martigues",
    "13020": "Gignac-la-Nerthe",
    "13021": "Le Bouc-Bel-Air",
    "13022": "La Fare-les-Oliviers",
    "13023": "Cuges-les-Pins",
    "13024": "Cadolive",
    "13025": "Saint-Zacharie",
    "13026": "Auriol",
    "13027": "Saint-Savournin",
    "13028": "Gréasque",
    "13029": "La Bouilladisse",
    "13030": "Mimet",
    "13031": "Simiane-Collongue",
    "13032": "Aubagne",
    "13033": "Roquevaire",
    "13034": "La Destrousse",
    "13035": "Peypin",
    "13036": "Saint-Marcel-Paulel",
    "13037": "Meyreuil",
    "13038": "Châteauneuf-le-Rouge",
    "13039": "Peynier",
    "13040": "Rousset",
    "13041": "Trets",
    "13042": "Saint-Antonin-sur-Bayon",
    "13043": "Pourrières",
    "13044": "Puyloubier",
    "13045": "Beaurecueil",
    "13046": "Le Tholonet",
    "13047": "Eguilles",
    "13048": "Meyrargues",
    "13049": "Peyrolles-en-Provence",
    "13050": "Saint-Canadet",
    "13051": "Jouques",
    "13052": "Meyrargues",
    "13053": "Saint-Paul-lès-Durance",
    "13054": "Le Puy-Sainte-Réparade",
    "13055": "Marseille",
    "13056": "Aix-en-Provence",
    "13057": "Marseille",
    "13058": "Marseille",
    "13059": "Marseille",
    "13060": "Marseille",
    "13061": "Marseille",
    "13062": "Marseille",
    "13063": "Marseille",
    "13064": "Marseille",
    "13065": "Marseille",
    "13066": "Marseille",
    "13067": "Marseille",
    "13068": "Marseille",
    "13069": "Marseille",
    "13070": "Marseille",
    "13071": "Marseille",
    "13072": "Marseille",
    "13073": "Marseille",
    "13074": "Marseille",
    "13075": "Marseille",
    "13076": "Marseille",
    "13077": "Marseille",
    "13078": "Marseille",
    "13079": "Marseille",
    "13080": "Marseille",
    "13081": "Marseille",
    "13082": "Marseille",
    "13083": "Marseille",
    "13084": "Marseille",
    "13085": "Marseille",
    "13086": "Marseille",
    "13087": "Marseille",
    "13088": "Marseille",
    "13089": "Marseille",
    "13090": "Marseille",
    "13091": "Marseille",
    "13092": "Marseille",
    "13093": "Marseille",
    "13094": "Marseille",
    "13095": "Marseille",
    "13096": "Marseille",
    "13097": "Marseille",
    "13098": "Marseille",
    "13099": "Marseille",
    "13100": "Marseille",
    "13101": "Marseille",
    "13102": "Marseille",
    "13103": "Marseille",
    "13104": "Marseille",
    "13105": "Marseille",
    "13106": "Marseille",
    "13107": "Marseille",
    "13108": "Marseille",
    "13109": "Marseille",
    "13110": "Marseille",
    "13111": "Marseille",
    "13112": "Marseille",
    "13113": "Marseille",
    "13114": "Marseille",
    "13115": "Marseille",
    "13116": "Marseille",
}

# Inverser le dictionnaire pour avoir Nom -> Code INSEE (plus pratique pour le selectbox)
NOMS_COMMUNES = {v: k for k, v in COMMUNES_MARSEILLE.items()}

# --- Fonction de chargement des données (générique) ---
@st.cache_data
def load_commune_data(insee_code: str):
    """
    Charge les données DVF 2024 pour une commune des Bouches-du-Rhône donnée par son code INSEE.
    """
    url = f"https://files.data.gouv.fr/geo-dvf/latest/csv/2024/communes/13/{insee_code}.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        df = pd.read_csv(io.StringIO(response.text), sep=',', low_memory=False)
        
        if df.empty:
            return pd.DataFrame()

        # Nettoyage (identique à la version précédente)
        df["date_mutation"] = pd.to_datetime(df["date_mutation"], format='%Y-%m-%d', errors='coerce')
        df["valeur_fonciere"] = pd.to_numeric(df["valeur_fonciere"], errors='coerce')
        df = df[df["type_local"].isin(['Maison', 'Appartement'])]
        
        if df.empty:
            return pd.DataFrame()

        df = df.dropna(subset=["valeur_fonciere", "surface_reelle_bati", "code_postal", "date_mutation"])
        df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors='coerce')
        df = df.dropna(subset=["surface_reelle_bati"])

        if df.empty:
            return pd.DataFrame()

        df['prix_m2'] = df['valeur_fonciere'] / df['surface_reelle_bati']
        # Ajustement des bornes pour Marseille (prix plus élevés que dans la Creuse)
        df = df[(df['prix_m2'] > 1000) & (df['prix_m2'] < 20000)]
        
        if df.empty:
            return pd.DataFrame()
        
        return df

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion pour la commune {insee_code} : {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
        return pd.DataFrame()

# --- Fonction pour charger toutes les communes de la Métropole Aix-Marseille-Provence ---
@st.cache_data
def load_all_marseille_data():
    """
    Charge les données DVF 2024 pour toutes les communes de la Métropole Aix-Marseille-Provence.
    """
    all_data = []
    
    for insee_code, commune_name in COMMUNES_MARSEILLE.items():
        df = load_commune_data(insee_code)
        if not df.empty:
            df['commune'] = commune_name
            all_data.append(df)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

# --- Interface Utilisateur ---
st.title("🏖️ Dashboard Immobilier Marseille")

# Sélection de la commune dans la barre latérale
st.sidebar.header("Sélection de la commune")
selected_commune_name = st.sidebar.selectbox(
    "Choisissez une commune :",
    options=sorted(NOMS_COMMUNES.keys())
)

# Option pour afficher toutes les communes
show_all_communes = st.sidebar.checkbox("Afficher toutes les communes de la Métropole Aix-Marseille-Provence")

# Récupérer le code INSEE correspondant
selected_insee_code = NOMS_COMMUNES[selected_commune_name]

# Afficher un message d'information dynamique
if show_all_communes:
    st.info(f"ℹ️ Données réelles DVF 2024 pour toutes les communes de la **Métropole Aix-Marseille-Provence**, provenant de data.gouv.fr")
else:
    st.info(f"ℹ️ Données réelles DVF 2024 pour la commune de **{selected_commune_name}** (INSEE {selected_insee_code}), provenant de data.gouv.fr")

# --- Chargement et Traitement des Données ---
if show_all_communes:
    df = load_all_marseille_data()
else:
    df = load_commune_data(selected_insee_code)
    # Ajouter la colonne 'commune' même si on ne charge qu'une seule commune
    if not df.empty:
        df['commune'] = selected_commune_name

if df.empty:
    if show_all_communes:
        st.warning("Aucune donnée de vente (Maison/Appartement) valide trouvée pour la Métropole Aix-Marseille-Provence en 2024.")
    else:
        st.warning(f"Aucune donnée de vente (Maison/Appartement) valide trouvée pour {selected_commune_name} en 2024.")
    st.stop()

# --- Filtres ---
st.sidebar.header("Filtres")
if show_all_communes:
    communes_disponibles = sorted(df['commune'].unique())
    commune_selectionnee = st.sidebar.multiselect("Commune", communes_disponibles, default=communes_disponibles)
else:
    # Si on n'affiche qu'une commune, on la pré-sélectionne pour le filtre
    commune_selectionnee = [selected_commune_name]

codes_postaux_disponibles = sorted(df['code_postal'].astype(str).unique())
code_postal_selectionne = st.sidebar.multiselect("Code postal", codes_postaux_disponibles, default=codes_postaux_disponibles)
type_local = st.sidebar.selectbox("Type de bien", ['Tous', 'Maison', 'Appartement'])
prix_min = st.sidebar.number_input("Prix minimum (€)", value=0, step=10000)
prix_max = st.sidebar.number_input("Prix maximum (€)", value=int(df['valeur_fonciere'].max()), step=10000)

# Application des filtres
df_filtre = df[
    (df['commune'].isin(commune_selectionnee)) &
    (df['code_postal'].astype(str).isin(code_postal_selectionne)) &
    (df['valeur_fonciere'] >= prix_min) &
    (df['valeur_fonciere'] <= prix_max)
].copy()

if type_local != 'Tous':
    df_filtre = df_filtre[df_filtre['type_local'] == type_local]

if df_filtre.empty:
    st.warning("Aucune transaction ne correspond à vos filtres.")
    st.stop()

# --- KPIs et Visualisations ---
if show_all_communes:
    st.header("Indicateurs Clés pour la Métropole Aix-Marseille-Provence")
else:
    st.header(f"Indicateurs Clés pour {selected_commune_name}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Prix Moyen / m²", f"{df_filtre['prix_m2'].mean():.0f} €")
with col2:
    st.metric("Prix Médian", f"{df_filtre['valeur_fonciere'].median():.0f} €")
with col3:
    st.metric("Transactions", f"{len(df_filtre):,}")
with col4:
    surface_moyenne = df_filtre['surface_reelle_bati'].mean()
    st.metric("Surface Moyenne", f"{surface_moyenne:.0f} m²")

if show_all_communes:
    st.header("Visualisations pour la Métropole Aix-Marseille-Provence")
else:
    st.header(f"Visualisations pour {selected_commune_name}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Répartition des Prix au m²")
    fig = px.histogram(df_filtre, x='prix_m2', nbins=50, color='type_local', marginal="box")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Répartition des Types de Biens")
    fig = px.pie(df_filtre, names='type_local', title='Répartition par type')
    st.plotly_chart(fig, use_container_width=True)

if show_all_communes:
    st.subheader("Carte des Transactions dans la Métropole Aix-Marseille-Provence")
else:
    st.subheader(f"Carte des Transactions à {selected_commune_name}")

if 'latitude' in df_filtre.columns and 'longitude' in df_filtre.columns:
    df_carte = df_filtre.sample(min(5000, len(df_filtre)))
    if show_all_communes:
        fig = px.scatter_mapbox(df_carte, lat="latitude", lon="longitude", color="prix_m2", size="surface_reelle_bati", hover_data=["valeur_fonciere", "type_local", "date_mutation", "commune"], color_continuous_scale=px.colors.sequential.Viridis, size_max=15, zoom=9, mapbox_style="open-street-map", title=f"Carte de {len(df_carte)} transactions (échantillon)")
    else:
        fig = px.scatter_mapbox(df_carte, lat="latitude", lon="longitude", color="prix_m2", size="surface_reelle_bati", hover_data=["valeur_fonciere", "type_local", "date_mutation", "commune"], color_continuous_scale=px.colors.sequential.Viridis, size_max=15, zoom=11, mapbox_style="open-street-map", title=f"Carte de {len(df_carte)} transactions (échantillon)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Les données de localisation (latitude/longitude) ne sont pas disponibles pour afficher la carte.")

st.subheader("Détail des Transactions (dernières)")
st.dataframe(df_filtre.sort_values('date_mutation', ascending=False).head(100).drop(columns=['latitude', 'longitude'], errors='ignore'))