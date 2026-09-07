# ----- App-Farben, entsprechend des "Inferno" Themes von plotly.express -----
ESSENTIELL_GELB = "#FBF388"
HILFREICH_ROT = "#9E323C"
SPIELT_KEINE_ROLLE_VIOLETT = "#260C4B"

# ----- Identitätsmerkmale -----
IDENTITY_LABELS = {
    "has_migration": "Migration",
    "has_lgbtq": "LGBTQ+",
    "has_kinder": "Kinder",
    "has_pflege": "Pflege",
    "has_behinderung": "Behinderung",
    "has_bildungsfern": "Bildungsfern",
}

IDENTITY_COLS = list(IDENTITY_LABELS.keys())

# ----- AV: Bewertungen der Wirksamkeit von Fördermaßnahmen -----
RATING_MAPPING = {
    "rating_flexibility": "Wie hilfreich sind/wären flexible Arbeitszeiten für Ihre persönliche Situation?",
    "rating_networks": "Wie hilfreich ist/wäre die Förderung der Etablierung und Pflege von sozialen Netzwerken für Ihre persönliche Situation?",
    "rating_mentoring": "Wie hilfreich ist/wäre Mentoring für Ihre persönliche Situation?",
    "rating_family_friendliness": "Wie hilfreich ist/wäre Familienfreundlichkeit für Ihre persönliche Situation?",
    "rating_womens_quota": "Wie hilfreich ist/wäre ein hoher Frauenanteil für Ihre persönliche Situation?",
    "rating_jobsharing": "Wie hilfreich ist/wäre Jobsharing für Führungspositionen für Ihre persönliche Situation?",
}

RATING_CATEGORY_MAPPING = {
    "essentiell": 2,
    "hilfreich": 1,
    "spielen für mich keine Rolle": 0,
    "Keine Antwort": None,
    "": None,
    None: None,
}

RATING_LABELS = {
    "rating_flexibility": "Flexible Arbeitszeiten",
    "rating_networks": "Soziale Netzwerke",
    "rating_mentoring": "Mentoring",
    "rating_family_friendliness": "Familienfreundlichkeit",
    "rating_womens_quota": "Hoher Frauenanteil",
    "rating_jobsharing": "Jobsharing (Führung)",
}

RATING_COLS = list(RATING_LABELS.keys())

# ----- Verfügbarkeit der Maßnahmen im Unternehmen -----
AVAILABILITY_MAPPING = {
    "availability_flexibility": "In meinem Unternehmen wird flexible Arbeitszeit ermöglicht ...",
    "availability_networks": "In meinem Unternehmen wird die Etablierung und Pflege von diversen sozialen Netzwerken gefördert, um sich untereinander zu organisieren.",
    "availability_mentoring": "In meinem Unternehmen gibt es Mentoring-Programme\xa0",  # (wahrscheinlich von Excel eingefügtes) Leerzeichen am Ende
    "availability_family_friendliness": None,  # im Datensatz nicht eindeutig
    "availability_womens_quota": None,  # im Datensatz nicht eindeutig
    "availability_jobsharing": "In meinem Unternehmen wird Jobsharing für Führungspositionen ...",
}

# ----- Karrierebarrieren -----
BARRIER_MAPPING = {
    "barrier_kompetenz_beweisen": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [ich musste meine Kompetenz häufiger unter Beweis stellen als andere]",
    "barrier_ideen_ueberhoert": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [meine Ideen wurden überhört, aber später von anderen aufgegriffen]",
    "barrier_befoerderung_uebergangen": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [ich wurde trotz Qualifikation bei Beförderungen übergangen]",
    "barrier_faehigkeiten_angezweifelt": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [Kolleg*innen äußerten Zweifel an meinen technischen Fähigkeiten]",
    "barrier_weniger_herausforderungen": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [ich erhielt weniger herausfordernde Projekte zugeteilt]",
    "barrier_schlechtere_gehaltsverhandlung": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [meine Gehaltsverhandlungen verliefen schlechter als erwartet]",
    "barrier_ausschluss_in_netzwerken": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [ich fühlte mich in informellen Netzwerken ausgeschlossen]",
    "barrier_kommentare_identitaet": "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt? (Mehrfach-Auswahl möglich) [ich erlebte Kommentare zu meinem Aussehen/Geschlecht/Herkunft]",
    "barrier_befoerderungshindernisse": "Sehen Sie für sich persönliche Hindernisse bei Beförderungen?",
    "barrier_fehlende_transparenz": "In meinem Unternehmen sind die Beförderungskriterien transparent.",
}

BARRIER_LABELS = {
    "barrier_kompetenz_beweisen": "Kompetenz beweisen (prove-it-again)",
    "barrier_ideen_ueberhoert": "Ideen überhört",
    "barrier_befoerderung_uebergangen": "Bei Beförderung übergangen",
    "barrier_faehigkeiten_angezweifelt": "Zweifel an Fähigkeiten",
    "barrier_weniger_herausforderungen": "Weniger herausfordernde Projekte",
    "barrier_schlechtere_gehaltsverhandlung": "Schlechte Gehaltsverhandlungen",
    "barrier_ausschluss_in_netzwerken": "Netzwerkausschluss",
    "barrier_kommentare_identitaet": "Kommentare zu Identität",
    "barrier_befoerderungshindernisse": "Beförderungshindernisse",
    "barrier_fehlende_transparenz": "Fehlende Transparenz (Beförderung)",
}

BARRIER_COLS = list(BARRIER_LABELS.keys())

# Barrieren mit Binär-Kodierung (Ja/Nein) -> MC-Frage "Haben Sie in Ihrem beruflichen IT-Umfeld folgende Situationen mindestens einmal erlebt?"
BARRIER_COLS_MULTIPLE_CHOICE = [
    "barrier_kompetenz_beweisen",
    "barrier_ideen_ueberhoert",
    "barrier_befoerderung_uebergangen",
    "barrier_faehigkeiten_angezweifelt",
    "barrier_weniger_herausforderungen",
    "barrier_schlechtere_gehaltsverhandlung",
    "barrier_ausschluss_in_netzwerken",
    "barrier_kommentare_identitaet",
]
