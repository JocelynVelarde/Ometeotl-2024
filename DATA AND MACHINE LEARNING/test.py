import rasterio
import pandas as pd
import numpy as np

# Replace 'path_to_your_geotiff.tif' with the actual path to your GeoTIFF file
file_path = 'DATA AND MACHINE LEARNING\MOD11A1.061_Clear_day_cov_doy2023278_aid0001.tif'

# Open the GeoTIFF file
with rasterio.open(file_path) as src:
    # Read the data from the first band
    data = src.read(1)  # Assuming single-band data
    # Get the affine transformation of the dataset
    transform = src.transform

    # Get the dimensions of the data
    rows, cols = data.shape

    # Create arrays of row and column indices
    row_indices = np.arange(rows)
    col_indices = np.arange(cols)

    # Create a meshgrid of indices
    col_indices_mesh, row_indices_mesh = np.meshgrid(col_indices, row_indices)

    # Flatten the arrays for vectorized computations
    data_flat = data.flatten()
    row_indices_flat = row_indices_mesh.flatten()
    col_indices_flat = col_indices_mesh.flatten()

    # Convert pixel indices to geographic coordinates
    xs, ys = rasterio.transform.xy(transform, row_indices_flat, col_indices_flat)
    xs = np.array(xs)
    ys = np.array(ys)

    # Create a DataFrame with the coordinates and data values
    df = pd.DataFrame({
        'longitude': xs,
        'latitude': ys,
        'value': data_flat 
    })

    df2 = df[df['value'] > 0]
# Display the first few rows of the DataFrame
print(df.head())
print(df2)