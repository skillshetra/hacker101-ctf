# 🧠 Hacker101 CTF Python Solutions by Skillshetra 🐍

Welcome to the **Skillshetra Hacker101 CTF repository** — a hands-on, Python-powered journey through web application security! Whether you're a budding ethical hacker, a bug bounty hunter in the making, or a developer eager to learn about real-world vulnerabilities, this repository will guide you through the Capture The Flag (CTF) challenges offered on the [Hacker101](https://ctf.hacker101.com/) platform.

> ⚠️ **Disclaimer:** This repository is for educational purposes only. All challenges are hosted by Hacker101 and designed for ethical hacking training.

---

## 🌐 What is Hacker101 CTF?

**Hacker101 CTF** is a gamified platform created by HackerOne to help aspiring security researchers learn and practice web security concepts through realistic scenarios. Each level presents a challenge — sometimes hidden, sometimes obvious — that mirrors real-world web app vulnerabilities.

---

## 📁 About This Repository

This repository contains **Python-based automation scripts** that solve various Hacker101 CTF challenges using web interaction and parsing tools like:

- `requests` – for crafting and handling HTTP requests.
- `BeautifulSoup (bs4)` – for parsing and scraping HTML content.
- `re`, `hashlib`, `base64` – for regex, encoding, and cryptographic tasks.

Each Python script corresponds to a single challenge and walks through the logic used to exploit the vulnerability and retrieve the flag.

---

## 🎯 Learning Objectives

- 🧠 Solidify your understanding of common web vulnerabilities.
- ⚙️ Practice automating recon, exploitation, and flag capture using Python.
- 🔍 Develop skills used in bug bounty programs and penetration testing.
- 🧰 Learn safe and ethical hacking techniques with real-world applications.

---

## 🧪 Solved Challenges & Key Concepts

Each challenge listed below includes a brief description and the core web security concepts it teaches:

### 1. `01_A_little_something_to_get_you_started.py`
> **Challenge Type:** Introductory Recon  
> **Concepts:**  
✔️ URL manipulation  
✔️ Directory traversal  
✔️ Basic web enumeration  

### 2. `Codys_First_Blog.py`
> **Challenge Type:** Reflected XSS  
> **Concepts:**  
✔️ JavaScript injection  
✔️ Cookie theft via malicious payloads  
✔️ DOM manipulation and alert boxes  

### 3. `Micro-CMS_v1.py`
> **Challenge Type:** Access Control  
> **Concepts:**  
✔️ IDOR (Insecure Direct Object Reference)  
✔️ URL brute-forcing  
✔️ Unprotected resources  

### 4. `Micro-CMS_v2.py`
> **Challenge Type:** SQL Injection & Auth Bypass  
> **Concepts:**  
✔️ Classic SQLi  
✔️ Authentication bypass  
✔️ Hidden flag logic and form manipulation  

### 5. `Encrypted_Pastebin.py`
> **Challenge Type:** Cryptographic Flaws  
> **Concepts:**  
✔️ Misuse of encryption  
✔️ Decoding base64 payloads  
✔️ Logic flaws in token validation  

### 6. `Model_E1337-Rolling_Code_Lock.py`
> **Challenge Type:** Reverse Engineering Logic  
> **Concepts:**  
✔️ Predictable codes  
✔️ Algorithmic brute-force  
✔️ Weak rolling-code implementation  

### 7. `Petshop_Pro.py`
> **Challenge Type:** Access Control / Logic Bug  
> **Concepts:**  
✔️ Admin panel abuse  
✔️ Price manipulation  
✔️ Business logic flaws  

### 8. `Photo_Gallery.py`
> **Challenge Type:** IDOR  
> **Concepts:**  
✔️ Bypassing access controls  
✔️ URL manipulation  
✔️ Viewing private content  

### 9. `Postbook.py`
> **Challenge Type:** Session Handling  
> **Concepts:**  
✔️ Session hijacking  
✔️ Predictable session tokens  
✔️ Weak authentication  

### 10. `Ticketastic_Demo_Instance.py`  
### 11. `Ticketastic_Live_Instance.py`
> **Challenge Type:** Multi-stage logic & parameter abuse  
> **Concepts:**  
✔️ Forging tickets  
✔️ Logic flaw exploitation  
✔️ Input tampering across endpoints  

---

## 🔧 Tools & Libraries Used

| Library        | Purpose                          |
|----------------|----------------------------------|
| `requests`     | HTTP request handling             |
| `BeautifulSoup`| HTML parsing and data extraction |
| `re`           | Regular expressions               |
| `hashlib`      | MD5, SHA1 hashing and comparison |
| `base64`       | Encoding and decoding payloads   |

📌 All dependencies are listed in the `requirements.txt` file.

---

## 🗂️ Project Structure

hacker101-ctf/
│
├── 01_A_little_something_to_get_you_started.py
├── Codys_First_Blog.py
├── Encrypted_Pastebin.py
├── Micro-CMS_v1.py
├── Micro-CMS_v2.py
├── Model_E1337-Rolling_Code_Lock.py
├── Petshop_Pro.py
├── Photo_Gallery.py
├── Postbook.py
├── Ticketastic_Demo_Instance.py
├── Ticketastic_Live_Instance.py
├── requirements.txt
└── README.md

---

## 🚀 Getting Started

To run any challenge script:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/skillshetra/hacker101-ctf.git
   cd hacker101-ctf
