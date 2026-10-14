# FarmFlow
# Smart Farmer Procurement Platform

---

## 1. Problem Statement

> *"Farmers often face long waiting times, lack of information regarding procurement schedules, and uncertainty about procurement status."*

### Proposed Solution
A comprehensive digital platform that enables farmer registration and slot booking, provides real-time queue management, sends automated notifications, tracks procurement and payment status, and significantly reduces physical congestion and waiting times at designated procurement centres.

---

## 2. Understanding Procurement & The Core Problem

Agricultural procurement is the process by which government agencies (such as the FCI, state civil supplies corporations, and local mandis) purchase crops directly from farmers, usually at the Minimum Support Price (MSP). 

### Current Friction Points:
* **Blind Arrival:** Farmers travel to procurement centres without knowing queue lengths or wait times, leading to hours or days of waiting.
* **Zero Queue Visibility:** No transparency regarding where a farmer stands in line or when their turn will arrive.
* **Post-Delivery Uncertainty:** Lack of real-time updates on quality checks, procurement confirmations, or direct bank payment releases.
* **Physical Congestion:** Massive crowding during peak harvest seasons causes delays and potential crop spoilage.

**The Core Fix:** A digital coordination layer between the farmer and the procurement centre to handle appointments, live queue tracking, and the complete produce-to-payment lifecycle.

---

## 3. Core Features

### Farmer-Facing:
* Secure registration and login.
* Browse active procurement centres and view available date/time slots.
* Book slots specifying crop type and time window.
* Real-time queue position tracking and wait-time estimation.
* Instant in-app notifications and targeted SMS alerts.
* Complete booking, procurement, and payment history logs.

### Centre Admin-Facing:
* Daily booking dashboard per centre.
* Granular queue control: transition farmers through *Arrived* $\rightarrow$ *In Queue* $\rightarrow$ *Procured*.
* Input procured quantities and manage payment statuses.
* Live queue length and analytics overview.

---

## 4. Architecture

```text
Frontend (React, Vite, TailwindCSS)
         │
         │ REST API calls (HTTPS)
         ▼
Backend (Node.js + Express.js)
   - Auth Service (JWT)
   - Booking & Slot Service
   - Queue Engine (Position & Wait-Time Logic)
   - Notification Service (In-App + Fast2SMS Adapter)
         │
         │ Mongoose ODM
         ▼
Database (MongoDB)
   - Users, ProcurementCentres, Slots, Bookings, QueueEntries, Payments, Notifications
