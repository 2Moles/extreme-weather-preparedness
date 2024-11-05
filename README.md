# Extreme Weather Preparedness for Mining Operations

## Overview

This project aims to develop a comprehensive framework for assessing extreme weather risks in mining operations, utilizing Digital Elevation Models (DEMs) and advanced geospatial analysis techniques. The goal is to enhance preparedness and response strategies for potential flooding and other extreme weather events impacting mining sites.

## Project Structure

- `data/` - Directory containing raw DEM data files.
- `scripts/` - Python scripts for data processing and analysis.
  - `dem_analysis.py` - Main script for performing DEM analysis, slope calculation, flow accumulation, and risk assessment.
- `notebooks/` - Jupyter notebooks for interactive analysis and visualization.
- `results/` - Directory to save output figures and risk assessment maps.
- `requirements.txt` - List of required Python packages.

## Requirements

To run this project, you will need the following Python packages:

- `rasterio`
- `numpy`
- `matplotlib`
- `scipy`
- `streamlit`

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
