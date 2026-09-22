import cv2
import numpy as np

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Use DICT_4X4_50 as per our architecture plan
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    # Use the new ArucoDetector API (OpenCV 4.7+) with fallback for older versions
    try:
        detector_params = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)
        use_new_api = True
    except AttributeError:
        detector_params = cv2.aruco.DetectorParameters_create()
        use_new_api = False

    print("--- ArUco Crosshair Test ---")
    print("Aim the center crosshair at an ArUco marker.")
    print("Press SPACE to simulate firing.")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip horizontally for selfie-view mirroring (makes testing intuitive)
        frame = cv2.flip(frame, 1)

        h, w = frame.shape[:2]
        crosshair = (int(w / 2), int(h / 2))

        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect markers (API version-dependent)
        if use_new_api:
            corners, ids, rejected = detector.detectMarkers(gray)
        else:
            corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=detector_params)

        hit_target = None

        if ids is not None and len(ids) > 0:
            # Draw all detected markers in green
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            for i, corner in enumerate(corners):
                marker_id = int(ids[i][0])
                # corner[0] is a (4, 2) array of the marker's corners
                # Must be float32 for pointPolygonTest
                marker_polygon = np.array(corner[0], dtype=np.float32)

                # Point in Polygon test
                # crosshair must be a tuple of floats
                is_inside = cv2.pointPolygonTest(
                    marker_polygon,
                    (float(crosshair[0]), float(crosshair[1])),
                    False
                )

                if is_inside >= 0:
                    hit_target = marker_id
                    # Highlight the targeted marker in RED
                    cv2.polylines(frame, [np.int32(marker_polygon)], True, (0, 0, 255), 3)
                    break  # Only report the first hit

        # Draw HUD (Crosshair)
        color = (0, 0, 255) if hit_target is not None else (0, 255, 0)
        thickness = 3 if hit_target is not None else 1

        # Draw reticle
        cv2.line(frame, (crosshair[0] - 20, crosshair[1]), (crosshair[0] + 20, crosshair[1]), color, thickness)
        cv2.line(frame, (crosshair[0], crosshair[1] - 20), (crosshair[0], crosshair[1] + 20), color, thickness)
        cv2.circle(frame, crosshair, 5, color, -1 if hit_target is not None else 1)

        # Status text
        if hit_target is not None:
            cv2.putText(frame, f"LOCKED ON: Marker {hit_target}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "SCANNING...", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("ArUco Crosshair Targeting", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):  # SPACE = simulate trigger pull
            if hit_target is not None:
                print(f"BANG! Hit Marker {hit_target}")
            else:
                print("BANG! Missed.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
