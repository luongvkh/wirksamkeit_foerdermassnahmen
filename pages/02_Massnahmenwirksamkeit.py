import streamlit as st
import plotly.express as px
import pandas as pd
from utils import (
    load_data,
    filter_df_dimensions,
    calculate_effectiveness,
    calculate_availability,
)
from constants import (
    ESSENTIELL_GELB,
    HILFREICH_ROT,
    SPIELT_KEINE_ROLLE_VIOLETT,
    IDENTITY_COLS,
    IDENTITY_LABELS,
    RATING_LABELS,
    BARRIER_COLS,
    BARRIER_LABELS,
    RATING_COLS,
)

# ----- Sidebar -----
with st.sidebar:
    # File Upload
    uploaded_file = st.file_uploader(
        "Datensatz hochladen (.xlsx, .csv)",
        type=["xlsx", "csv"],
    )

    st.divider()

    # Identitätsmerkmale
    selected_dims = st.multiselect(
        "Identitätsmerkmale",
        options=IDENTITY_COLS,
        format_func=lambda col: IDENTITY_LABELS[col],
        placeholder="Identitätsmerkmale auswählen...",
    )

    dim_kombination = st.toggle(
        "Nur exakte Kombination",
        value=False,
        key="dim_kombination",
        help="Wenn eingeschaltet, werden nur Personen mit ALLEN ausgewählten Merkmalen ausgegeben, ansonsten alle Personen mit mindestens einem Merkmal.",
    )

    # Fördermaßnahmen
    selected_massnahmen = st.multiselect(
        "Fördermaßnahmen",
        options=list(RATING_COLS),
        format_func=lambda col: RATING_LABELS[col],
        placeholder="Fördermaßnahmen auswählen...",
    )

    # Karrierebarrieren
    selected_barriers = st.multiselect(
        "Karrierebarrieren (optional)",
        options=BARRIER_COLS,
        format_func=lambda col: BARRIER_LABELS[col],
        placeholder="Karrierebarrieren auswählen...",
    )

    if selected_barriers:
        barrier_kombination = st.toggle(
            "Nur exakte Kombination",
            value=False,
            key="barrier_kombination",
            help="Wenn eingeschaltet, werden nur Personen mit ALLEN ausgewählten Barrieren ausgegeben, ansonsten alle Personen mit mindestens einer Barriere.",
        )

st.title("Wirksamkeit von IT-Fördermaßnahmen")
st.markdown("### :grey[nach intersektionalen Konstellationen]")

st.divider()

# Daten laden
df, filter_log = load_data(uploaded_file)

# Case 1: kein Datensatz hochgeladen
if df is None:
    st.info(
        "Lade links in der Sidebar einen Datensatz hoch.",
        icon=":material/upload_file:",
    )
    st.stop()

# Case 2: keine Identitätsmerkmale oder Maßnahmen ausgewählt
if not selected_dims or not selected_massnahmen:
    st.info(
        "Wähle links in der Sidebar Identitätsmerkmale und Fördermaßnahmen aus.",
        icon=":material/info:",
    )
    st.stop()

# ----- Datenbereinigung -----
with st.expander("Datenbereinigung", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Rohdatensatz",
            value=f"n = {filter_log["n_raw"]}",
            help="Gesamtzahl aller eingegangenen Fragebögen",
        )
    with col2:
        st.metric(
            label="Nach Vollständigkeits-Filter",
            value=f"n = {filter_log["n_after_page_filter"]}",
            delta=f"-{filter_log["n_removed_page_filter"]} Zeilen",
            delta_color="yellow",
        )
    with col3:
        st.metric(
            label="Nach Geschlechter-Filter",
            value=f"n = {filter_log["n_after_gender_filter"]}",
            delta=f"-{filter_log["n_removed_gender_filter"]} Zeilen",
            delta_color="yellow",
        )
    with col4:
        st.metric(
            label="Nach Identitätsmerkmale-Filter",
            value=f"n = {filter_log["n_after_iscore_filter"]}",
            delta=f"-{filter_log["n_removed_iscore_filter"]} Zeilen",
            delta_color="yellow",
        )

    st.markdown(
        """
    | Filter | Bedeutung | Begründung | Entfernte Zeilen |
    |--------|-----------|------------|------------------|
    | Vollständigkeits-Filter | Nur vollständig ausgefüllte Fragebögen (Letzte Seite = 5) | Fragen zu den Maßnahmen stehen auf den letzten Seiten (unvollständige Fragebögen haben diese nie erreicht) | {} |
    | Geschlechter-Filter | Nur weiblich + non-binär identifizierende Personen | Forschungsfrage bezieht sich auf Frauen und nicht-binäre Personen in der IT | {} |
    | Identitätsmerkmale-Filter | Nur Personen mit mindestens einem Identitätsmerkmal (i-Score > 0) | Forschungsfrage bezieht sich auf intersektionale Konstellationen - Personen ohne jegliches Merkmal sind nicht Zielgruppe der Untersuchung | {} |
    """.format(
            filter_log["n_removed_page_filter"],
            filter_log["n_removed_gender_filter"],
            filter_log["n_removed_iscore_filter"],
        )
    )

# filter dimensions
df_filtered = filter_df_dimensions(df, selected_dims, dim_kombination)
n_filtered = len(df_filtered)

# filter barriers (optional)
if selected_barriers:
    if barrier_kombination:
        barrier_maske = pd.Series([True] * len(df_filtered), index=df_filtered.index)
        for col in selected_barriers:
            barrier_maske &= df_filtered[col] == True
    else:
        barrier_maske = pd.Series([False] * len(df_filtered), index=df_filtered.index)
        for col in selected_barriers:
            barrier_maske |= df_filtered[col] == True
    df_filtered = df_filtered[barrier_maske]
    n_filtered = len(df_filtered)

# ----- Profil-Beschreibung -----
dim_labels = [IDENTITY_LABELS[dim] for dim in selected_dims]
if dim_kombination:
    merkmale_text = " × ".join(dim_labels)
else:
    merkmale_text = " | ".join(dim_labels)

with st.expander("Profil-Beschreibung", expanded=False):
    st.markdown("### Identitätsmerkmale")
    st.markdown(f"{merkmale_text}")

    if selected_barriers:
        barrier_labels_text = [BARRIER_LABELS[b] for b in selected_barriers]
        if barrier_kombination:
            barrieren_text = " × ".join(barrier_labels_text)
        else:
            barrieren_text = " | ".join(barrier_labels_text)
        st.markdown("### Karrierebarrieren")
        st.markdown(f"{barrieren_text}")

    st.info(f"**{n_filtered} Teilnehmende** im Datensatz entsprechen diesem Profil.")

# Warnung: geringe n
if n_filtered < 10:
    st.warning(
        f"Nur {n_filtered} Teilnehmende mit diesem Profil gefunden. Ergebnisse sind statistisch evtl. nicht aussagekräftig.",
        icon=":material/error:",
    )

# ----- Überblick: Gesamtdatensatz -----
with st.expander("Überblick: Gesamtdatensatz", expanded=False):
    st.markdown(
        f":grey[Die folgenden Diagramme basieren auf dem gesamten Datensatz (n = {filter_log['n_final']}), unabhängig von der aktuellen Filterauswahl.]"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Identitätsmerkmale × Maßnahmen",
            "Karrierebarrieren × Maßnahmen",
            "i-Score × Maßnahmen",
        ]
    )

    with tab1:
        # ----- Heatmap: Identitätsmerkmale × Maßnahmen -----
        st.markdown("## Überblick: Identitätsmerkmale × Fördermaßnahmen")
        st.markdown(":grey[Durchschnittliche Maßnahmenbewertung je Identitätsmerkmal.]")

        # avg_rating aller Maßnahmen für jedes Identitätsmerkmal berechnen
        dim_heatmap_data = []

        for dim_col in IDENTITY_COLS:
            df_has_dim = df[df[dim_col] == True]
            wirksamkeit_has_dim = calculate_effectiveness(df_has_dim, list(RATING_COLS))

            for _, row in wirksamkeit_has_dim.iterrows():
                dim_heatmap_data.append(
                    {
                        "Identitätsmerkmal": IDENTITY_LABELS[dim_col],
                        "Fördermaßnahme": row["massnahme_label"],
                        "Ø Bewertung": row["avg_rating"],
                    }
                )

        df_dim_heatmap = pd.DataFrame(dim_heatmap_data)

        # Pivot für Heatmap-Format
        df_dim_heatmap_pivoted = df_dim_heatmap.pivot(
            index="Fördermaßnahme", columns="Identitätsmerkmal", values="Ø Bewertung"
        )

        fig_dim_heatmap = px.imshow(
            df_dim_heatmap_pivoted,
            color_continuous_scale="Inferno",
            zmin=0,
            zmax=2,
            text_auto=".2f",
            aspect="equal",
            labels={"color": "Ø Bewertung"},
            height=538,
        )

        fig_dim_heatmap.update_layout(
            xaxis_title="",
            yaxis_title="",
            coloraxis_colorbar=dict(
                title="Ø Bewertung",
                tickvals=[0, 1, 2],
                ticktext=["0 - spielt keine Rolle", "1 - hilfreich", "2 - essentiell"],
            ),
        )
        st.plotly_chart(fig_dim_heatmap, width="stretch")

    with tab2:
        # ----- Heatmap: Karrierebarrieren × Maßnahmen -----
        st.markdown("## Überblick: Karrierebarrieren × Fördermaßnahmen")
        st.markdown(":grey[Durchschnittliche Maßnahmenbewertung je Karrierebarriere.]")

        barrier_heatmap_data = []

        for barrier_col in BARRIER_COLS:
            df_has_barrier = df[df[barrier_col] == True]
            if len(df_has_barrier) < 5:
                continue
            effectiveness = calculate_effectiveness(df_has_barrier, list(RATING_COLS))
            for _, row in effectiveness.iterrows():
                barrier_heatmap_data.append(
                    {
                        "Karrierebarriere": BARRIER_LABELS[barrier_col],
                        "Fördermaßnahme": row["massnahme_label"],
                        "Ø Bewertung": row["avg_rating"],
                    }
                )

        df_barrier_heatmap = pd.DataFrame(barrier_heatmap_data)
        df_barrier_heatmap_pivoted = df_barrier_heatmap.pivot(
            index="Fördermaßnahme", columns="Karrierebarriere", values="Ø Bewertung"
        )

        fig_barrier_heatmap = px.imshow(
            df_barrier_heatmap_pivoted,
            color_continuous_scale="Inferno",
            zmin=0,
            zmax=2,
            text_auto=".2f",
            aspect="equal",
            labels={"color": "Ø Bewertung"},
            height=600,
        )
        fig_barrier_heatmap.update_layout(
            xaxis_title="",
            yaxis_title="",
            coloraxis_colorbar=dict(
                title="Ø Bewertung",
                tickvals=[0, 1, 2],
                ticktext=["0 - spielt keine Rolle", "1 - hilfreich", "2 - essentiell"],
            ),
        )
        st.plotly_chart(fig_barrier_heatmap, width="stretch")

    with tab3:
        # ----- Heatmap: i-Score-Kategorie × Maßnahmen & Boxplot: i-Score × Maßnahmen -----
        st.markdown("## Überblick: i-Score × Fördermaßnahmen")
        st.markdown(
            ":grey[Durchschnittliche Maßnahmenbewertung je additivem Intersektionalitäts-Score (*i-Score*).]"
        )

        i_score_ansicht = st.radio(
            "Ansicht",
            options=[
                "i-Score kontinuierlich (1-6)",
                "i-Score-Kategorie (niedrig, mittel, hoch)",
            ],
            horizontal=True,
            key="i_score_ansicht",
        )

        # Heatmap: i-Score kontinuierlich (1-6) × Maßnahmen
        if i_score_ansicht == "i-Score kontinuierlich (1-6)":
            i_score_heatmap_data = []
            for rating_col in RATING_COLS:
                df_grouped = df[["i_score_additiv", rating_col]].dropna()
                grouped = (
                    df_grouped.groupby("i_score_additiv")[rating_col]
                    .mean()
                    .reset_index()
                )
                for _, row in grouped.iterrows():
                    i_score_heatmap_data.append(
                        {
                            "i-Score (Anzahl Merkmale)": int(row["i_score_additiv"]),
                            "Fördermaßnahme": RATING_LABELS[rating_col],
                            "Ø Bewertung": round(row[rating_col], 2),
                        }
                    )

            df_i_score_heatmap = pd.DataFrame(i_score_heatmap_data)
            df_i_score_heatmap_pivoted = df_i_score_heatmap.pivot(
                index="Fördermaßnahme",
                columns="i-Score (Anzahl Merkmale)",
                values="Ø Bewertung",
            )

            fig_i_score_heatmap = px.imshow(
                df_i_score_heatmap_pivoted,
                color_continuous_scale="Inferno",
                zmin=0,
                zmax=2,
                text_auto=".2f",
                aspect="equal",
                labels={"color": "Ø Bewertung"},
                height=530,
            )
            fig_i_score_heatmap.update_layout(
                xaxis_title="i-Score",
                yaxis_title="",
                coloraxis_colorbar=dict(
                    title="Ø Bewertung",
                    tickvals=[0, 1, 2],
                    ticktext=[
                        "0 - spielt keine Rolle",
                        "1 - hilfreich",
                        "2 - essentiell",
                    ],
                ),
            )
            st.plotly_chart(fig_i_score_heatmap, width="stretch")
            st.caption("i-Score = Anzahl zutreffender Identitätsmerkmale (1-6)")

        else:
            # Heatmap: i-Score-Kategorie (niedrig, mittel, hoch) × Maßnahmen
            i_score_heatmap_data = []
            for kategorie in ["niedrig (1)", "mittel (2)", "hoch (≥3)"]:
                df_kategorie = df[df["i_score_kategorie"] == kategorie]
                if len(df_kategorie) < 5:
                    continue
                effectiveness = calculate_effectiveness(df_kategorie, list(RATING_COLS))
                for _, row in effectiveness.iterrows():
                    i_score_heatmap_data.append(
                        {
                            "i-Score-Kategorie": kategorie,
                            "Fördermaßnahme": row["massnahme_label"],
                            "Ø Bewertung": row["avg_rating"],
                        }
                    )

            df_i_score_heatmap = pd.DataFrame(i_score_heatmap_data)
            df_i_score_heatmap_pivoted = df_i_score_heatmap.pivot(
                index="Fördermaßnahme",
                columns="i-Score-Kategorie",
                values="Ø Bewertung",
            )

            # Spalten ordnen
            df_i_score_heatmap_pivoted = df_i_score_heatmap_pivoted[
                ["niedrig (1)", "mittel (2)", "hoch (≥3)"]
            ]

            fig_i_score_heatmap = px.imshow(
                df_i_score_heatmap_pivoted,
                color_continuous_scale="Inferno",
                zmin=0,
                zmax=2,
                text_auto=".2f",
                aspect="equal",
                labels={"color": "Ø Bewertung"},
                height=530,
            )
            fig_i_score_heatmap.update_layout(
                xaxis_title="i-Score-Kategorie",
                yaxis_title="",
                coloraxis_colorbar=dict(
                    title="Ø Bewertung",
                    tickvals=[0, 1, 2],
                    ticktext=[
                        "0 - spielt keine Rolle",
                        "1 - hilfreich",
                        "2 - essentiell",
                    ],
                ),
            )
            st.plotly_chart(fig_i_score_heatmap, width="stretch")
            st.caption(
                "i-Score-Kategorien: niedrig = 1 Merkmal · mittel = 2 Merkmale · hoch ≥ 3 Merkmale"
            )

st.divider()

# Maßnahmenwirksamkeit berechnen
df_wirksamkeit = calculate_effectiveness(df_filtered, selected_massnahmen)
df_raw_wirksamkeit = calculate_effectiveness(df, selected_massnahmen)

# ----- Diagramm: Wirksamkeits-Ranking -----
st.markdown("## Wirksamkeits-Ranking")
st.markdown(
    ":grey[Durchschnittliche Bewertung pro Fördermaßnahme für das ausgewählte Profil.]"
)

sort_wirksamkeits_ranking = st.radio(
    "Sortieren",
    options=["nach Bewertung", "alphabetisch"],
    horizontal=True,
    key="sort_wirksamkeits_ranking",
)

df_wirksamkeits_ranking = df_wirksamkeit.sort_values(
    "avg_rating" if sort_wirksamkeits_ranking == "nach Bewertung" else "massnahme_label"
)

fig_wirksamkeits_ranking = px.bar(
    df_wirksamkeits_ranking,
    x="avg_rating",
    y="massnahme_label",
    orientation="h",
    color="avg_rating",
    color_continuous_scale="Inferno",
    range_color=[0, 2],
    text="avg_rating",
    labels={"avg_rating": "Ø Bewertung (0-2)", "massnahme_label": ""},
    height=350,
)

fig_wirksamkeits_ranking.update_layout(
    coloraxis_colorbar=dict(
        title="Ø Bewertung",
        tickvals=[0, 1, 2],
        ticktext=["0 - spielt keine Rolle", "1 - hilfreich", "2 - essentiell"],
    ),
)
fig_wirksamkeits_ranking.update_traces(textposition="outside")
st.plotly_chart(fig_wirksamkeits_ranking, width="stretch")

st.divider()

# ----- Diagramm: Bewertungsverteilung -----
st.markdown("## Bewertungsverteilung")
st.markdown(
    ":grey[Anteil der Bewertungskategorien pro Fördermaßnahme für das ausgewählte Profil.]"
)

col_option_1, col_option_2 = st.columns(2)
with col_option_1:
    sort_bewertungsverteilung = st.radio(
        "Sortieren",
        options=["nach Bewertung", "alphabetisch"],
        horizontal=True,
        key="sort_bewertungsverteilung",
    )
with col_option_2:
    chart_type_bewertungsverteilung = st.radio(
        "Diagrammtyp",
        options=["Stacked", "Grouped"],
        horizontal=True,
        key="chart_type_bewertungsverteilung",
    )

df_bewertungsverteilung = df_wirksamkeit.sort_values(
    "avg_rating" if sort_bewertungsverteilung == "nach Bewertung" else "massnahme_label"
)

# Daten für stacked/grouped Balkendiagramm vorbereiten
df_melted = df_bewertungsverteilung.melt(
    id_vars=["massnahme_label"],
    value_vars=["perc_essentiell", "perc_hilfreich", "perc_keine_Rolle"],
    var_name="Bewertung",
    value_name="Anteil (%)",
)

df_melted["Bewertung"] = df_melted["Bewertung"].map(
    {
        "perc_essentiell": "essentiell",
        "perc_hilfreich": "hilfreich",
        "perc_keine_Rolle": "spielt keine Rolle",
    }
)

fig_bewertungsverteilung = px.bar(
    df_melted,
    x="Anteil (%)",
    y="massnahme_label",
    text="Anteil (%)",
    color="Bewertung",
    orientation="h",
    barmode="stack" if chart_type_bewertungsverteilung == "Stacked" else "group",
    color_discrete_map={
        "essentiell": ESSENTIELL_GELB,
        "hilfreich": HILFREICH_ROT,
        "spielt keine Rolle": SPIELT_KEINE_ROLLE_VIOLETT,
    },
    labels={"massnahme_label": ""},
    category_orders={"Bewertung": ["essentiell", "hilfreich", "spielt keine Rolle"]},
    height=(450),
)

fig_bewertungsverteilung.update_traces(textposition="outside")
st.plotly_chart(fig_bewertungsverteilung, width="stretch")

st.divider()

# ----- Diagramm: Verfügbarkeit im Unternehmen -----
st.markdown("## Verfügbarkeit im Unternehmen")
st.markdown(
    ":grey[Bei wie vielen Teilnehmenden mit dem ausgewählten Profil werden die Maßnahmen in ihrem Unternehmen umgesetzt?]"
)

df_availability = calculate_availability(df_filtered, selected_massnahmen)

if df_availability.empty:
    st.info("Keine Verfügbarkeitsdaten für die ausgewählten Maßnahmen vorhanden.")
else:
    sort_availability = st.radio(
        "Sortieren",
        options=["nach Verfügbarkeit", "alphabetisch"],
        horizontal=True,
        key="sort_availability",
    )

    df_availability = df_availability.sort_values(
        "perc_available"
        if sort_availability == "nach Verfügbarkeit"
        else "massnahme_label"
    )

    df_availability_melted = df_availability.melt(
        id_vars=["massnahme_label"],
        value_vars=["perc_available", "perc_not_available"],
        var_name="status",
        value_name="Anteil (%)",
    )

    df_availability_melted["status"] = df_availability_melted["status"].map(
        {
            "perc_available": "verfügbar",
            "perc_not_available": "nicht verfügbar",
        }
    )

    fig_availability = px.bar(
        df_availability_melted,
        x="Anteil (%)",
        y="massnahme_label",
        color="status",
        orientation="h",
        barmode="stack",
        color_discrete_map={
            "verfügbar": ESSENTIELL_GELB,
            "nicht verfügbar": HILFREICH_ROT,
        },
        labels={"massnahme_label": ""},
        category_orders={"status": ["verfügbar", "nicht verfügbar"]},
        text="Anteil (%)",
        height=350,
    )
    fig_availability.update_traces(textposition="outside")
    st.plotly_chart(fig_availability, width="stretch")
    st.caption(
        f"Hinweis: Für *Familienfreundlichkeit* und *Frauenanteil* werden keine Verfügbarkeitsdaten angezeigt, da die Maßnahmen im Datensatz nicht eindeutig als `verfügbar` / `nicht verfügbar` erfasst wurden."
    )

st.divider()

# ----- Diagramm: Vergleich mit Gesamtstichprobe -----
st.markdown("## Vergleich mit Gesamtstichprobe")
st.markdown(
    "Durchschnittliche Maßnahmenbewertung des ausgewählten Profils im Vergleich zu der Gesamtheit aller Teilnehmenden."
)

sort_vgl_gesamt = st.radio(
    "Sortieren",
    options=["nach Bewertung", "alphabetisch"],
    horizontal=True,
    key="sort_vgl_gesamt",
)

df_profil = df_wirksamkeit[["massnahme_label", "avg_rating"]].copy()
df_profil["Gruppe"] = "ausgewähltes Profil"

df_gesamt = df_raw_wirksamkeit[["massnahme_label", "avg_rating"]].copy()
df_gesamt["Gruppe"] = "alle Teilnehmenden"

df_vgl_gesamt = pd.concat([df_profil, df_gesamt])

order = (
    df_wirksamkeit.sort_values("avg_rating")["massnahme_label"].tolist()
    if sort_vgl_gesamt == "nach Bewertung"
    else sorted(df_wirksamkeit["massnahme_label"].tolist())
)

fig_vgl_gesamt = px.bar(
    df_vgl_gesamt,
    x="avg_rating",
    y="massnahme_label",
    color="Gruppe",
    orientation="h",
    barmode="group",
    color_discrete_map={
        "ausgewähltes Profil": ESSENTIELL_GELB,
        "alle Teilnehmenden": HILFREICH_ROT,
    },
    category_orders={"massnahme_label": order},
    labels={"avg_rating": "Ø Bewertung (0-2)", "massnahme_label": ""},
    height=350,
)

st.plotly_chart(fig_vgl_gesamt, width="stretch")
st.caption("Bewertungsskala: 0 = spielt keine Rolle · 1 = hilfreich · 2 = essentiell")

st.divider()

st.caption(
    "Im Rahmen der Bachelorarbeit von Van Khanh Luong · Berliner Hochschule für Technik (BHT) · 2026 "
)
