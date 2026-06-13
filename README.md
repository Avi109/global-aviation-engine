# 🌐 Global Core Aviation Engine

![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![UI](https://img.shields.io/badge/Interface-Vanilla_JS_%2B_CSS3-blue?style=flat-square)
![Architecture](https://img.shields.io/badge/Architecture-Dual_Portal-purple?style=flat-square)

> A high-performance, dark-mode aviation logistics terminal. Features a dual-portal architecture supporting a public passenger booking interface and a secure corporate administrative dashboard.

## 📋 Overview

The **Global Core Aviation Engine** is a full-stack web simulation of a modern flight booking and telemetry system. Designed with a sleek, low-latency UI, the system separates concerns between standard passenger operations (flight queries, boarding pass generation) and secure corporate operations (manifest tracking, operator authorization).

The frontend operates entirely on Vanilla JavaScript with Fetch API integrations, asynchronously communicating with a RESTful backend.

## ✨ Core Features

### ✈️ Passenger Terminal (Public Interface)
* **Real-Time Live Global Search:** Query active flights using standard 3-letter IATA codes (e.g., JFK, LHR, ICN).
* **Target Corridor Locking:** Click-to-select table rows that securely lock in flight variables for booking.
* **Encrypted Boarding Passes:** Dynamically generates stylized, receipt-like boarding passes upon successful transaction.
* **Session Authorization:** Stateful user logins with UI state morphing based on `logged_in` status.

### ⚠️ Corporate Manifest Terminal (Admin Interface)
* **Role-Based Access Control (RBAC):** Dedicated login route requiring `is_admin` backend flags.
* **Master Passenger Log:** View global database of all booked tickets, flight routes, and exact seat allocations.
* **Authorized Operator Registration:** System locked behind a master `admin_key` passphrase to prevent unauthorized corporate account creation.

### 🎨 UI/UX Highlights
* **Zero-Dependency Frontend:** No React, Vue, or Bootstrap. 100% custom CSS utilizing CSS Variables and CSS Grid.
* **Asynchronous Toast Notifications:** Custom-built sliding notification system for non-blocking user feedback.
* **Cyberpunk / Dark Theme:** Immersive `#0b0f19` and `#111827` color palettes with vibrant accent states (Primary Blue for passengers, Alert Red for admins).

## 🗺️ API Architecture (Frontend Consumptions)

The frontend expects a backend (Node.js, Flask, FastAPI, etc.) serving the following REST endpoints:

* `GET  /api/session` - Evaluates current user state (`logged_in`, `username`, `is_admin`).
* `POST /api/register` - Creates user/admin profiles (payload: `username`, `email`, `password`, `admin_key`).
* `POST /api/login` - Authenticates and establishes secure session.
* `POST /api/logout` - Terminates session.
* `GET  /api/flights?from={IATA}&to={IATA}&date={DATE}` - Fetches available flight array.
* `POST /api/bookings` - Submits final manifest order (payload: `flight_id`, `seat_number`).
* `GET  /api/my-tickets` - Retrieves current passenger's boarding passes.
* `GET  /api/admin/bookings` - (Admin Only) Retrieves master database of all bookings.

## 🚀 Local Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Avi109/global-aviation-engine.git](https://github.com/Avi109/global-aviation-engine.git)
cd global-aviation-engine
