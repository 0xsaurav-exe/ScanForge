# 🔥 ScanForge - Web Vulnerability Scanner
![ScanForge Demo](assets/scanforge-demo.png)
ScanForge is a lightweight Python-based tool designed to detect common web vulnerabilities such as:

* Cross-Site Scripting (XSS)
* SQL Injection (SQLi)

---

## 🚀 Features

* Supports **GET parameter testing**
* Detects **XSS via reflection**
* Detects **SQLi via response difference**
* CLI support (`-u`, `-f`, `-o`)
* Generates **HTML reports**
* Clean and readable output

---

## ⚙️ Installation

```bash
git clone https://github.com/0xsaurav-exe/ScanForge.git
cd ScanForge
pip install requests
```

---

## 🧪 Usage

### Scan single target

```bash
python3 scanforge.py -u "http://example.com/page?id=1"
```

### Scan multiple targets

```bash
python3 scanforge.py -f urls.txt
```

### Save custom report

```bash
python3 scanforge.py -u <url> -o result.html
```

---

## 📊 Example Output

```
[!] SQLi FOUND → id
Payload: ' OR '1'='1
URL: http://example.com/page?id=' OR '1'='1
```

---

## 📄 Report
## 📊 Sample Report

![Report Preview](assets/scanforge-report.png)
ScanForge generates an HTML report:

```
report.html
```

---

## ⚠️ Disclaimer

This tool is for **educational and authorized security testing only**.

---

## 👨‍💻 Author

0xsaurav-exe
