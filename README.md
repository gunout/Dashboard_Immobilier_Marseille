# Dashboard_Immobilier_Marseille 2 METHODES ( HTTP ou LOCAL ) 
🏖️ Dashboard Immobilier Marseille  ℹ️ Données réelles DVF 2024 pour la commune de Marseille (INSEE 13116), provenant de data.gouv.fr

<img width="660" height="460" alt="Screenshot_2025-10-17_02-13-42" src="https://github.com/user-attachments/assets/5e205860-85fb-4554-8d96-0719ba4bb1c6" />

# EXAMPLE
<img width="1280" height="1024" alt="Screenshot_2025-10-17_02-09-58" src="https://github.com/user-attachments/assets/be2ade0a-38ed-4d5a-90a9-2ac0f1fcbe3a" />
<img width="1280" height="1024" alt="Screenshot_2025-10-17_02-10-21" src="https://github.com/user-attachments/assets/c71acd2e-ab76-4ac2-bcd9-9f1f984eceed" />
<img width="1280" height="1024" alt="Screenshot_2025-10-17_02-10-33" src="https://github.com/user-attachments/assets/038f94a4-3ba8-4250-96ab-d5f580001372" />
<img width="1280" height="1024" alt="Screenshot_2025-10-17_02-10-39" src="https://github.com/user-attachments/assets/520fe0ba-1507-4b2f-877e-dc5b54659c97" />

# INSTALL DEPENDENCIES

    pip install beautifulsoup4 streamlit pandas requests plotly

# RUN PROGRAM ( METHODE HTTP ) 

    streamlit run Dashboard.py

# METHODE LOCAL ( FICHIER LOCAL )

# TÉLÉCHARGEMENT " dvf_2024.csv " avec CURL

    curl -L -o dvf_2024.csv.gz "https://files.data.gouv.fr/geo-dvf/latest/csv/2024/full.csv.gz"

# RUN PROGRAM ( Marseille ) METHODE LOCAL

    streamlit run Dash.py

PS : pour la methode local s'assurer d'avoir le fichier : dvf_2024.csv dans le meme dossier que Dash.py

By Gleaphe 2025 .
