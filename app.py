import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import io

st.set_page_config(page_title="CVAT Ordered Label List", layout="wide")
st.title("CVAT Video XML → Fixed Ordered Label List")

st.write("Always outputs the full ordered label list, with blank track_id where missing.")

# ------------------------------------------------------------------
# FIXED ORDER GIVEN BY USER (ALWAYS INCLUDED)
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
# Parse CVAT XML and map track_ids to labels
# ------------------------------------------------------------------
def extract_track_ids(xml_bytes):
    tree = ET.parse(io.BytesIO(xml_bytes))
    root = tree.getroot()

    # Map label → first track_id (or keep empty)
    label_to_id = {label: "" for label in CUSTOM_ORDER}

    for track in root.findall("track"):
        label = track.attrib.get("label", "")
        track_id = track.attrib.get("id", "")

        # Only keep if the label is in the fixed list
        if label in label_to_id:
            # If first time seen, store the ID
            if label_to_id[label] == "":
                label_to_id[label] = track_id

    # Build dataframe in exact custom order
    df = pd.DataFrame({
        "label": CUSTOM_ORDER,
        "track_id": [label_to_id[label] for label in CUSTOM_ORDER]
    })

    return df


# ------------------------------------------------------------------
# UI
# ------------------------------------------------------------------
uploaded = st.file_uploader("Upload CVAT Video XML", type=["xml"])

if uploaded:
    st.success("XML uploaded!")

    df = extract_track_ids(uploaded.read())

    st.subheader("Ordered Label List (fixed length)")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="ordered_label_list.csv",
        mime="text/csv"
    )
