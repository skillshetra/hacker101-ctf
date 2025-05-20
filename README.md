# 🧠 Hacker101 CTF Challenges Solved with Python 🐍

Welcome to the **Skillshetra** GitHub repository! 🚀 This repo contains Python-based solutions for various web application challenges from the [Hacker101 CTF platform](https://ctf.hacker101.com/). All challenges have been solved using **`requests`** and **`BeautifulSoup`** (bs4), two powerful Python libraries for web interaction and scraping.

> 👨‍💻 This repository is perfect for beginners and intermediates in **ethical hacking**, **bug bounty hunting**, or **web app penetration testing** who want hands-on practice with real-world vulnerabilities.

---

## 📁 Repository Overview

Each Python file in this repo represents a solution to a specific Hacker101 CTF challenge. Challenges simulate vulnerabilities like:

- ✅ SQL Injection (SQLi)
- ✅ Cross-Site Scripting (XSS)
- ✅ Insecure Direct Object Reference (IDOR)
- ✅ Server-Side Request Forgery (SSRF)
- ✅ Authentication Bypass
- ✅ Session Hijacking
- ✅ Misconfigurations and Logic Flaws

---

## 📜 Table of Contents

- [🎯 Objectives](#-objectives)
- [🧪 Challenges & Solutions](#-challenges--solutions)
- [🔧 Tools & Libraries](#-tools--libraries)
- [📂 Project Structure](#-project-structure)
- [⚙️ How to Run](#️-how-to-run)
- [🙌 Contributions](#-contributions)
- [📬 Contact](#-contact)
- [📝 License](#-license)

---

## 🎯 Objectives

This project aims to:

- 🧠 Apply theoretical knowledge of web security.
- 🤖 Automate exploitation using Python scripts.
- 🔍 Understand common web vulnerabilities.
- 🧰 Practice safe and ethical hacking techniques.

---

## 🧪 Challenges & Solutions

Below are the currently solved CTFs with a brief description of what was done:

### 1️⃣ 01_A_little_something_to_get_you_started.py

> A great warm-up! This challenge introduces basic recon and flag discovery techniques.

**Concepts Covered:**  
✔️ Basic web enumeration  
✔️ URL manipulation  
✔️ Simple directory traversal

---

### 2️⃣ Codys_First_Blog.py

> A mock blog with exploitable admin features and vulnerable inputs.

**Concepts Covered:**  
✔️ Reflected XSS  
✔️ Cookie stealing  
✔️ JavaScript injection

---

### 3️⃣ Micro-CMS_v1.py

> A simple content management system with broken access control.

**Concepts Covered:**  
✔️ IDOR  
✔️ Parameter tampering  
✔️ URL brute-forcing

---

### 4️⃣ Micro-CMS_v2.py

> Same CMS, new vulnerabilities — can you break it again?

**Concepts Covered:**  
✔️ SQL Injection  
✔️ Auth bypass  
✔️ Hidden flag logic

---

## 🔧 Tools & Libraries

This project heavily utilizes:

| Library        | Purpose                        |
|----------------|--------------------------------|
| `requests`     | Sending HTTP requests/responses|
| `BeautifulSoup`| HTML parsing and extraction    |
| `re`           | Regular expressions            |
| `hashlib`      | Hashing (MD5/SHA1) operations  |
| `base64`       | Encoding/decoding payloads     |

> All dependencies are listed in `requirements.txt`.

---

## 📂 Project Structure

```bash
skillshetra/hacker101-ctf/
│
├── 01_A_little_something_to_get_you_started.py
