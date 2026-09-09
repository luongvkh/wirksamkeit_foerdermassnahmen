import pandas as pd
import streamlit as st
from constants import (
    IDENTITY_COLS,
    RATING_MAPPING,
    RATING_LABELS,
    RATING_CATEGORY_MAPPING,
    BARRIER_MAPPING,
    BARRIER_COLS_MULTIPLE_CHOICE,
)


# ----- Identitätsdimensionen -----
def has_migration(row):
    val = row.get("Haben Sie einen Migrationshintergrund?", "")
    return val not in [
        "sowohl ich als auch meine Eltern wurden in Deutschland geboren",
        "Keine Antwort",
        "",
    ]


def has_lgbtq(row):
    val = row.get("Was beschreibt am ehesten Ihre sexuelle Orientierung?", "")
    return val not in ["heterosexuell", "Keine Antwort", ""]


def has_kinder(row):
    val = row.get("Familiensituation (Kinder)", "")
    return val not in ["ich habe keine Kinder in meinem Haushalt", "Keine Antwort", ""]


def has_pflege(row):
    val = row.get(
        "Familiensituation (Pflege Angehörige). Pflegen Sie (eine*n) Angehörige*n?", ""
    )
    return val == "ja"


def has_behinderung(row):
    val = row.get("Leben Sie mit einer Behinderung oder chronischen Erkrankung?", "")
    return val not in ["nein", "Keine Antwort", ""]


def has_bildungsfern(row):
    val = row.get("Sozioökonomischer Hintergrund Ihrer Herkunftsfamilie", "")
    return val == "beide Eltern ohne formale Berufsqualifikation"


# ----- Daten laden & verarbeiten -----
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        # load uploaded file
        if uploaded_file.name.endswith(".csv"):
            # seperator auslesen, source: https://stackoverflow.com/a/65153074
            df_comma = pd.read_csv(uploaded_file, nrows=1, sep=",")
            df_semicolon = pd.read_csv(uploaded_file, nrows=1, sep=";")
            seperator = "," if df_comma.shape[1] > df_semicolon.shape[1] else ";"

            uploaded_file.seek(0)  # reset file pointer
            df_raw = pd.read_csv(uploaded_file, sep=seperator)
        else:
            df_raw = pd.read_excel(uploaded_file)
    else:
        try:
            df_raw = pd.read_excel("data/results-survey_final.xlsx")  # load local file
        except FileNotFoundError:
            return None, None  # no local file found

    n_raw = len(df_raw)

    # Filter 1: vollständig beantwortete Fragebögen (bis letzte Seite)
    letzte_seite = int(df_raw["Letzte Seite"].max())
    df = df_raw[df_raw["Letzte Seite"] == letzte_seite].copy()
    n_after_page_filter = len(df)

    # Filter 2: Geschlecht (nur weiblich und non-binär)
    df = df[df["Wie identifizieren Sie sich?"].isin(["weiblich", "non-binär"])]
    n_after_gender_filter = len(df)

    # binäre Spalten für Identitätsdimensionen erstellen
    df["has_migration"] = df.apply(has_migration, axis=1)
    df["has_lgbtq"] = df.apply(has_lgbtq, axis=1)
    df["has_kinder"] = df.apply(has_kinder, axis=1)
    df["has_pflege"] = df.apply(has_pflege, axis=1)
    df["has_behinderung"] = df.apply(has_behinderung, axis=1)
    df["has_bildungsfern"] = df.apply(has_bildungsfern, axis=1)

    # i-Score berechnen (additiv und theoriebasiert)
    df["i_score_additiv"] = sum(df[col].astype(int) for col in IDENTITY_COLS)

    # Filter 3: nur Personen mit mindestens einem Identitätsmerkmal (i_score > 0)
    df = df[df["i_score_additiv"] > 0]
    n_after_iscore_filter = len(df)

    weights_theoriebasiert = {
        "has_bildungsfern": 1.5,
        "has_migration": 1.3,
        "has_pflege": 1.2,
        "has_lgbtq": 1.1,
        "has_behinderung": 1.1,
        "has_kinder": 1.0,
    }
    df["i_score_theoriebasiert"] = sum(
        df[col].astype(float) * w for col, w in weights_theoriebasiert.items()
    )

    df["i_score_kategorie"] = pd.cut(
        df["i_score_additiv"],
        bins=[0, 1, 2, 6],
        labels=["niedrig (1)", "mittel (2)", "hoch (≥3)"],
    )

    # AV RATING_* kodieren
    for new_col, orig_col in RATING_MAPPING.items():
        df[new_col] = df[orig_col].map(RATING_CATEGORY_MAPPING)

    # Barrieren 1-8: Multiple Choice Ja/Nein → True/False
    for col in BARRIER_COLS_MULTIPLE_CHOICE:
        orig_col = BARRIER_MAPPING[col]
        df[col] = df[orig_col].apply(
            lambda v: (
                True
                if str(v).strip() == "Ja"
                else (False if str(v).strip() == "Nein" else None)
            )
        )

    # barrier 9: Beförderungshindernisse → True, wenn Hindernisse vorhanden
    df["barrier_befoerderungshindernisse"] = df[
        BARRIER_MAPPING["barrier_befoerderungshindernisse"]
    ].apply(
        lambda v: (
            True
            if str(v).strip() in ["ja, einige Hindernisse", "ja, deutliche Hindernisse"]
            else (
                False
                if str(v).strip()
                in [
                    "mir sind keine Hindernisse bewusst",
                    "nein, es gibt keine Hindernisse",
                ]
                else None
            )
        )
    )

    # barrier 10: Fehlende Transparenz → True, wenn NICHT transparent
    df["barrier_fehlende_transparenz"] = df[
        BARRIER_MAPPING["barrier_fehlende_transparenz"]
    ].apply(
        lambda v: False if str(v).strip() == "ja" else (None if pd.isna(v) else True)
    )

    # Filter-Log
    filter_log = {
        "n_raw": n_raw,
        "n_after_page_filter": n_after_page_filter,
        "n_removed_page_filter": n_raw - n_after_page_filter,
        "n_after_gender_filter": n_after_gender_filter,
        "n_removed_gender_filter": n_after_page_filter - n_after_gender_filter,
        "n_after_iscore_filter": n_after_iscore_filter,
        "n_removed_iscore_filter": n_after_gender_filter - n_after_iscore_filter,
        "n_final": n_after_iscore_filter,
    }

    return df, filter_log


# ----- Dataframe filtern -----
def filter_df_dimensions(df, selected_dimensions, kombination=True):
    """
    Filtert den Datensatz nach ausgewählten Identitätsmerkmalen.

    `selected_dimensions`: Liste der Identitätsdimensionen, nach denen gefiltert werden soll<br/>
    `kombination=True`: Nur Zeilen, die **alle** ausgewählten Merkmale haben<br/>
    `kombination=False`: Zeilen, die **mindestens eines** der Merkmale haben
    """
    if not selected_dimensions:
        return df

    if kombination:
        # Start: alle Zeilen sind ausgewählt
        maske = pd.Series([True] * len(df), index=df.index)
        for col in selected_dimensions:
            # behalte nur Zeilen, die AUCH dieses Merkmal haben (UND-Verknüpfung)
            maske &= df[col] == True
    else:
        # Start: keine Zeile ist ausgewählt
        maske = pd.Series([False] * len(df), index=df.index)
        for col in selected_dimensions:
            # nehme alle Zeilen dazu, die MINDESTENS dieses Merkmal haben (ODER-Verknüpfung)
            maske |= df[col] == True

    return df[maske]


# ----- Maßnahmenwirksamkeit berechnen -----
def calculate_effectiveness(df, selected_avs):
    """
    Berechnet durchschnittliche Wirksamkeitsbewertung und Prozentzahl aller Bewertungen je Maßnahme.

    `selected_avs`: Liste von AV-Spalten (abhängige Variablen, z.B. rating_mentoring)
    """
    results = []

    for col in selected_avs:
        values = df[col].dropna()
        if len(values) == 0:
            continue
        results.append(
            {
                "av_col": col,
                "massnahme_label": RATING_LABELS[col],
                "n": len(values),
                "avg_rating": round(values.mean(), 2),
                "perc_essentiell": round((values == 2).sum() / len(values) * 100, 1),
                "perc_hilfreich": round((values == 1).sum() / len(values) * 100, 1),
                "perc_keine_Rolle": round((values == 0).sum() / len(values) * 100, 1),
            }
        )

    return pd.DataFrame(results)

# funktioniert für die binär kodierten Maßnahmen (s. constants.py)
def calculate_availability(df, selected_avs):
    """
    Berechnet Verfügbarkeit der Maßnahmen im Unternehmen.
    Gibt Prozentsatz der Teilnehmenden zurück, bei denen die Maßnahme verfügbar ist.

    `selected_avs`: Liste von AV-Spalten (abhängige Variablen, z.B. rating_mentoring)
    """
    availability_col_map = {
        "rating_flexibility": (
            "In meinem Unternehmen wird flexible Arbeitszeit ermöglicht ...",
            lambda v: v
            in [
                "ja, Arbeitszeit und Anwesenheit selbstbestimmbar",
                "flexible Arbeitszeiten mit Präsenzpflicht",
            ],
        ),
        "rating_networks": (
            "In meinem Unternehmen wird die Etablierung und Pflege von diversen sozialen Netzwerken gefördert, um sich untereinander zu organisieren.",
            lambda v: v
            in [
                "ja, aktive Förderung",
                "machen die Mitarbeiter*innen auf eigene Initiative, wird unterstützt",
            ],
        ),
        "rating_mentoring": (
            "In meinem Unternehmen gibt es Mentoring-Programme\xa0",
            lambda v: v
            in [
                "ja, beides",
                "ja, über Hierarchiestufen hinweg",
                "ja, auf kollegialer Ebene",
            ],
        ),
        "rating_jobsharing": (
            "In meinem Unternehmen wird Jobsharing für Führungspositionen ...",
            lambda v: v
            in [
                "angeboten, aber nicht gelebt",
                "angeboten und gelebt",
            ],
        ),
    }

    results = []

    for av_col in selected_avs:
        if av_col not in availability_col_map:
            continue  # Familienfreundlichkeit + Frauenanteil überspringen

        orig_col, is_available = availability_col_map[av_col]
        values = df[orig_col].dropna()
        if len(values) == 0:
            continue

        n_available = values.apply(
            is_available
        ).sum()  # lambda-Funktion auf jeden value anwenden und True-Werte zählen (summieren)
        results.append(
            {
                "av_col": av_col,
                "massnahme_label": RATING_LABELS[av_col],
                "n_values": len(values),
                "n_available": int(n_available),
                "perc_available": round(n_available / len(values) * 100, 1),
                "perc_not_available": round((1 - n_available / len(values)) * 100, 1),
            }
        )

    return pd.DataFrame(results)
