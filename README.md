# URL Shortening Service 🔗

A scalable URL Shortening Service built using Python, Flask, and dictionary-based
in-memory storage. The service supports:

•	Custom aliases
•	Expiration (TTL)
•	Hash-based key generation
•	Fast O(1) lookups using dictionaries
•	Usage analytics (click count + last accessed)
•	Clean REST API design & structured error handling

This project demonstrates backend design, API development, data structures,
and system thinking — similar to real-world URL shorteners like Bitly or TinyURL.

## 🚀 Features

•	Hash-generated short URLs
•	Optional custom aliases
•	Optional expiration time (TTL)
•	Fast redirection using dictionary lookups
•	Click analytics tracking
•	Separate stats API
•	Graceful error responses

## 🧩 Tech Stack

•	Language : Python
•	Framework : Flask (REST APIs)
•	Data Structures : Hashing + Dictionaries (O(1) lookup)
•	Other : datetime, hashing, redirect handling

## ▶️ Running the Project
pip install flask
python url_shortener.py




