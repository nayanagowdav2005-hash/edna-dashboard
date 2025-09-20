import streamlit as st
import pandas as pd
import time
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="eDNA Biodiversity Explorer", layout="wide")
st.title("🌱 AI-powered eDNA Taxonomy & Biodiversity Dashboard")

# -------------------
# Section 0: Show Images (Professional visuals)
# -------------------
st.subheader("Project Overview Images")
st.image("flowchart.png", caption="System Architecture", use_container_width=True)
st.image("dashboard.png", caption="Dashboard Mockup", use_container_width=True)
st.image("ai_internals.png", caption="AI Pipeline Internals", use_container_width=True)
st.image("storyboard.png", caption="Researcher Journey Storyboard", use_container_width=True)
st.image("infographic.png", caption="Project Summary Infographic", use_container_width=True)

st.markdown("---")  # horizontal line

# -------------------
# Step 1: Upload File
# -------------------
uploaded_file = st.file_uploader("Upload eDNA file (CSV/FASTQ)", type=["csv", "fastq"])
if uploaded_file:
    st.success("File uploaded successfully!")

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Show uploaded data
    st.subheader("Uploaded Data Sample")
    st.dataframe(df.head())

    # Show Predicted Species + Annotation
    if "PredictedSpecies" in df.columns and "Annotation" in df.columns:
        st.subheader("Predicted Species & Annotation")
        st.dataframe(df[["SampleID", "PredictedSpecies", "Annotation"]])

    # -------------------
    # Step 2: Simulate Pipeline
    # -------------------
    st.subheader("Processing Pipeline")
    steps = ["Preprocessing Reads", "Encoding Features", "Clustering Taxa",
             "Mapping Taxonomy", "Estimating Abundance"]

    progress = st.progress(0)
    status_text = st.empty()
    for i, step in enumerate(steps):
        status_text.text(f"{step} ...")
        time.sleep(1)  # simulate processing time
        progress.progress((i+1)/len(steps))
    st.success("Processing Complete ✅")

    # -------------------
    # Step 3: Display Dashboard
    # -------------------
    st.subheader("Results Dashboard")

    # KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Samples Processed", len(df))
    kpi2.metric("Taxa Identified", df["PredictedSpecies"].nunique())
    kpi3.metric("Novel Taxa %", "8.5%")
    kpi4.metric("Avg Turnaround", "4.2 hrs")

    # Abundance Bar Chart with Annotations
    if "PredictedSpecies" in df.columns and "Annotation" in df.columns:
        data_bar = df.groupby("PredictedSpecies").size().reset_index(name="Count")
        data_bar = data_bar.merge(df[["PredictedSpecies", "Annotation"]].drop_duplicates(),
                                  on="PredictedSpecies")
        fig_bar = px.bar(data_bar, x="PredictedSpecies", y="Count", text="Annotation",
                         title="Predicted Species Abundance with Annotation")
        st.plotly_chart(fig_bar, use_container_width=True)

        # Pie chart with Annotations
        fig_pie = px.pie(data_bar, values="Count", names="PredictedSpecies",
                         hover_data=["Annotation"], title="Predicted Species Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Taxonomy Sunburst (mocked)
    data_sunburst = pd.DataFrame({
        "Kingdom": ["Animalia", "Animalia", "Animalia", "Fungi"],
        "Phylum": ["Chordata", "Arthropoda", "Mollusca", "Ascomycota"],
        "Count": [120, 90, 45, 60]
    })
    fig_sunburst = px.sunburst(data_sunburst, path=["Kingdom", "Phylum"], values="Count",
                               title="Taxonomic Distribution")
    st.plotly_chart(fig_sunburst, use_container_width=True)

    # Sample Locations Map (mocked)
    st.subheader("Sample Locations")
    map_data = pd.DataFrame({
        "lat": [12.9716, 13.0827, 15.2993],
        "lon": [77.5946, 80.2707, 74.1240],
        "Sample": ["SMP_01", "SMP_02", "SMP_03"]
    })
    st.map(map_data)

    # -------------------
    # Step 4: Export Results
    # -------------------
    st.download_button("Download Results (CSV)", df.to_csv(index=False),
                       file_name="results.csv")

# -------------------
# Footer / Closing Impact
# -------------------
st.markdown("---")

