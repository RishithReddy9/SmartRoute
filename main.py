import streamlit as st
from utils.geocode import geocode_addresses
from utils.distance_matrix import build_distance_matrix
from planner.route_optimizer import optimize_routes
from utils.visualizer import display_routes
import pandas as pd

st.set_page_config(page_title="Logistics Route Planner", layout="wide")
st.title("\U0001F69A Smart Logistics Route Planner")

uploaded_file = st.file_uploader("Upload CSV with Addresses", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, quotechar='"')
    st.subheader("Uploaded Data")
    st.dataframe(df)

    if st.button("Plan Routes"):
        try:
            with st.spinner("Geocoding addresses and building distance matrix..."):
                locations, latlngs, failed = geocode_addresses(df)

                if failed:
                    st.warning("The following addresses could not be geocoded:")
                    for addr in failed:
                        st.error(f"❌ {addr}")
                    st.stop()

                distance_matrix = build_distance_matrix(latlngs)

            with st.spinner("Optimizing routes with OR-Tools..."):
                routes, total_distance = optimize_routes(distance_matrix, df['PackageWeight'].tolist())

            st.success(f"Optimization Complete! Total Distance: {total_distance} km")

            with st.spinner("Generating map..."):
                map_html = display_routes(routes, latlngs, locations)
                st.components.v1.html(map_html, height=600, scrolling=True)

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            import traceback
            st.text(traceback.format_exc())

