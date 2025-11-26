import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import io

st.set_page_config(page_title="CVAT Track List (Ordered)", layout="wide")
st.title("CVAT Video XML → Ordered Label & Track ID List")

st.write("Upload a CVAT Video XML. Output is always ordered by your custom label priority list.")

# ------------------------------------------------------------------
# FIXED ORDER GIVEN BY USER
# ------------------------------------------------------------------
CUSTOM_ORDER = [
    "White Private",
    "Red Private",
    "Black Private",
    "Blue Private",
    "Yellow Private",
    "Silver Private",
    "Solar Panel",
    "Standalone Sofa",
    "Graffiti #1",
    "Graffiti #2",
    "Graffiti #3",
    "Graffiti #4",
    "Graffiti #5",
    "Graffiti #6",
    "Electric Gate",
    "Gold Private",
    "Lighting Pole (1 light)",
    "Lighting Pole (2 lights)",
    "Building 1",
    "Barricade",
    "Info Sign",
    "Unique Ground Texture",
    "Roof Hole",
    "Window",
    "Door",
    "Betonada 1",
    "Betonada 2",
    "White Pickup",
    "Oval SideWalk",
    "Lighting Pole (3 lights)",
]


# ------------------------------------------------------------------
# Extract tracks
# ------------------------------------------------------------------
def extract_track_list(xml_bytes):
    tree = ET.parse(io.BytesIO(xml_bytes))
    root = tree.getroot()

    entries = []
    for track in root.findall("track"):
        entries.append({
            "label": track.attrib.get("label", ""),
            "track_id": track.attrib.get("id", "")
        })

    df = pd.DataFrame(entries).drop_duplicates()

    # ------------------------------------------------------------------
    # Apply custom ordering
    # ------------------------------------------------------------------
    df["sort_key"] = df["label"].apply(
        lambda x: CUSTOM_ORDER.index(x) if x in CUSTOM_ORDER else 9999
    )

    df = df.sort_values(["sort_key", "label", "track_id"])
    df = df.drop(columns=["sort_key"])

    return df


# ------------------------------------------------------------------
# UI
# ------------------------------------------------------------------
uploaded = st.file_uploader("Upload CVAT Video XML", type=["xml"])

if uploaded:
    st.success("XML uploaded!")

    df = extract_track_list(uploaded.read())

    st.subheader("Ordered Track List")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="ordered_cvat_track_list.csv",
        mime="text/csv"
    )
