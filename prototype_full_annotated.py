import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# ------------------------------
# Page config
# ------------------------------
st.set_page_config(
    page_title="AI eDNA Dashboard",
    layout="wide",
    page_icon="🧬"
)

st.title("🌊 AI-powered eDNA Biodiversity Dashboard")
st.markdown("Analyze environmental DNA sequences and predict species with AI.")

# ------------------------------
# Sample dataset with annotations
# ------------------------------
data = {
    "SampleID": ["S1", "S2", "S3", "S4", "S5"],
    "eDNA_Sequence": [
        "ATCGTACGATCG",
        "GCTAGCTAGCTA",
        "TTAGGCATCGAT",
        "CGATCGTACGTA",
        "ATGCGTACGTAG"
    ],
    "PredictedSpecies": [
        "Species A",
        "Species B",
        "Species C",
        "Species D",
        "Species E"
    ],
    "Annotation": [
        "GeneX: Present, GeneY: Absent",
        "GeneX: Absent, GeneY: Present",
        "GeneX: Present, GeneY: Present",
        "GeneX: Absent, GeneY: Absent",
        "GeneX: Present, GeneY: Partial"
    ]
}

df = pd.DataFrame(data)

# ------------------------------
# Sidebar filter
# ------------------------------
st.sidebar.header("Filters")
selected_species = st.sidebar.multiselect(
    "Select Species to View",
    options=df["PredictedSpecies"].unique(),
    default=df["PredictedSpecies"].unique()
)

filtered_df = df[df["PredictedSpecies"].isin(selected_species)]

# ------------------------------
# Data table with annotations
# ------------------------------
st.subheader("Predicted Species & Annotations")
st.dataframe(filtered_df[["SampleID", "PredictedSpecies", "eDNA_Sequence", "Annotation"]])

# ------------------------------
# Interactive Dashboard Layout
# ------------------------------
st.subheader("Dashboard")

col1, col2 = st.columns(2)

# Left column: species chart
with col1:
    species_count = filtered_df["PredictedSpecies"].value_counts().reset_index()
    species_count.columns = ["Species", "Count"]
    fig_species = px.bar(
        species_count,
        x="Species",
        y="Count",
        color="Species",
        title="Number of Samples per Species"
    )
    st.plotly_chart(fig_species, use_container_width=True)

# Right column: gene annotation chart
with col2:
    gene_summary = pd.DataFrame({
        "Gene": ["GeneX Present", "GeneX Absent", "GeneY Present", "GeneY Absent"],
        "Count": [
            filtered_df["Annotation"].str.contains("GeneX: Present").sum(),
            filtered_df["Annotation"].str.contains("GeneX: Absent").sum(),
            filtered_df["Annotation"].str.contains("GeneY: Present").sum(),
            filtered_df["Annotation"].str.contains("GeneY: Absent").sum()
        ]
    })
    fig_genes = px.pie(
        gene_summary,
        names="Gene",
        values="Count",
        title="Gene Annotation Distribution"
    )
    st.plotly_chart(fig_genes, use_container_width=True)

# ------------------------------
# Images Section
# ------------------------------
st.subheader("System Architecture & Dashboard Preview")

col3, col4 = st.columns(2)

with col3:
    try:
        flowchart = Image.open("flowchart.png")
        st.image(flowchart, caption="System Architecture", use_container_width=True)
    except:
        st.warning("flowchart.png not found. Upload it to GitHub!")

with col4:
    try:
        dashboard_img = Image.open("dashboard.png")
        st.image(dashboard_img, caption="Dashboard Preview", use_container_width=True)
    except:
        st.warning("dashboard.png not found. Upload it to GitHub!")
