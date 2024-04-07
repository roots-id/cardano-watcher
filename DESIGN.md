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
actor controller
controller->>agent: Key Event
agent->>witness A: Key Event
agent->>witness B: Key Event
agent->>witness C: Key Event
watcher->>witness A: get KEL receipts
watcher->>witness B: get KEL receipts
watcher->>witness C: get KEL receipts
watcher->>watcher: Validate KELR
actor verifier
verifier->>watcher: Request verification
watcher->>verifier: Verification result
```
### AID witnessed by Cardano Backer
```mermaid
sequenceDiagram
actor controller
controller->>agent: Key Event
agent->>backer: Key Event
backer->>backer: Validate KEL
backer->>Cardano: write KEL as metadata
watcher->>Cardano: read KEL metadata
watcher->>watcher: Validate KEL
actor verifier
verifier->>watcher: Request verification
watcher->>verifier: Verification result
```
### AID witnessed by Cardano Blockchain
```mermaid
sequenceDiagram
actor controller
controller->>agent: Key Event
agent->>Cardano: write Key Event as metadata
watcher->>Cardano: read KEL metadata
watcher->>watcher: Validate KEL
actor verifier
verifier->>watcher: Request verification
watcher->>verifier: Verification result
```


## Feature set
