import streamlit as st
import pydicom
import matplotlib.pyplot as plt
import numpy as np

def load_and_display_dcm_series(dcm_file_path):
    # Load DICOM file
    ds = pydicom.dcmread(dcm_file_path)
    
    # Extract and display each image in the series
    num_frames = ds.NumberOfFrames if hasattr(ds, 'NumberOfFrames') else 1
    
    col1, col2, col3, col4, col5 = st.columns(5)  # Divide into 5 columns
    
    for i in range(num_frames):
        with col1 if i % 5 == 0 else col2 if i % 5 == 1 else col3 if i % 5 == 2 else col4 if i % 5 == 3 else col5:
            pixel_array = ds.pixel_array[i]
            
            # Apply the 'bone' colormap manually
            cmap = plt.cm.bone
            normalized_image = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array))
            colored_image = cmap(normalized_image)
            
            st.image(colored_image, caption=f"DICOM Image {i+1}", use_column_width=True)
            
            # Add a separator between images
            if i < num_frames - 1:
                st.write("---")

def main():
    st.title("DICOM Image Viewer")
    
    # File upload
    uploaded_file = st.file_uploader("Upload a DICOM file", type=["dcm"])
    
    if uploaded_file is not None:
        # Display DICOM images when file is uploaded
        load_and_display_dcm_series(uploaded_file)
    
if __name__ == "__main__":
    main()
