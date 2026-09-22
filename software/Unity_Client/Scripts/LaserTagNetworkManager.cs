using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;
using System.Text;
using System;

[Serializable]
public class JoinMessage
{
    public string type = "JOIN";
    public string player_name;
    public int marker_id;
    public string team;
}

[Serializable]
public class HitReportMessage
{
    public string type = "HIT_REPORT";
    public int target_marker_id;
    public double timestamp;
}

[Serializable]
public class ServerMessage
{
    public string type;
    public int amount;
    public string shooter_name;
    public bool is_fatal;
    public string target_name;
    public string player_id;
    public string message;
    public int respawn_timer_seconds;
}

public class LaserTagNetworkManager : MonoBehaviour
{
    private WebSocket websocket;
    private bool isConnected = false;

    [Header("Server Config")]
    public string serverUrl = "ws://192.168.1.100:8765";

    [Header("Player Config")]
    public string playerName = "Player1";
    public int myMarkerId = 0;
    public string myTeam = "TEAM_RED";

    [Header("References")]
    public LaserTagGun gunLogic;

    async void Start()
    {
        websocket = new WebSocket(serverUrl);

        websocket.OnOpen += () =>
        {
            Debug.Log("[NET] Connected to Server!");
            isConnected = true;
            SendJoinGame();
        };

        websocket.OnError += (e) =>
        {
            Debug.LogWarning("[NET] Error: " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("[NET] Connection closed.");
            isConnected = false;
        };

        websocket.OnMessage += (bytes) =>
        {
            string message = Encoding.UTF8.GetString(bytes);
            HandleServerMessage(message);
        };

        Debug.Log("[NET] Connecting to " + serverUrl + "...");
        await websocket.Connect();
    }

    void Update()
    {
        // Guard against null websocket (before Start completes)
        if (websocket != null)
        {
            #if !UNITY_WEBGL || UNITY_EDITOR
            websocket.DispatchMessageQueue();
            #endif
        }
    }

    public async void SendJoinGame()
    {
        if (!isConnected) return;

        JoinMessage msg = new JoinMessage
        {
            player_name = playerName,
            marker_id = myMarkerId,
            team = myTeam
        };
        string json = JsonUtility.ToJson(msg);
        await websocket.SendText(json);
        Debug.Log("[NET] Sent JOIN: " + json);
    }

    public async void ReportHit(int targetMarkerId)
    {
        if (!isConnected) return;

        HitReportMessage msg = new HitReportMessage
        {
            target_marker_id = targetMarkerId,
            timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()
        };
        string json = JsonUtility.ToJson(msg);
        await websocket.SendText(json);
    }

    private void HandleServerMessage(string json)
    {
        // Parse using the unified ServerMessage class
        ServerMessage msg;
        try
        {
            msg = JsonUtility.FromJson<ServerMessage>(json);
        }
        catch (Exception e)
        {
            Debug.LogWarning("[NET] Failed to parse: " + e.Message);
            return;
        }

        if (msg == null || string.IsNullOrEmpty(msg.type)) return;

        switch (msg.type)
        {
            case "DAMAGE_RECEIVED":
                Debug.Log($"[NET] Took {msg.amount} damage from {msg.shooter_name}!");
                if (gunLogic != null) gunLogic.TakeDamage(msg.amount, msg.is_fatal);
                break;

            case "HIT_CONFIRMED":
                Debug.Log("[NET] Hit confirmed on " + msg.target_name + "!");
                if (gunLogic != null) gunLogic.ShowHitmarker();
                break;

            case "DEATH_EVENT":
                Debug.Log("[NET] YOU DIED! Respawning in " + msg.respawn_timer_seconds + "s");
                if (gunLogic != null) gunLogic.Die(msg.respawn_timer_seconds);
                break;

            case "RESPAWN":
                Debug.Log("[NET] Respawned!");
                if (gunLogic != null) gunLogic.Respawn();
                break;

            case "JOIN_ACK":
                Debug.Log("[NET] Server says: " + msg.message);
                break;

            case "ERROR":
                Debug.LogError("[NET] Server error: " + msg.message);
                break;

            case "STATE_SYNC":
                // Periodic state update - can update scoreboard UI here
                break;
        }
    }

    private async void OnApplicationQuit()
    {
        if (websocket != null && isConnected)
        {
            await websocket.Close();
        }
    }
}
