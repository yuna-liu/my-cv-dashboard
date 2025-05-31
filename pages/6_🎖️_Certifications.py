import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Certifications", page_icon="📜")

st.title("🎖️ Certifications")

# Sample certification data
data = [
    {
        "Certification": "Microsoft Certified: Azure Data Engineer Associate",
        "Issuer": "Microsoft",
        "Issue Date": "2024-09",
        "Expiry Date": None,
        "Area": "Cloud/Data Engineering",
    },
    {
        "Certification": "Databricks Certified Machine Learning Professional",
        "Issuer": "Databricks",
        "Issue Date": "2025-01",
        "Expiry Date": "2027-01",
        "Area": "Machine Learning",
    },
    {
        "Certification": "Matillion Associate Certification",
        "Issuer": "Matillion",
        "Issue Date": "2024-08",
        "Expiry Date": "2027-08",
        "Area": "Data Engineering",
    },
    {
        "Certification": "Credit Risk Modeling in Python 2021",
        "Issuer": "Udemy",
        "Issue Date": "2021-12",
        "Expiry Date": None,
        "Area": "Risk Modeling",
    },
]

df = pd.DataFrame(data)

# Sidebar filters
issuers = ["All"] + sorted(df["Issuer"].unique().tolist())
areas = ["All"] + sorted(df["Area"].unique().tolist())

selected_issuers = st.sidebar.multiselect("Filter by Issuer", issuers, default=["All"])
selected_areas = st.sidebar.multiselect("Filter by Area", areas, default=["All"])

def filter_df(df, issuers, areas):
    if "All" not in issuers:
        df = df[df["Issuer"].isin(issuers)]
    if "All" not in areas:
        df = df[df["Area"].isin(areas)]
    return df

filtered_df = filter_df(df, selected_issuers, selected_areas)

st.write(f"### Showing {len(filtered_df)} certifications")
st.dataframe(filtered_df.reset_index(drop=True))

# Plot: Number of Certifications by Issuer and Area
if not filtered_df.empty:
    chart_data = (
        filtered_df.groupby(["Issuer", "Area"])
        .size()
        .reset_index(name="Count")
    )

    chart = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X("Issuer:N", title="Issuer"),
            y=alt.Y("Count:Q", title="Number of Certifications"),
            color="Area:N",
            tooltip=["Issuer", "Area", "Count"],
        )
        .properties(width=700, height=400, title="Certifications Count by Issuer and Area")
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No certifications match the selected filters.")
