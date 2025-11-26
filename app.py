import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import io

st.set_page_config(page_title="CVAT Track List", layout="wide")
st.title("CVAT Video XML → Label & Track ID List")

st.write("Upload a CVAT **video** XML and get a unique list of labels + track IDs.")

# -----------------------------------------------------
# Parse XML and extract tracks
# -----------------------------------------------------
def extract_track_list(xml_bytes):
    tree = ET.parse(io.BytesIO(xml_bytes))
    root = tree.getroot()

    label_ids = []

    for track in root.findall("track"):
        label = track.attrib.get("label", "")
        track_id = track.attrib.get("id", "")
        label_ids.append((label, track_id))

    # Remove duplicates (just in case)
    unique_list = list({(l, t) for l, t in label_ids})

    df = pd.DataFrame(unique_list, columns=["label", "track_id"])
    df = df.sort_values(by=["label", "track_id"])
    return df


# -----------------------------------------------------
# UI
# -----------------------------------------------------
uploaded = st.file_uploader("Upload CVAT Video XML", type=["xml"])

if uploaded:
    st.success("XML uploaded successfully!")

    df = extract_track_list(uploaded.read())

    st.subheader("Track List")
    st.dataframe(df)

    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="cvat_track_list.csv",
        mime="text/csv"
    )
