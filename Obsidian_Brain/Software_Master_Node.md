# 💻 Software Architecture: Master Node

> [!info] 🧠 Core Philosophy
> The gun (phone) is "dumb" regarding game rules. It only reports what it sees. The **Server** is the source of truth for teams, health, and whether a hit is valid.

Welcome to the Software Engine of the ArUco Phone-as-Gun Laser Tag system. This node branches out into the four critical pillars of the software stack.

## 🏗 System Architecture Diagram

```mermaid
flowchart TD
    subgraph Client [Gun App (Player 1)]
        C[Camera Feed] --> CV[ArUco Detector]
        T[Physical Trigger] --> CV
        CV --> |On Trigger: Extracts Marker ID| N[WebSocket Client]
        N --> |Receives Damage/Kill| UI[HUD & Haptics]
    end

    subgraph Server [Local Game Server]
        W[WebSocket Router]
        GM[Game Manager]
        TM[Team & Player State]
        
        W --> |HitEvent(Shooter: P1, TargetMarker: 4)| GM
        GM --> TM
        TM --> |Validates Hit, Deducts HP| GM
        GM --> |DamageEvent| W
    end
    
    Client == "JSON over local WiFi" ==> Server
```

## 📚 Documentation Nodes

Navigate to the specific subsystems for deep-dive technical breakdowns:

- 🟩 **[[SW_Client_App]]** - The Mobile Application (UI, Hardware interfaces)
- 🟦 **[[SW_Computer_Vision]]** - The Optical Engine (ArUco Math, Crosshair intersections)
- 🟪 **[[SW_Server_Logic]]** - The Game Host (Matchmaking, Team balancing, State)
- 🟧 **[[SW_Network_Protocol]]** - The Communication Layer (JSON schemas, Sockets)

---
*Return to [[Home]]*
