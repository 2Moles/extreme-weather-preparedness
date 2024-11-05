import streamlit as st
import requests
import pandas as pd
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude
import plotly.graph_objects as go

# Streamlit container for map display
container = st.container()

# Sidebar inputs
with st.sidebar:
    south_input = st.text_input('South Bound', '22.0')
    north_input = st.text_input('North Bound', '22.5')
    west_input = st.text_input('West Bound', '85.4')
    east_input = st.text_input('East Bound', '85.8')
    
    # Dropdown for selecting DEM type
    dem_type = st.selectbox(
        'DEM Type', 
        ['SRTMGL3', 'SRTMGL1', 'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 
         'COP30', 'COP90', 'EU_DTM', 'GEDI_L3', 'GEBCOIceTopo', 'GEBCOSubIceTopo'], 
        index=0
    )
    
    if st.button('Show Bounds'):
        try:
            north = float(north_input)
            south = float(south_input)
            east = float(east_input)
            west = float(west_input)
            
            # Create bounds DataFrame
            xbounds = [south, south, north, north]
            ybounds = [east, west, east, west]
            df = pd.DataFrame(data={'lat': xbounds, 'lon': ybounds})
            
            # Show map with bounds
            container.map(df)
        except ValueError:
            st.error("Please enter valid numerical coordinates.")
    
    if st.button('Download DEM'):
        # Build the URL with the dem_type parameter
        url = f'https://portal.opentopography.org/API/globaldem?demtype={dem_type}&south='+south_input+'&north='+north_input+'&west='+west_input+'&east='+east_input+'&outputFormat=GTiff&API_Key=demoapikeyot2022'
        
        # Display the generated URL for verification
        st.write(f"Generated URL: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            with open('noamundi_dem.tif', 'wb') as f:
                f.write(response.content)
            st.write('DEM Downloaded Successfully')
        except requests.exceptions.RequestException as e:
            st.error(f"Download failed: {e}")

# Function to visualize DEM
def display_dem(dem_path):
    with rasterio.open(dem_path) as dem:
        dem_data = dem.read(1)
        fig, ax = plt.subplots(figsize=(8, 6))
        cax = ax.imshow(dem_data, cmap="terrain")
        fig.colorbar(cax, ax=ax, orientation='vertical', label='Elevation (m)')
        ax.set_title("DEM Data for Selected Area")
        st.pyplot(fig)

# Slope Calculation using Gradient Magnitude
def calculate_slope(dem_path):
    with rasterio.open(dem_path) as dem:
        dem_data = dem.read(1)
        # Gaussian gradient magnitude to approximate slope
        slope = gaussian_gradient_magnitude(dem_data, sigma=1)
        return slope

def display_slope(slope_data):
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.imshow(slope_data, cmap="viridis")
    fig.colorbar(cax, ax=ax, orientation='vertical', label='Slope (%)')
    ax.set_title("Slope Analysis for Selected Area")
    st.pyplot(fig)

# Flow Accumulation (simplified as local high gradient areas)
def calculate_flow_accumulation(slope_data):
    # Thresholding high-gradient areas for flow accumulation
    flow_accumulation = np.where(slope_data > np.percentile(slope_data, 80), 1, 0)
    return flow_accumulation

def display_flow(flow_data):
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.imshow(flow_data, cmap="Blues")
    fig.colorbar(cax, ax=ax, orientation='vertical', label='Flow Accumulation')
    ax.set_title("Flood Risk Map for Selected Area")
    st.pyplot(fig)

# Risk Classification based on slope and flow accumulation
def calculate_risk(slope_data, flow_data):
    # Combining slope and flow for risk assessment
    risk_map = slope_data * 0.5 + flow_data * 0.5
    return risk_map

def display_risk(risk_data):
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.imshow(risk_data, cmap="hot")
    fig.colorbar(cax, ax=ax, orientation='vertical', label='Risk Level')
    ax.set_title("Risk Classification Map for Selected Area")
    st.pyplot(fig)

# 3D Plot of DEM Data using Plotly
def display_3d_dem(dem_path):
    with rasterio.open(dem_path) as dem:
        dem_data = dem.read(1)
        x, y = np.meshgrid(range(dem_data.shape[1]), range(dem_data.shape[0]))

        fig = go.Figure(data=[go.Surface(z=dem_data, x=x, y=y, colorscale='earth')])
        fig.update_layout(
            title="3D DEM Visualization",
            scene=dict(
                xaxis_title='X Coordinates',
                yaxis_title='Y Coordinates',
                zaxis_title='Elevation (m)'
            ),
            margin=dict(l=0, r=0, t=50, b=0)
        )
        st.plotly_chart(fig)

# Add this call within your Streamlit app's main code block
dem_path = "noamundi_dem.tif"
if os.path.exists(dem_path):
    display_3d_dem(dem_path)
    display_dem(dem_path)
    slope_data = calculate_slope(dem_path)
    display_slope(slope_data)
    flow_data = calculate_flow_accumulation(slope_data)
    display_flow(flow_data)
    risk_data = calculate_risk(slope_data, flow_data)
    display_risk(risk_data)
else:
    st.error("DEM file not found.")
