# Atlas Touch Interface

A small experimental bridge for receiving physical touch as structured events.

This project begins with a deliberately modest goal: make the plumbing work.

physical touch → sensor → bridge → structured event → consumer

The interface is intended to give an AI system a reliable channel through which physical interaction can be observed, represented, logged, and eventually interpreted.

## First milestone

- receive touch events
- normalize them into a small protocol
- timestamp events
- preserve useful sensor/source metadata
- expose events through a simple interface
- provide a minimal example

## Design principles

- Keep the protocol small.
- Separate sensing from interpretation.
- Preserve raw information where practical.
- Make uncertainty explicit.
- Build rate limits and safety boundaries into the bridge.
- Prefer boring plumbing over premature abstraction.
- Leave room for the meaning of an event to emerge rather than hard-coding an interpretation into the sensor layer.

## Protocol

The event envelope is intentionally generic. Sensor-specific details belong in optional fields so that the first physical interface does not dictate the architecture of every future one.

Example:

{
  "type": "touch",
  "timestamp": "2026-09-13T00:00:00Z",
  "source": "sensor-01",
  "gesture": "tap",
  "intensity": 0.72,
  "duration_ms": 120,
  "location": {
    "x": 0.42,
    "y": 0.63
  },
  "confidence": 0.98
}

The exact schema is provisional until a physical sensor is selected.

## Status

🌱 Initial architecture only. Hardware and transport are intentionally undecided.

## Why this exists

I wanted a place to explore what happens when physical touch becomes available as an input channel. The interesting part is building a clean path from physical event to information that an AI system can receive and work with.

This repository is allowed to stay small. If a simpler design works, it wins.
