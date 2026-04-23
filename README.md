# 🤟 HearMe  
### A Smart Sign Language Communication Platform

![Python](https://img.shields.io/badge/Python-Backend-blue)
![Django](https://img.shields.io/badge/Django-Framework-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![WebRTC](https://img.shields.io/badge/WebRTC-Realtime-orange)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

---

##  UI Preview

### Landing Page  
![Landing](./project4/screenshots/landing-page.png)

### Landing Page Sign-In
![LandingSignIn](./project4/screenshots/landing-page-signIn.png)

### Calander
![Calander](./project4/screenshots/Calender.png)

### Event
![Event](./project4/screenshots/Event.png)

### games
![games](./project4/screenshots/games.png)

### name game
![nameGame](./project4/screenshots/name-game.png)

### guess game
![guessGame](./project4/screenshots/guess-game.png)

### Live Video Call  
![Call](./project4/screenshots/Rooms-call.png)

### Sign Language Lessons  
![Lessons](./project4/screenshots/ESL-Lessons.png)

### Sign Language Lessons Details  
![LessonsDetails](./project4/screenshots/lesson-details.png)

### Recognition  
![Recognition](./project4/screenshots/Recognition.png)

### Profile
![Profile](./project4/screenshots/profile.png)

---

## Project Overview

**HearMe** is a full-stack web application designed to bridge communication between deaf and hearing individuals using sign language technology.

The platform focuses on:
- Real-time communication  
- Accessibility and inclusivity  
- AI-powered gesture recognition  
- Interactive learning experience  

---

##  Live Demo



---

### Current Features

- Real-time video calling using WebRTC  
- Live chat inside call rooms  
- User authentication (Sign up / Login / Logout)  
- Sign language learning modules  
- Responsive and accessible UI  
- Room-based communication system  

---

## System Design

### Entities

**Users**
- ID  
- Name  
- Email  
- Password  

**Rooms**
- RoomID  
- Name  
- Max Participants  

**Messages**
- MessageID  
- Content  
- Timestamp  
- UserID (Reference)  
- RoomID (Reference)  

**Lessons**
- LessonID  
- Title  
- Video  
- Language  

---

## Built With

### Backend
- Python (Django)  
- Django Channels (WebSockets)  

### Frontend
- HTML, CSS, JavaScript  

### Database
- PostgreSQL  

### Libraries / Tools
- OpenCV – gesture detection  
- TensorFlow / PyTorch – ML models  
- WebRTC – real-time video/audio  
- gTTS / pyttsx3 – text-to-speech  
- YouTube API – lesson videos  

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/hearme.git
cd hearme
