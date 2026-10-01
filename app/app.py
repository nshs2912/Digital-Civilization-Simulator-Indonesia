from pathlib import Path
import sys

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.civilization.ai import get_openai_api_key  # noqa: E402


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
    },
}

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


def go_home() -> None:
    st.session_state.page = "home"


def open_page(key: str) -> None:
    st.session_state.page = key


if "page" not in st.session_state:
    st.session_state.page = "home"

language = st.sidebar.selectbox(
    "🇮🇩 / 🇬🇧",
    ["ID", "EN"],
    format_func=lambda value: "🇮🇩 Bahasa Indonesia" if value == "ID" else "🇬🇧 English",
)
t = TEXT[language]

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

    try:
        openai_api_key = get_openai_api_key()
    except RuntimeError:
        openai_api_key = None

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
    st.subheader("⭐ Pilot Vertical Slice: Borobudur")
    st.write(
        "Place → Time → Civilization Snapshot → People → Community → "
        "Knowledge Graph → Evidence → AI Guide"
    )
    if st.button("🧭 Explore Borobudur / Jelajahi Borobudur", use_container_width=True):
        st.session_state.page = "places"
        st.session_state.selected_place = "Borobudur"
        st.rerun()


def render_map() -> None:
    page_header(t["map"], "Explore historical places with spatial context.")
    st.map(
        {"lat": [BOROBUDUR["lat"]], "lon": [BOROBUDUR["lon"]]},
        latitude="lat",
        longitude="lon",
        zoom=6,
    )
    st.success("📍 Borobudur — Central Java, Indonesia")
    st.caption(
        "Spatial context is historical/archaeological context; modern administrative "
        "boundaries are not projected backward automatically."
    )


def render_time() -> None:
    page_header(t["time"], "Move through historical time and inspect civilization snapshots.")
    year = st.slider(t["year"], 600, 1200, BOROBUDUR["year"], 25)
    st.subheader(f"{t['snapshot']} — {year}")
    st.write(f"**{t['place']}:** {BOROBUDUR['name']}")
    st.write(f"**{t['period']}:** {BOROBUDUR['period']}")
    st.info(
        "This is a derived snapshot. It represents a modelled state at a selected "
        "time and place, not a replacement for primary evidence."
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
    query = st.text_area(t["query"], placeholder="Contoh: Mengapa Borobudur dibangun?")
    if st.button("🤖 " + t["ask"], type="primary", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a question." if language == "EN" else "Masukkan pertanyaan.")
        else:
            st.info(
                "Civilization AI interface is ready. Retrieval + evidence citation "
                "will be connected in the next engine stage."
                if language == "EN"
                else "Antarmuka Civilization AI siap. Retrieval + sitasi evidence "
                "akan dihubungkan pada tahap engine berikutnya."
            )
            st.caption("Answer type: UNKNOWN — no historical claim has been generated yet.")


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
    baseline = st.selectbox("Baseline / Dasar", ["Borobudur around 800 CE"])
    assumption = st.selectbox(
        "Scenario assumption / Asumsi skenario",
        [
            "Trade activity increases",
            "Trade activity decreases",
            "Environmental pressure increases",
        ],
    )
    st.write(f"**Baseline:** {baseline}")
    st.write(f"**Assumption:** {assumption}")
    if st.button("🎮 Run Scenario / Jalankan Skenario", use_container_width=True):
        st.success(
            "Scenario boundary created: baseline + assumption + model + uncertainty."
        )
        st.caption(
            "🔵 Simulation output is hypothetical and must not be presented as historical fact."
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
