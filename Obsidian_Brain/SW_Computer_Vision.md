# 🟦 Computer Vision Engine

> [!info] The Math Behind the Magic
> We don't just need to know if a marker is on screen. We need to know if the **crosshair** is physically aiming at it.

## 1. ArUco Dictionary Selection
We will use the **`DICT_4X4_50`** ArUco dictionary. 
- **Why 4x4?** 4x4 grids have larger internal black/white blocks than 5x5 or 6x6. Larger blocks are vastly easier for a phone camera to resolve from 10 meters away in low light.
- **Why 50?** We only need 8-12 markers. 50 is the smallest pre-built dictionary, making lookups slightly faster.

## 2. Detection Pipeline

When the trigger is pulled, we pass the current frame to OpenCV:

```python
# OpenCV Python example
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# corners is a list of [top-left, top-right, bottom-right, bottom-left] for each marker
corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
```

## 3. The "Hit" Math (Point in Polygon)
Once we have the 4 corners of a detected marker, we need to know if the center of the phone screen (the crosshair) falls inside that box.

Let $C = (C_x, C_y)$ be the center pixel of the screen.
Let $M$ be the polygon formed by the 4 corners of the ArUco marker: $[P_1, P_2, P_3, P_4]$.

We use a standard **Ray-Casting Algorithm** or OpenCV's `pointPolygonTest`:

```python
crosshair = (screen_width / 2, screen_height / 2)

for i in range(len(ids)):
    marker_corners = corners[i][0] # Get the 4 points
    
    # Check if crosshair is inside this specific marker's bounds
    # returnVal > 0 means inside, < 0 means outside, == 0 means on the edge
    is_inside = cv2.pointPolygonTest(marker_corners, crosshair, False)
    
    if is_inside >= 0:
        return ids[i][0] # BOOM! We are aiming directly at this marker!
        
return None # Shot missed
```

## 4. Range Limits (Anti-Sniper)
To prevent people from shooting targets 50 meters away (which ruins the fun), we calculate the Area of the polygon. If the area (in pixels) is smaller than a threshold, the target is "Out of Range" and the hit is discarded.

---
*Parent: [[Software_Master_Node]]*
