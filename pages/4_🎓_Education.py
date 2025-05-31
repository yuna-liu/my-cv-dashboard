import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
from datetime import datetime

st.set_page_config(page_title="Education Journey", page_icon="🎓")
st.markdown("# 🎓 Education Journey")
st.sidebar.header("Filter Education")
st.write(
    "Dive into my educational story by filtering degrees and years. Each step reflects milestones that shaped my skills and expertise."
)




def encode_image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Local logos base64 encoded
LOGO_PATHS = {
    "NWUPPL": "assets/nwuppl_logo.png",
    "HUMBOLDT": "assets/humboldt_logo.png",
    "UMEA": "assets/umea_logo.png",
    "ITHS": "assets/iths_logo.png"
}

BASE64_ICONS = {
    key: f"data:image/png;base64,{encode_image_to_base64(path)}"
    for key, path in LOGO_PATHS.items()
}

# Add degree level and parse dates for filtering
education_data = pd.DataFrame([
    {
        "institution": "Northwest University of Politics and Law, China",
        "degree": "BSc International Economics and Trade",
        "dates": "2001 – 2005",
        "start_year": 2001,
        "end_year": 2005,
        "degree_level": "Bachelor",
        "lat": 34.2736,
        "lon": 108.9416,
        "icon_data": {
            "url": BASE64_ICONS["NWUPPL"],
            "width": 128,
            "height": 128,
            "anchorY": 128
        }
    },
    {
        "institution": "Humboldt University of Berlin, Germany",
        "degree": "Master in Economics and Management",
        "dates": "2005 – 2008",
        "start_year": 2005,
        "end_year": 2008,
        "degree_level": "Master",
        "lat": 52.5179,
        "lon": 13.3923,
        "icon_data": {
            "url": BASE64_ICONS["HUMBOLDT"],
            "width": 128,
            "height": 128,
            "anchorY": 128
        }
    },
    {
        "institution": "Umeå University, Sweden",
        "degree": "Ph.D. in Economics",
        "dates": "2009 – 2016",
        "start_year": 2009,
        "end_year": 2016,
        "degree_level": "Doctor",
        "lat": 63.8258,
        "lon": 20.2630,
        "icon_data": {
            "url": BASE64_ICONS["UMEA"],
            "width": 128,
            "height": 128,
            "anchorY": 128
        }
    },
    {
        "institution": "IT Högskolan, Gothenburg, Sweden",
        "degree": "Developer in AI and Machine Learning",
        "dates": "2021 – 2023",
        "start_year": 2021,
        "end_year": 2023,
        "degree_level": "Career Education",
        "lat": 57.7089,
        "lon": 11.9746,
        "icon_data": {
            "url": BASE64_ICONS["ITHS"],
            "width": 128,
            "height": 128,
            "anchorY": 128
        }
    }
])

# Sidebar filters
degree_options = ["All"] + education_data["degree_level"].unique().tolist()
selected_degrees = st.sidebar.multiselect("Select Degree Level(s):", degree_options, default=["All"])

years_min = education_data["start_year"].min()
years_max = education_data["end_year"].max()
selected_years = st.sidebar.slider("Select Year Range:", years_min, years_max, (years_min, years_max))

# Filter function
def filter_data(df, degrees, year_range):
    if "All" not in degrees:
        df = df[df["degree_level"].isin(degrees)]
    df = df[
        (df["start_year"] <= year_range[1]) & (df["end_year"] >= year_range[0])
    ]
    return df.reset_index(drop=True)

filtered_data = filter_data(education_data, selected_degrees, selected_years)

if filtered_data.empty:
    st.warning("No education records match the selected filters.")
    st.stop()

# Arc colors start from orange, then green, then blue
arc_colors = [
    [255, 140, 0],     # Orange
    [0, 128, 0],       # Green
    [30, 144, 255]     # Blue
]

arc_data = []
for i in range(len(filtered_data) - 1):
    source = filtered_data.iloc[i]
    target = filtered_data.iloc[i + 1]
    arc_data.append({
        "from_lon": source["lon"],
        "from_lat": source["lat"],
        "to_lon": target["lon"],
        "to_lat": target["lat"],
        "color": arc_colors[i % len(arc_colors)]
    })

arc_layer = pdk.Layer(
    "ArcLayer",
    data=pd.DataFrame(arc_data),
    get_source_position=["from_lon", "from_lat"],
    get_target_position=["to_lon", "to_lat"],
    get_source_color="color",
    get_target_color="color",
    get_width=7,
    width_scale=0.0001,
    width_min_pixels=4,
    width_max_pixels=25,
    auto_highlight=True,
    pickable=True
)

icon_layer = pdk.Layer(
    type="IconLayer",
    data=filtered_data,
    get_icon="icon_data",
    get_size=4,
    size_scale=15,
    get_position=["lon", "lat"],
    pickable=True
)

view_state = pdk.ViewState(
    latitude=filtered_data.iloc[0]['lat'],
    longitude=filtered_data.iloc[0]['lon'],
    zoom=2,
    pitch=45
)

tooltip = {
    "html": "<b>{degree}</b><br>{institution}<br>{dates}",
    "style": {
        "backgroundColor": "black",
        "color": "white"
    }
}

deck = pdk.Deck(
    layers=[icon_layer, arc_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",
    tooltip=tooltip
)

st.pydeck_chart(deck)


# Timeline descending order by start_year
st.markdown("## 📘 Timeline")
for i, row in filtered_data.sort_values(by="start_year", ascending=False).iterrows():
    st.markdown(f"""
    ### {row['degree']}
    **{row['institution']}**  
    _{row['dates']}_
    """)