# Mobile Robot and Drone Intruder Detection System

This project demonstrates a tele-operated robotic system using CoppeliaSim and PyQt5 for real-time monitoring, navigation, and intruder detection.

---

## 📌 Project Overview

The system simulates a **surveillance robot** that detects intruders (e.g., horse, human, or objects) in an environment.

* A mobile robot captures camera data
* A drone performs aerial patrol
* A GUI displays real-time information
* Intruder detection is based on image processing

When an intruder and fallen objects are detected, the system updates:
👉 **"Intruder detected"**
Otherwise:
👉 **"No intruder detected"**

---

## ⚙️ System Components

### 🤖 Mobile Robot

* Captures live camera feed
* Performs object detection
* Navigates based on user commands

### 🚁 Drone System

* Patrols using predefined waypoints
* Provides aerial monitoring view

### 🖥️ Graphical User Interface (PyQt5)

* Displays:

  * Live camera feed
  * Aerial map view
  * Robot coordinates (X, Y, Z)
* Controls:

  * Simulation start/stop
  * Camera rotation
  * Robot movement
  * Drone patrol

---

## 🧠 System Workflow

1. Start simulation
2. Activate live camera
3. Capture image from robot vision sensor
4. Convert image to HSV
5. Apply brown color mask
6. Detect contours (intruder objects)
7. Update system status:

   * Intruder detected
   * No intruder detected

---

## 🤖 Key Features

* 🎥 Real-time camera streaming
* 🧠 Intruder detection using image processing
* 🎯 Color-based masking (brown detection)
* 🗺️ Interactive map with waypoint selection
* 🚁 Drone patrol system
* 📍 Live coordinate tracking (X, Y, Z)
* 🎮 Tele-operation interface

---

## 🧠 Technical Concepts

* Computer vision (OpenCV)
* HSV color space filtering
* Contour detection
* Remote API communication (CoppeliaSim ZMQ)
* Event-driven GUI (PyQt5)
* Robot navigation control

---

## ▶️ How to Run

1. Open CoppeliaSim
2. Load the simulation scene
3. Run Python script:

```bash
python src/main.py
```

4. Use GUI to:

* Start simulation
* Enable live camera
* Control robot and drone

---

## ⚠️ Limitations

* Robot cannot move autonomously
* Manual positioning required
* Detection depends on camera visibility
* Possible false positives

---

## 🚀 Future Improvements

* Add autonomous navigation
* Improve object detection using AI models
* Enhance detection accuracy
* Integrate real-time tracking

---

## 📊 Learning Outcomes

* Mobile robot system design
* Human-robot interaction
* Computer vision integration
* Simulation using CoppeliaSim
* GUI-based robot control

---
