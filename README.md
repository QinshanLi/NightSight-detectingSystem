# AIoT Low-Light Risk Event Stream System

## 📌 Project Overview
This project transforms publicly available low-light driving video datasets into a system-level continuous event stream for AIoT validation.

Unlike traditional single-test datasets (e.g., ExDark, DarkFace), this project constructs a structured and continuous low-light traffic risk scenario stream under driver first-person perspective.

## 🚗 Key Features
- Driver first-person low-light video scenario reconstruction
- Risk-based event classification and labeling
- Continuous event stream generation from segmented clips
- AIoT system-level validation (not only model accuracy testing)
- Multi-risk scenarios:
  - Vehicle-pedestrian co-occurrence risk
  - Weak-light small object detection risk
  - Strong glare interference risk
  - Blind spot approach risk
  - Dangerous area intrusion risk

## 🧠 System Pipeline
1. Raw low-light driving video collection
2. Risk-based segmentation
3. Scene classification and labeling
4. Programmatic recombination
5. Continuous event stream generation
6. AIoT system testing (enhancement + detection + alerting + logging)

## 🎯 Goal
Bridge the gap between algorithm-level evaluation and real-world AIoT system deployment in low-light traffic safety scenarios.

## 📂 Dataset Status
Dataset:
https://www.kaggle.com/datasets/evelynmimi/nightsightsystem-eventstream
