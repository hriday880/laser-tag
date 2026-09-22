using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class LaserTagGun : MonoBehaviour
{
    [Header("Dependencies")]
    public LaserTagNetworkManager networkManager;

    [Header("Stats")]
    public int maxAmmo = 10;
    private int currentAmmo;
    public int currentHP = 100;
    private bool isDead = false;

    [Header("UI Feedback")]
    public Image crosshair;
    public Image damageVignette;
    public Text ammoText;
    public Text hpText;
    public GameObject deathScreen;  // Optional: a full-screen "YOU DIED" overlay

    void Start()
    {
        currentAmmo = maxAmmo;
        UpdateHUD();
        if (damageVignette != null)
            damageVignette.color = new Color(1, 0, 0, 0);  // Transparent red
        if (deathScreen != null)
            deathScreen.SetActive(false);
    }

    /// <summary>
    /// Checks if the gun is able to fire (used by Vision system to skip CV if empty).
    /// </summary>
    public bool CanFire()
    {
        return !isDead && currentAmmo > 0;
    }

    /// <summary>
    /// Called by the ArUcoVision script when the volume button is pressed.
    /// </summary>
    public void FireWeapon(int? hitMarkerId)
    {
        if (!CanFire()) return;

        currentAmmo--;
        UpdateHUD();

        // Haptic recoil feedback
        #if UNITY_ANDROID || UNITY_IOS
        Handheld.Vibrate();
        #endif

        if (hitMarkerId.HasValue && hitMarkerId.Value >= 0)
        {
            Debug.Log("[GUN] Hit Target: " + hitMarkerId.Value);
            if (networkManager != null)
                networkManager.ReportHit(hitMarkerId.Value);
        }
        else
        {
            Debug.Log("[GUN] Shot missed.");
        }
    }

    public void OnReloadPressed()
    {
        if (!isDead)
        {
            currentAmmo = maxAmmo;
            UpdateHUD();
            Debug.Log("[GUN] Reloaded.");
        }
    }

    /// <summary>
    /// Called by NetworkManager when server says we got hit.
    /// </summary>
    public void TakeDamage(int amount, bool fatal)
    {
        if (isDead) return;  // Already dead, ignore further damage

        currentHP -= amount;
        if (currentHP < 0) currentHP = 0;

        UpdateHUD();
        if (damageVignette != null)
            StartCoroutine(FlashDamageScreen());

        if (fatal)
        {
            Die(10);  // Default respawn, server will override
        }
    }

    public void ShowHitmarker()
    {
        if (crosshair != null)
            StartCoroutine(FlashHitmarker());
    }

    /// <summary>
    /// Called when the player dies. Shows death screen and disables shooting.
    /// </summary>
    public void Die(int respawnSeconds)
    {
        isDead = true;
        currentHP = 0;
        UpdateHUD();
        Debug.Log("[GUN] YOU DIED! Respawning in " + respawnSeconds + "s");
        if (deathScreen != null)
            deathScreen.SetActive(true);
    }

    /// <summary>
    /// Called when the server respawns the player.
    /// </summary>
    public void Respawn()
    {
        isDead = false;
        currentHP = 100;
        currentAmmo = maxAmmo;
        UpdateHUD();
        Debug.Log("[GUN] Respawned!");
        if (deathScreen != null)
            deathScreen.SetActive(false);
    }

    private void UpdateHUD()
    {
        if (ammoText != null) ammoText.text = currentAmmo.ToString();
        if (hpText != null) hpText.text = currentHP.ToString();
    }

    private IEnumerator FlashDamageScreen()
    {
        damageVignette.color = new Color(1, 0, 0, 0.5f);
        yield return new WaitForSeconds(0.15f);
        float t = 0;
        while (t < 1f)
        {
            t += Time.deltaTime * 3f;  // Fade out over ~0.33 seconds
            damageVignette.color = Color.Lerp(new Color(1, 0, 0, 0.5f), new Color(1, 0, 0, 0), t);
            yield return null;
        }
        damageVignette.color = new Color(1, 0, 0, 0);  // Ensure fully transparent
    }

    private IEnumerator FlashHitmarker()
    {
        Color originalColor = crosshair.color;
        crosshair.color = Color.red;
        yield return new WaitForSeconds(0.15f);
        crosshair.color = originalColor;
    }
}
