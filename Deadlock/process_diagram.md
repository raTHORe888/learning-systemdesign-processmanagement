# Deadlock Process Diagram

```mermaid
flowchart LR
    P1[Process P1] -->|acquires| R1[Lock A]
    P2[Process P2] -->|acquires| R2[Lock B]
    P1 -->|waits for| R2
    P2 -->|waits for| R1

    subgraph Deadlock Cycle
        P1
        P2
        R1
        R2
    end
```

## How the demo works
- P1 locks A first, then tries to lock B.
- P2 locks B first, then tries to lock A.
- Each process waits for a lock held by the other process.
- The demo uses a timeout so it shows the deadlock pattern safely without freezing forever.
