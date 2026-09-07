import streamlit as st

st.title("Wirksamkeit von IT-Fördermaßnahmen")
st.markdown("### :grey[nach intersektionalen Konstellationen]")

st.divider()

# ----- Projektkontext -----
st.markdown("## Projektkontext")
st.markdown("""
Laut dem Women in Digital Scoreboard 2024 der EU-Kommission liegt der Frauenanteil in der IT global bei 25-30 % und in der EU
insgesamt bei nur 17% - und bis zu 57 % der Frauen verlassen die IT-Branche im mittleren Karrierestadium (*Leaky Pipeline*).

Bisherige Forschung und Fördermaßnahmen behandeln Frauen dabei oft als homogene Gruppe. Die intersektionale Perspektive zeigt
jedoch, dass Frauen mit mehreren Diversitätsmerkmalen (z. B. Migrationshintergrund × Mutterschaft × LGBTQ+-Identität)
unterschiedlich ausgeprägte Karrierebarrieren erleben. Dieses Projekt soll zeigen, dass Personen mit verschiedenen
intersektionalen Konstellationen unterschiedlich stark von Fördermaßnahmen profitieren können.

**These: "One Size Fits None"** - Standardmaßnahmen funktionieren nicht für alle Frauen gleich.
""")

st.markdown("### Intersektionalität")
st.markdown("""
Das Konzept der **Intersektionalität** (Kimberlé Crenshaw, 1989) beschreibt, wie verschiedene Identitätsdimensionen 
zusammenwirken und individuelle Erfahrungen von Diskriminierung und Privilegierung schaffen.

In dieser Studie wird der Einfluss der folgenden sechs Identitätsmerkmale auf die Maßnahmenwirksamkeit untersucht:
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("- Migrationshintergrund")
    st.markdown("- sexuelle Orientierung / LGBTQ+")
with col2:
    st.markdown("- Kinder im Haushalt")
    st.markdown("- Pflegeaufgaben")
with col3:
    st.markdown("- Behinderung / chronische Erkrankung")
    st.markdown("- Bildungsferner Hintergrund")

st.divider()
st.caption(
    "Im Rahmen der Bachelorarbeit von Van Khanh Luong · Berliner Hochschule für Technik (BHT) · 2026 "
)
