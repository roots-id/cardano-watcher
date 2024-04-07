# Cardano Watcher Design

## Ecosystem
The folloging diagram of a generic KERI/ACDC ecosystem shows the **Cardano Watcher** positioned between the secondary root of trust provided by witnesses and the Cardano blockchain and the verifiers:
![Ecosystem](Cardano_Watcher_Ecosystem.jpg)

# Flow of events
The following sequence diagrams show a simplified flow of events for three different cases:
1. an AID witnessed by a set of witnesses
2. an AID witnessed by a Cardano Backer
3. an AID witnessed by the Cardano Blockchain

### AID witnessed by a set of witnesses

```mermaid
sequenceDiagram
AID->>Witness A: Key Event
AID->>Witness B: Key Event
AID->>Witness C: Key Event
Watcher->>Witness A: get KEL receipts
Watcher->>Witness B: get KEL receipts
Watcher->>Witness C: get KEL receipts
loop HealthCheck
    Watcher->>Watcher: Validate KEL
Verifier->>Watcher: Request verification
Watcher->>Verifier: Verification result
end
```


## Feature set
