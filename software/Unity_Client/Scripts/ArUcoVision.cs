using UnityEngine;
using UnityEngine.UI;
using OpenCVForUnity.CoreModule;
using OpenCVForUnity.ImgprocModule;
using OpenCVForUnity.ArucoModule;
using OpenCVForUnity.UnityUtils;
using System.Collections.Generic;

public class ArUcoVision : MonoBehaviour
{
    [Header("Dependencies")]
    public LaserTagGun gunLogic;
    public RawImage cameraDisplay;  // UI RawImage to show the camera feed as the game view

    private WebCamTexture webCamTexture;
    private Mat rgbaMat;
    private Mat grayMat;
    private Texture2D outputTexture;

    // Use fully qualified name to avoid collision with System.Collections.Generic.Dictionary
    private OpenCVForUnity.ArucoModule.Dictionary arucoDictionary;
    private DetectorParameters detectorParams;

    // Minimum marker area in pixels to count as "in range"
    // Prevents sniping a 5-pixel marker from across the arena
    [Header("Config")]
    public float minMarkerArea = 500f;

    void Start()
    {
        // 1. Find and start the rear-facing camera (not the selfie cam)
        string rearCamName = null;
        WebCamDevice[] devices = WebCamTexture.devices;
        for (int i = 0; i < devices.Length; i++)
        {
            if (!devices[i].isFrontFacing)
            {
                rearCamName = devices[i].name;
                break;
            }
        }

        if (rearCamName != null)
        {
            webCamTexture = new WebCamTexture(rearCamName, 1280, 720, 30);
        }
        else
        {
            // Fallback: use default camera (e.g., on a laptop for testing)
            Debug.LogWarning("[VISION] No rear camera found, using default.");
            webCamTexture = new WebCamTexture(1280, 720, 30);
        }

        webCamTexture.Play();

        // 2. Initialize OpenCV ArUco
        arucoDictionary = Aruco.getPredefinedDictionary(Aruco.DICT_4X4_50);
        detectorParams = DetectorParameters.create();

        Debug.Log("[VISION] System Online. Using rear camera: " + webCamTexture.deviceName);
    }

    void Update()
    {
        // Check volume button INDEPENDENTLY of camera frame updates
        // This prevents dropped shots when camera didn't deliver a new frame on that tick
        bool triggerPulled = Input.GetKeyDown(KeyCode.VolumeUp) || Input.GetKeyDown(KeyCode.VolumeDown);

        // Update the camera display every frame (so it looks like a live viewfinder)
        if (webCamTexture.isPlaying && webCamTexture.didUpdateThisFrame)
        {
            UpdateCameraDisplay();
        }

        // Only run the expensive CV math when the trigger is pulled
        if (triggerPulled)
        {
            if (webCamTexture.isPlaying)
            {
                ProcessShot();
            }
            else
            {
                // Camera not ready, still fire (miss)
                if (gunLogic != null) gunLogic.FireWeapon(null);
            }
        }
    }

    private void UpdateCameraDisplay()
    {
        // Show the live camera feed on the UI RawImage (the player's "scope" view)
        if (cameraDisplay != null)
        {
            cameraDisplay.texture = webCamTexture;
        }
    }

    private void ProcessShot()
    {
        if (gunLogic != null && !gunLogic.CanFire())
        {
            // Still call FireWeapon so it can play the "empty clip" sound
            gunLogic.FireWeapon(null);
            return;
        }

        // 1. Initialize Mats if needed
        if (rgbaMat == null || rgbaMat.width() != webCamTexture.width())
        {
            rgbaMat = new Mat(webCamTexture.height, webCamTexture.width, CvType.CV_8UC4);
            grayMat = new Mat(webCamTexture.height, webCamTexture.width, CvType.CV_8UC1);
        }

        // 2. Copy camera frame to OpenCV Mat
        Utils.webCamTextureToMat(webCamTexture, rgbaMat);
        Imgproc.cvtColor(rgbaMat, grayMat, Imgproc.COLOR_RGBA2GRAY);

        // 3. Detect Markers
        List<Mat> corners = new List<Mat>();
        Mat ids = new Mat();
        List<Mat> rejected = new List<Mat>();
        Aruco.detectMarkers(grayMat, arucoDictionary, corners, ids, detectorParams, rejected);

        int? hitMarkerId = null;

        if (ids.total() > 0)
        {
            // 4. Crosshair = dead center of the camera frame
            Point crosshair = new Point(rgbaMat.width() / 2.0, rgbaMat.height() / 2.0);

            int[] idsArray = new int[(int)ids.total()];
            ids.get(0, 0, idsArray);

            for (int i = 0; i < corners.Count; i++)
            {
                // Get the 4 corners of the detected marker
                float[] cornerData = new float[8];
                corners[i].get(0, 0, cornerData);

                // Build polygon from the 4 corner points
                MatOfPoint2f polygon = new MatOfPoint2f(
                    new Point(cornerData[0], cornerData[1]),
                    new Point(cornerData[2], cornerData[3]),
                    new Point(cornerData[4], cornerData[5]),
                    new Point(cornerData[6], cornerData[7])
                );

                // Range check: calculate the area of the marker polygon
                double area = Imgproc.contourArea(polygon);
                if (area < minMarkerArea)
                {
                    polygon.Dispose();
                    continue;  // Target is too far away, skip
                }

                // 5. Point-In-Polygon test
                double isInside = Imgproc.pointPolygonTest(polygon, crosshair, false);
                polygon.Dispose();

                if (isInside >= 0)
                {
                    hitMarkerId = idsArray[i];
                    break;  // First hit wins
                }
            }
        }

        // Cleanup
        ids.Dispose();
        foreach (Mat c in corners) c.Dispose();
        foreach (Mat r in rejected) r.Dispose();

        // 6. Tell the gun logic we fired
        if (gunLogic != null)
        {
            gunLogic.FireWeapon(hitMarkerId);
        }
    }

    void OnDestroy()
    {
        if (webCamTexture != null) webCamTexture.Stop();
        if (rgbaMat != null) rgbaMat.Dispose();
        if (grayMat != null) grayMat.Dispose();
    }
}
