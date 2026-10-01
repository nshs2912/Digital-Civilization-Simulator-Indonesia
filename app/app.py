from openai import OpenAI
import streamlit as st  # noqa: I001


st.set_page_config(
    page_title="Digital Civilization Simulator Indonesia",
    page_icon="🌏",
    layout="wide",
)

TEXT = {
    "ID": {
        "home": "🏠 Beranda Peradaban",
        "map": "🗺 Peta Peradaban",
        "time": "⏳ Mesin Waktu",
        "civilizations": "🏛 Peradaban",
        "people": "👥 Tokoh",
        "communities": "🏘 Komunitas",
        "places": "📍 Tempat",
        "events": "📜 Peristiwa",
        "culture": "🎨 Budaya",
        "technology": "🔧 Teknologi",
        "economy": "💰 Ekonomi",
        "environment": "🌿 Lingkungan",
        "artifacts": "🏺 Artefak",
        "evidence": "📚 Bukti & Sumber",
        "ai": "🤖 AI Peradaban",
        "era": "🧬 Hidup di Zamannya",
        "simulation": "🎮 Laboratorium Simulasi",
        "language": "Bahasa",
        "explore": "Jelajahi Peradaban",
        "back": "← Kembali ke Beranda",
        "welcome": "Memahami, Menelusuri, dan Merasakan Peradaban Nusantara dari Waktu ke Waktu.",
        "intro": "Platform eksplorasi peradaban berbasis evidence, time, place, knowledge graph, AI, dan simulation.",
        "select": "Pilih modul untuk mulai menjelajah.",
        "status": "Status Platform",
        "configured": "🟢 OpenAI API terkonfigurasi",
        "not_configured": "🟡 OpenAI API belum terkonfigurasi",
        "foundation": "Evidence First",
        "temporal": "Temporal Integrity",
        "security": "AI Security",
        "on": "AKTIF",
        "snapshot": "Civilization Snapshot",
        "period": "Periode",
        "place": "Tempat",
        "year": "Tahun",
        "search": "Cari",
        "query": "Pertanyaan tentang peradaban",
        "ask": "Tanyakan kepada Civilization AI",
        "ai_note": "AI akan ditempatkan di atas Knowledge Graph dan Evidence Graph; jawaban harus dapat ditelusuri ke sumber.",
        "simulation_note": "Simulasi adalah model, bukan fakta sejarah.",
        "choose_language": "Pilih Bahasa / Choose Language",
        "question_empty": "Masukkan pertanyaan.",
        "thinking": "⏳ OpenAI sedang berpikir...",
        "result_ready": "✅ Hasil OpenAI selesai",
        "ai_error": "❌ OpenAI gagal menghasilkan jawaban.",
        "model": "Model OpenAI",
    },
    "EN": {
        "home": "🏠 Civilization Home",
        "map": "🗺 Civilization Map",
        "time": "⏳ Time Machine",
        "civilizations": "🏛 Civilizations",
        "people": "👥 People",
        "communities": "🏘 Communities",
        "places": "📍 Places",
        "events": "📜 Events",
        "culture": "🎨 Culture",
        "technology": "🔧 Technology",
        "economy": "💰 Economy",
        "environment": "🌿 Environment",
        "artifacts": "🏺 Artifacts",
        "evidence": "📚 Evidence & Sources",
        "ai": "🤖 Civilization AI",
        "era": "🧬 Live the Era",
        "simulation": "🎮 Simulation Lab",
        "language": "Language",
        "explore": "Explore Civilization",
        "back": "← Back to Civilization Home",
        "welcome": "Understand, trace, and experience Nusantara civilization across time.",
        "intro": "An exploration platform built around evidence, time, place, knowledge graphs, AI, and simulation.",
        "select": "Choose a module to begin exploring.",
        "status": "Platform Status",
        "configured": "🟢 OpenAI API configured",
        "not_configured": "🟡 OpenAI API not configured",
        "foundation": "Evidence First",
        "temporal": "Temporal Integrity",
        "security": "AI Security",
        "on": "ON",
        "snapshot": "Civilization Snapshot",
        "period": "Period",
        "place": "Place",
        "year": "Year",
        "search": "Search",
        "query": "Ask about civilization",
        "ask": "Ask Civilization AI",
        "ai_note": "AI sits above the Knowledge Graph and Evidence Graph; answers should remain traceable to sources.",
        "simulation_note": "A simulation is a model, not a historical fact.",
        "choose_language": "Choose Language / Pilih Bahasa",
        "question_empty": "Please enter a question.",
        "thinking": "⏳ OpenAI is thinking...",
        "result_ready": "✅ OpenAI result ready",
        "ai_error": "❌ OpenAI could not generate an answer.",
        "model": "OpenAI model",
    },
}

LANGUAGE_OPTIONS = ["ID", "EN"]
DEFAULT_LANGUAGE = "ID"


if "language" not in st.session_state:
    st.session_state.language = DEFAULT_LANGUAGE

language = st.radio(
    TEXT[DEFAULT_LANGUAGE]["choose_language"],
    LANGUAGE_OPTIONS,
    index=LANGUAGE_OPTIONS.index(st.session_state.language),
    horizontal=True,
    format_func=lambda value: "🇮🇩 Bahasa Indonesia" if value == "ID" else "🇬🇧 English",
)
st.session_state.language = language

t = TEXT[language]

MODULES = [
    ("map", "🗺"),
    ("time", "⏳"),
    ("civilizations", "🏛"),
    ("people", "👥"),
    ("communities", "🏘"),
    ("places", "📍"),
    ("events", "📜"),
    ("culture", "🎨"),
    ("technology", "🔧"),
    ("economy", "💰"),
    ("environment", "🌿"),
    ("artifacts", "🏺"),
    ("evidence", "📚"),
    ("ai", "🤖"),
    ("era", "🧬"),
    ("simulation", "🎮"),
]

BOROBUDUR = {
    "name": "Borobudur",
    "period": "Sailendra / 8th–9th century",
    "year": 800,
    "lat": -7.6079,
    "lon": 110.2038,
    "type": "Archaeological site",
}

# Civilization history is represented as overlapping layers rather than a single
# linear "Indonesian civilization". Dates are exploration ranges and may contain
# regional variation or scholarly debate.
HISTORICAL_LAYERS = [
    {
        "id": "deep-human-history",
        "period": "Deep Human History",
        "id_period": "Sejarah Manusia Awal",
        "range": "≥ 2.4 million years ago",
        "start": -2400000,
        "end": -1000,
        "regions": "Java and wider Indonesian archipelago",
        "themes": "human evolution, environment, stone technology, migration",
        "nodes": ["Sangiran", "Early human fossil record", "Stone artifacts"],
        "evidence": "Archaeological + palaeoanthropological",
    },
    {
        "id": "prehistoric-archipelago",
        "period": "Prehistoric & Maritime Communities",
        "id_period": "Masyarakat Prasejarah & Maritim",
        "range": "Before written historical records",
        "start": -1000,
        "end": 400,
        "regions": "Sumatra, Java, Sulawesi, Nusa Tenggara, Maluku and other islands",
        "themes": "settlement, agriculture, seafaring, exchange, ritual, material culture",
        "nodes": ["Austronesian-linked maritime networks", "Megalithic traditions", "Early settlements"],
        "evidence": "Archaeological + material evidence",
    },
    {
        "id": "early-polities",
        "period": "Early Historical Polities",
        "id_period": "Politas Awal Sejarah",
        "range": "c. 4th–7th centuries CE",
        "start": 350,
        "end": 700,
        "regions": "Java, Sumatra, Kalimantan and connected maritime routes",
        "themes": "inscriptions, trade, state formation, religion, agriculture",
        "nodes": ["Kutai", "Tarumanagara", "Early Sumatran polities"],
        "evidence": "Epigraphic + archaeological + textual",
    },
    {
        "id": "srivijaya-maritime",
        "period": "Srivijaya & Maritime Networks",
        "id_period": "Sriwijaya & Jaringan Maritim",
        "range": "c. 7th–13th centuries",
        "start": 650,
        "end": 1300,
        "regions": "Sumatra, Strait of Malacca and wider Southeast Asian maritime networks",
        "themes": "maritime trade, ports, Buddhism, diplomacy, waterways",
        "nodes": ["Srivijaya", "Palembang region", "Strait of Malacca"],
        "evidence": "Epigraphic + archaeological + external textual sources",
    },
    {
        "id": "classical-java",
        "period": "Classical Java",
        "id_period": "Jawa Klasik",
        "range": "c. 8th–15th centuries",
        "start": 750,
        "end": 1500,
        "regions": "Central and East Java",
        "themes": "temples, agrarian systems, court culture, literature, technology",
        "nodes": ["Sailendra", "Mataram-period polities", "Borobudur", "Prambanan", "Kediri", "Singhasari", "Majapahit"],
        "evidence": "Archaeological + epigraphic + literary",
    },
    {
        "id": "islamic-maritime",
        "period": "Islamic Sultanates & Port Cities",
        "id_period": "Kesultanan Islam & Kota Pelabuhan",
        "range": "c. 13th–19th centuries",
        "start": 1200,
        "end": 1900,
        "regions": "Sumatra, Java, Kalimantan, Sulawesi, Maluku and Nusa Tenggara",
        "themes": "Islamization, ports, trade, scholarship, diplomacy, local kingdoms",
        "nodes": ["Samudra Pasai", "Demak", "Aceh", "Banten", "Mataram Islam", "Makassar", "Ternate-Tidore"],
        "evidence": "Archaeological + archival + literary + oral traditions",
    },
    {
        "id": "colonial-transformations",
        "period": "European Colonial Expansion & Transformations",
        "id_period": "Ekspansi Kolonial Eropa & Transformasi",
        "range": "16th–20th centuries",
        "start": 1500,
        "end": 1942,
        "regions": "Archipelago-wide, with different regional trajectories",
        "themes": "trade monopolies, colonial administration, plantation economy, resistance, migration",
        "nodes": ["VOC", "Colonial port cities", "Local resistance movements", "Plantation regions"],
        "evidence": "Archival + archaeological + oral + material",
    },
    {
        "id": "national-movement",
        "period": "National Movement",
        "id_period": "Pergerakan Nasional",
        "range": "c. 1900–1942",
        "start": 1900,
        "end": 1942,
        "regions": "Major cities and networks across the archipelago",
        "themes": "education, organizations, press, labor, political movements, identity",
        "nodes": ["Urban associations", "Print culture", "Youth movements", "Anti-colonial organizations"],
        "evidence": "Archival + newspapers + memoirs + oral histories",
    },
    {
        "id": "occupation-revolution",
        "period": "Japanese Occupation & Revolution",
        "id_period": "Pendudukan Jepang & Revolusi",
        "range": "1942–1949",
        "start": 1942,
        "end": 1949,
        "regions": "Across the Indonesian archipelago, with regional differences",
        "themes": "occupation, mobilization, independence, diplomacy, armed conflict",
        "nodes": ["1945 Proclamation", "Revolutionary governments", "Diplomacy", "Regional struggles"],
        "evidence": "Archival + oral history + material evidence",
    },
    {
        "id": "early-republic",
        "period": "Early Republic",
        "id_period": "Republik Awal",
        "range": "1950–1965",
        "start": 1950,
        "end": 1965,
        "regions": "Republic of Indonesia",
        "themes": "state formation, regional politics, economy, culture, education",
        "nodes": ["Early republican institutions", "Regional movements", "National development"],
        "evidence": "Archival + statistical + oral + material",
    },
    {
        "id": "new-order",
        "period": "New Order",
        "id_period": "Orde Baru",
        "range": "1966–1998",
        "start": 1966,
        "end": 1998,
        "regions": "Republic of Indonesia",
        "themes": "centralization, development, industrialization, urbanization, social change",
        "nodes": ["Industrialization", "Transmigration", "Urban growth", "Political institutions"],
        "evidence": "Archival + statistical + oral + material",
    },
    {
        "id": "reformasi",
        "period": "Reformasi & Contemporary Indonesia",
        "id_period": "Reformasi & Indonesia Kontemporer",
        "range": "1998–present",
        "start": 1998,
        "end": 2026,
        "regions": "Republic of Indonesia",
        "themes": "democratization, decentralization, digital society, cultural change, environment",
        "nodes": ["Reformasi", "Decentralization", "Digital transformation", "Contemporary communities"],
        "evidence": "Archival + statistical + digital + oral + material",
    },
]

REGIONS = [
    ("All", "Seluruh Nusantara / All Nusantara"),
    ("Sumatra", "Sumatra"),
    ("Java", "Jawa / Java"),
    ("Kalimantan", "Kalimantan"),
    ("Sulawesi", "Sulawesi"),
    ("Bali-Nusa Tenggara", "Bali-Nusa Tenggara"),
    ("Maluku", "Maluku"),
    ("Papua", "Papua"),
    ("Maritime", "Jaringan Maritim / Maritime Networks"),
]


def go_home() -> None:
    st.session_state.page = "home"


def open_page(key: str) -> None:
    st.session_state.page = key


if "page" not in st.session_state:
    st.session_state.page = "home"

st.sidebar.title("🌏 Digital Civilization")
st.sidebar.caption("Experience Indonesia Across Time")
if st.sidebar.button(t["home"], use_container_width=True):
    go_home()

st.sidebar.divider()
for key, icon in MODULES:
    if st.sidebar.button(
        f"{icon} {t[key]}",
        key=f"nav_{key}",
        use_container_width=True,
    ):
        open_page(key)

st.sidebar.divider()
st.sidebar.caption("🔐 API key status: configured / not configured only.")


def page_header(title: str, subtitle: str) -> None:
    if st.button(t["back"], key=f"back_{st.session_state.page}"):
        go_home()
        st.rerun()
    st.title(title)
    st.caption(subtitle)


def render_home() -> None:
    st.title("🌏 DIGITAL CIVILIZATION SIMULATOR INDONESIA")
    st.subheader("AI-Powered. Across Time. Experience the Civilization of Nusantara.")
    st.write(t["welcome"])
    st.info(t["intro"])

    openai_api_key = st.secrets.get("OPENAI_API_KEY", "")

    if openai_api_key:
        st.success(t["configured"])
    else:
        st.warning(t["not_configured"])

    st.divider()
    st.subheader("🧭 " + t["explore"])
    st.write(t["select"])

    columns = st.columns(4)
    for index, (key, icon) in enumerate(MODULES):
        with columns[index % 4]:
            if st.button(
                f"{icon} {t[key]}",
                key=f"home_{key}",
                use_container_width=True,
            ):
                open_page(key)
                st.rerun()

    st.divider()
    st.subheader("🧩 " + t["status"])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t["foundation"], t["on"])
        st.caption("Knowledge remains traceable to evidence and sources.")
    with col2:
        st.metric(t["temporal"], t["on"])
        st.caption("Claims are checked against historical time context.")
    with col3:
        st.metric(t["security"], t["on"])
        st.caption("Credentials stay outside source code.")

    st.divider()
    st.subheader("🌏 Indonesia / Nusantara Civilization Atlas")
    st.write(
        "The simulator is designed as a multi-era, multi-region civilization atlas. "
        "Borobudur is only one pilot site inside the larger historical landscape."
    )
    active_year = st.slider("Explore a starting year / Pilih tahun awal", -2400000, 2026, 800, 100)
    matching = [
        layer for layer in HISTORICAL_LAYERS
        if layer["start"] <= active_year <= layer["end"]
    ]
    st.write(f"**{len(matching)} historical layer(s) intersect this time.**")
    cols = st.columns(3)
    for index, layer in enumerate(matching[:6]):
        with cols[index % 3], st.container(border=True):
                st.markdown(f"**⏳ {layer['period']}**")
                st.caption(layer["range"])
                st.write(layer["themes"])
                if st.button(
                    "Explore / Jelajahi",
                    key=f"home_layer_{layer['id']}",
                    use_container_width=True,
                ):
                    st.session_state.page = "time"
                    st.session_state.selected_layer = layer["id"]
                    st.rerun()

    st.divider()
    st.subheader("⭐ Pilot Vertical Slice: Borobudur")
    st.caption(
        "Pilot site, not the scope of the whole simulator. "
        "More regions and periods are first-class entities."
    )
    if st.button("🧭 Explore Borobudur / Jelajahi Borobudur", use_container_width=True):
        st.session_state.page = "places"
        st.session_state.selected_place = "Borobudur"
        st.rerun()


def render_map() -> None:
    page_header(t["map"], "Explore a multi-region historical landscape.")
    points = [
        {"name": "Sangiran", "lat": -7.45, "lon": 110.83},
        {"name": "Borobudur", "lat": -7.6079, "lon": 110.2038},
        {"name": "Prambanan", "lat": -7.752, "lon": 110.491},
        {"name": "Palembang region", "lat": -2.99, "lon": 104.76},
        {"name": "Ternate", "lat": 0.79, "lon": 127.38},
        {"name": "Makassar", "lat": -5.1477, "lon": 119.4327},
        {"name": "Banten region", "lat": -6.03, "lon": 106.16},
        {"name": "Bali", "lat": -8.34, "lon": 115.09},
    ]
    st.map(points, latitude="lat", longitude="lon", zoom=4)
    st.caption(
        "Map points are representative exploration nodes, not a claim that each "
        "location defines a whole civilization."
    )


def render_time() -> None:
    page_header(
        t["time"],
        "Explore the Indonesian/Nusantara historical landscape across deep time, "
        "regions, and civilization layers.",
    )
    selected_region = st.selectbox(
        "🌏 Region / Wilayah",
        REGIONS,
        format_func=lambda item: item[1],
    )[0]
    min_year = min(layer["start"] for layer in HISTORICAL_LAYERS)
    max_year = max(layer["end"] for layer in HISTORICAL_LAYERS)
    year = st.slider(
        t["year"],
        min_year,
        max_year,
        800,
        100,
    )

    active = [
        layer
        for layer in HISTORICAL_LAYERS
        if layer["start"] <= year <= layer["end"]
        and (
            selected_region == "All"
            or selected_region.lower() in layer["regions"].lower()
            or selected_region == "Maritime"
            and "maritime" in layer["regions"].lower()
        )
    ]

    st.subheader(f"🌏 {t['snapshot']} — {year}")
    if not active:
        st.info(
            "No curated layer is shown for this exact combination yet. "
            "The absence of a layer is not evidence that history was absent."
        )
        return

    for layer in active:
        with st.container(border=True):
            st.subheader(f"⏳ {layer['period']} / {layer['id_period']}")
            st.write(f"**Range:** {layer['range']}")
            st.write(f"**Regions:** {layer['regions']}")
            st.write(f"**Themes:** {layer['themes']}")
            st.write("**Representative nodes:** " + ", ".join(layer["nodes"]))
            st.caption(f"🟢 Evidence layer: {layer['evidence']}")

    st.info(
        "Temporal layers overlap. They are not a claim that one civilization "
        "replaced another everywhere at the same time."
    )


def render_catalog(key: str, title: str, items: list[str]) -> None:
    page_header(title, "Browse the current evidence-grounded catalog.")
    search = st.text_input(t["search"])
    shown = [item for item in items if search.lower() in item.lower()]
    if not shown:
        st.info("No matching items." if language == "EN" else "Tidak ada item yang cocok.")
        return
    for item in shown:
        with st.container(border=True):
            st.subheader(item)
            st.caption("🟢 Evidence-linked record / Rekaman terhubung bukti")
            st.write(
                "Detailed records will expand as the knowledge graph and source registry "
                "grow."
                if language == "EN"
                else "Rekaman detail akan berkembang seiring knowledge graph dan source registry."
            )


def render_places() -> None:
    page_header(t["places"], "Historical and archaeological places.")
    st.subheader("📍 Borobudur")
    st.write("Central Java, Indonesia")
    st.write(f"Coordinates: {BOROBUDUR['lat']}, {BOROBUDUR['lon']}")
    st.write(f"Context: {BOROBUDUR['type']}")
    st.success("🟢 Evidence / Bukti")
    if st.button("🗺 View on Civilization Map", use_container_width=True):
        open_page("map")
        st.rerun()


def render_events() -> None:
    render_catalog(
        "events",
        t["events"],
        ["Borobudur construction tradition", "Śailendra-period Buddhist activity"],
    )


def render_evidence() -> None:
    page_header(t["evidence"], "Evidence, sources, and provenance.")
    rows = [
        ["ARCHAEOLOGICAL", "DIRECT", "Borobudur monument and archaeological context"],
        ["EPIGRAPHIC", "DIRECT", "Inscriptional evidence where available"],
        ["LITERARY", "CONTEXTUAL", "Historical and religious textual context"],
    ]
    st.table(
        {
            "Evidence Type": [row[0] for row in rows],
            "Strength": [row[1] for row in rows],
            "Description": [row[2] for row in rows],
        }
    )
    st.info(
        "Evidence strength, model confidence, and claim status are separate concepts."
    )


def render_ai() -> None:
    page_header(t["ai"], "Evidence-grounded historical reasoning.")
    st.info(t["ai_note"])
    query = st.text_area(
        t["query"],
        placeholder=(
            "Contoh: Mengapa Borobudur dibangun?"
            if language == "ID"
            else "Example: Why was Borobudur built?"
        ),
    )

    if st.button("🤖 " + t["ask"], type="primary", use_container_width=True):
        if not query.strip():
            st.warning(t["question_empty"])
            return

        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key:
            st.error(t["not_configured"])
            return

        system_prompt = (
            "You are Civilization AI for the Digital Civilization Simulator Indonesia. "
            "Answer historical questions carefully. Distinguish established facts from "
            "interpretation and uncertainty. Never invent sources, evidence, dates, or "
            "citations. If the platform has not supplied retrieved evidence, explicitly "
            "say that the answer is general historical context rather than a verified "
            "Evidence Graph result. Answer in the user's selected language."
        )
        user_prompt = (
            f"Language: {'Indonesian' if language == 'ID' else 'English'}\\n"
            f"Historical question: {query.strip()}"
        )

        try:
            client = OpenAI(api_key=api_key)
            with st.spinner(t["thinking"]):
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions=system_prompt,
                    input=user_prompt,
                )

            answer = (response.output_text or "").strip()
            if not answer:
                st.error(t["ai_error"])
                return

            st.success(t["result_ready"])
            st.caption(f"{t['model']}: gpt-4.1-mini")
            with st.container(border=True):
                st.markdown("### 🤖 Civilization AI")
                st.write(answer)
            st.caption(
                "🟡 Interpretation / Context — until Evidence Graph retrieval and "
                "source citation are connected."
                if language == "EN"
                else "🟡 Interpretasi / Konteks — sampai Evidence Graph retrieval "
                "dan sitasi sumber terhubung."
            )
        except Exception as exc:
            st.error(t["ai_error"])
            st.caption(f"{type(exc).__name__}: {exc}")


def render_era() -> None:
    page_header(t["era"], "Experience daily life as an evidence-labelled reconstruction.")
    st.subheader("🧑 A day near Borobudur")
    st.write(
        "A future reconstruction can combine occupation, food, trade, ritual, "
        "environment, technology, and community evidence."
    )
    st.warning(
        "🔵 Simulation / Simulasi — experiential reconstruction, not a literal historical transcript."
    )


def render_simulation() -> None:
    page_header(t["simulation"], "Run transparent historical scenarios.")
    st.info(t["simulation_note"])

    baseline = st.selectbox(
        "Baseline / Dasar",
        ["Borobudur around 800 CE"],
    )
    assumption = st.selectbox(
        "Scenario assumption / Asumsi skenario",
        [
            "Trade activity increases",
            "Trade activity decreases",
            "Environmental pressure increases",
        ],
    )
    intensity = st.slider(
        "Scenario intensity / Intensitas skenario",
        10,
        50,
        25,
        5,
    )

    st.write(f"**Baseline:** {baseline}")
    st.write(f"**Assumption:** {assumption}")
    st.write(f"**Intensity:** {intensity}%")

    if st.button("🎮 Run Scenario / Jalankan Skenario", use_container_width=True):
        with st.spinner(
            "⏳ Scenario engine sedang menjalankan model..."
            if language == "ID"
            else "⏳ Scenario engine is running the model..."
        ):
            # This is an illustrative simulation model, not a reconstruction of
            # measured historical quantities. Baseline index = 100.
            trade_index = 100
            exchange_index = 100
            environment_pressure = 100
            resilience_index = 100

            delta = intensity / 100
            if assumption == "Trade activity increases":
                trade_index += 100 * delta
                exchange_index += 60 * delta
                environment_pressure += 20 * delta
                resilience_index += 10 * delta
            elif assumption == "Trade activity decreases":
                trade_index -= 100 * delta
                exchange_index -= 60 * delta
                environment_pressure -= 10 * delta
                resilience_index -= 15 * delta
            else:
                environment_pressure += 100 * delta
                exchange_index -= 30 * delta
                resilience_index -= 70 * delta

            scenario_rows = [
                [
                    "Trade activity / Aktivitas perdagangan",
                    100,
                    round(trade_index, 1),
                ],
                [
                    "Exchange / Pertukaran",
                    100,
                    round(exchange_index, 1),
                ],
                [
                    "Environmental pressure / Tekanan lingkungan",
                    100,
                    round(environment_pressure, 1),
                ],
                [
                    "Resilience / Ketahanan",
                    100,
                    round(resilience_index, 1),
                ],
            ]

        st.success(
            "✅ Scenario completed / Skenario selesai"
        )
        st.caption(
            "🔵 Simulation — illustrative index model. It is hypothetical and "
            "must not be presented as historical fact."
        )
        st.subheader("📊 Scenario Output / Hasil Skenario")
        st.table(
            {
                "Dimension / Dimensi": [row[0] for row in scenario_rows],
                "Baseline Index": [row[1] for row in scenario_rows],
                "Scenario Index": [row[2] for row in scenario_rows],
            }
        )
        st.write(
            "**Model boundary / Batas model:** baseline + assumption + intensity + "
            "illustrative rules + uncertainty."
        )
        st.warning(
            "These indices are model outputs, not historical measurements. "
            "Evidence retrieval and calibrated historical models are required before "
            "using real historical claims."
            if language == "EN"
            else "Indeks ini adalah keluaran model, bukan pengukuran historis. "
            "Evidence retrieval dan model historis yang terkalibrasi diperlukan "
            "sebelum membuat klaim historis nyata."
        )


catalogs = {
    "civilizations": ["Sailendra", "Srivijaya", "Majapahit", "Mataram Kuno"],
    "people": ["Historical figures — evidence records expanding"],
    "communities": ["Buddhist communities", "Artisan communities", "Trading communities"],
    "culture": ["Buddhist art", "Architecture", "Religious practice", "Maritime culture"],
    "technology": ["Stone construction", "Water management", "Maritime technology"],
    "economy": ["Agriculture", "Craft production", "Trade networks"],
    "environment": ["Volcanic landscape", "River systems", "Agricultural environment"],
    "artifacts": ["Borobudur reliefs", "Stupas", "Inscriptions"],
}

renderers = {
    "home": render_home,
    "map": render_map,
    "time": render_time,
    "places": render_places,
    "events": render_events,
    "evidence": render_evidence,
    "ai": render_ai,
    "era": render_era,
    "simulation": render_simulation,
}

if st.session_state.page in catalogs:
    render_catalog(st.session_state.page, t[st.session_state.page], catalogs[st.session_state.page])
else:
    renderers[st.session_state.page]()
