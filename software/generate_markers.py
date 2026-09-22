import cv2
import os

output_dir = "/Users/admin/Documents/Laser Tag/Markers_To_Print"
os.makedirs(output_dir, exist_ok=True)

# We are using the ORIGINAL dictionary for compatibility with js-aruco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

for i in range(8):
    # Generate a 1000x1000 pixel marker (high resolution for crisp printing)
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, i, 1000)
    
    # Add a thick white border (crucial for OpenCV to recognize the black edges)
    bordered_marker = cv2.copyMakeBorder(marker_image, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    
    filepath = os.path.join(output_dir, f"Player_Marker_ID_{i}.png")
    cv2.imwrite(filepath, bordered_marker)
    print(f"Created: {filepath}")

print("\nSuccess! Markers are ready for printing.")
