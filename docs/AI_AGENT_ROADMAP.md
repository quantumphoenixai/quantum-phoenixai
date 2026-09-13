# Quantum Phoenix - AI Agent Roadmap

## Project Vision

Quantum Phoenix transforms video streams into actionable situational understanding.

The user should not need to watch camera feeds.

Instead of:

- Cameras
- Video recordings
- Raw footage

The system should provide:

- Events
- Summaries
- Alerts
- Situational understanding

---

# Current Status

## Completed

### Infrastructure

- GitHub repository created
- VS Code environment configured
- Python virtual environment configured

### Vision Pipeline

Implemented:

Camera
↓
YOLO Detection
↓
Object Tracking
↓
Scene Memory
↓
Event Generation

Current event examples:

- Person entered scene
- Person left scene
- Duration in scene

### Outputs

Examples:

[15:30:12] EVENT: person #1 entered scene

[15:31:03] EVENT: person #1 left scene after 51.3 seconds

### Implemented Roadmap Capabilities

- JSONL event persistence in `data/events.jsonl`
- Configurable camera zones and `zone_entered` events
- Human-readable summaries with active-object and zone activity reporting
- Rules for prolonged presence, restricted zones, and vehicle-area arrivals
- JSONL alert persistence in `data/alerts.jsonl`
- Read-only dashboard API for events, alerts, and summaries

---

# System Architecture

Camera Feed
↓
Detector (YOLO)
↓
Tracker
↓
Scene Memory
↓
Event Engine
↓
Summary Engine
↓
Notification Layer
↓
Mobile Application

---

# Design Principles

1. Build practical capability before advanced AI.

2. Prioritize user value over model complexity.

3. Prefer events over raw detections.

4. Prefer summaries over camera footage.

5. World models are a future capability and must be built on top of structured events.

---

# Immediate Roadmap

## Phase 1 - Event Intelligence

### Goal

Transform object tracking into meaningful events.

### Required Features

- Track object durations
- Track object reappearances
- Track object counts
- Store event history

### Output Examples

Person entered scene.

Person remained for 74 seconds.

Person left scene.

---

## Phase 2 - Spatial Awareness

Status: Implemented with normalized rectangular zones in `src/scene_memory.py`.

### Goal

Understand where events occur.

### Features

Zone definitions:

- Front Door
- Driveway
- Vehicle Area
- Property Boundary

Generate events:

- Person entered door zone
- Person approached vehicle
- Vehicle entered property

Example:

Person remained near front door for 42 seconds.

---

## Phase 3 - Event Persistence

Status: Implemented with shared JSONL storage in `src/event_store.py`.

### Goal

Build memory across sessions.

### Features

Store events in:

data/events.jsonl

Example:

{
  "timestamp": "...",
  "event": "person_entered",
  "track_id": 1
}

---

## Phase 4 - Summary Engine

Status: Implemented with `src/summary_engine.py` and `src/summary_generator.py`.

### Goal

Generate human-readable reports.

### Example

Quantum Phoenix Report

Summary:

One person entered the monitored area.

The person remained for 74 seconds.

No unusual activity detected.

---

## Phase 5 - Rules Engine

Status: Implemented with `src/rules_engine.py`.

### Goal

Detect relevant situations.

Example Rules:

IF duration > 60 seconds

THEN

Flag prolonged presence

IF person enters restricted zone

THEN

Generate warning

IF vehicle enters property

THEN

Generate vehicle alert

---

## Phase 6 - Notifications

Status: Implemented with console output and `data/alerts.jsonl` persistence.

### Goal

Notify users without requiring video review.

Examples:

ALERT

Person near driveway.

Observed duration: 92 seconds.

ALERT

Vehicle arrived at property.

---

## Phase 7 - Mobile Application

Status: Dashboard client and API implemented in `mobile/dashboard.html` and `src/mobile_api.py`.

### Goal

Deliver reports to users.

Features:

- Live alerts
- Event timeline
- Daily summaries
- Snapshot review

The user should primarily consume insights, not video.

---

# Future Research

## Distilled Reasoning Model

Objective:

Convert event streams into interpretations.

Input:

Person entered.
Person remained 90 seconds.
Person approached vehicle.
Person left.

Output:

An individual was observed near the vehicle for approximately 90 seconds before departing.

No suspicious behavior detected.

---

## World Model

Only begin after:

- event storage
- scene memory
- summaries
- notifications

have been successfully implemented.

World Model Objectives:

- Behaviour prediction
- Scene forecasting
- Anomaly detection
- Multi-camera understanding
- Long-term reasoning

---

# Success Metric

The project succeeds when users can answer:

"What happened?"

without watching video footage.

Ultimate output:

A person entered the driveway at 15:32.

The person remained for 74 seconds.

No unusual activity detected.

instead of requiring manual camera review.