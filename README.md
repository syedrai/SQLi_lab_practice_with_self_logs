# SQLi_lab_practice_with_self_logs
A deliberately vulnerable Flask web application designed to demonstrate SQL injection attacks in a controlled, self-contained environment. This lab provides hands-on experience with both vulnerable and secure coding practices.
# Flask SQL Injection Lab - Educational Security Demonstration

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Security](https://img.shields.io/badge/Security-Educational%20Only-red)

A deliberately vulnerable Flask web application designed to demonstrate SQL injection attacks in a controlled, self-contained environment. This lab provides hands-on experience with both vulnerable and secure coding practices.

 🚨 Disclaimer

This project is for educational and authorized testing purposes only. 
- ⚠️ DO NOT DEPLOY IN PRODUCTION
- ⚠️ FOR LEGAL, EDUCATIONAL USE ONLY
- ⚠️ USE ONLY IN ISOLATED ENVIRONMENTS

 🎯 Purpose

This lab helps developers, security students, and penetration testers understand:
- How SQL injection vulnerabilities occur
- Common attack vectors and payloads
- The importance of input validation
- Secure coding practices with parameterized queries
- Attack detection and logging

 🛠 Features

 Vulnerable Components
- SQL Injection in Authentication - Direct string concatenation in login queries
- Insecure Search Functionality - Vulnerable user search with SQLi
- Verbose Error Messages - Detailed SQL errors exposed to attackers

 Secure Counterparts
- Parameterized Queries - Safe SQL execution examples
- Input Validation - Demonstration of proper sanitization
- Comprehensive Logging - Attack detection and monitoring

 Educational Tools
- Automated Attack Script - Pre-built SQL injection tests
- Real-time Logging - Live attack monitoring
- Side-by-Side Comparison - Vulnerable vs secure code examples

 🚀 Quick Start

 Prerequisites
- Python 3.8+
- pip package manager

 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/flask-sqli-lab.git
cd flask-sqli-lab
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the vulnerable server
```bash
python app.py
```

4. Launch attacks (in separate terminal)
```bash
python attacker.py
```

5. View attack logs
   - Visit `http://localhost:5000/logs` in your browser
   - Or check `attack_logs.log` file

 🎮 Usage Examples

 Manual Testing
Access the web interface at `http://localhost:5000` and try these payloads:

Authentication Bypass:
```sql
' OR '1'='1
admin'--
```

Data Extraction:
```sql
' UNION SELECT 1,2,3--
```

Database Schema Discovery:
```sql
' UNION SELECT sql,sql,sql,sql FROM sqlite_master--
```

 Automated Testing
Run the included attack script to demonstrate various techniques:
```bash
python attacker.py
```

 📊 What You'll Learn

 Attack Vectors
- Boolean-based blind SQL injection
- Union-based data extraction
- Error-based information disclosure
- Time-based blind attacks
- Authentication bypass techniques

 Defense Mechanisms
- Parameterized queries with SQLite
- Input validation and sanitization
- Principle of least privilege
- Security logging and monitoring
- Error handling best practices

 🏗 Project Structure

```
flask-sqli-lab/
├── app.py                 # Main vulnerable Flask application
├── attacker.py            # Automated attack demonstration script
├── requirements.txt       # Python dependencies
├── users.db              # SQLite database (auto-generated)
├── attack_logs.log       # Attack logs (auto-generated)
└── README.md             # This file
```

 🔍 Code Examples

 Vulnerable Code (What NOT to do)
```python
# ❌ VULNERABLE: String concatenation
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

 Secure Code (Best Practice)
```python
# ✅ SECURE: Parameterized queries
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

 📈 Learning Path

1. Beginner: Use the web interface to test basic payloads
2. Intermediate: Study the vulnerable vs secure code comparison
3. Advanced: Extend the attack script with new techniques
4. Expert: Implement additional security controls and monitoring

 🛡 Security Recommendations

- Always use parameterized queries or ORM
- Implement proper input validation
- Use principle of least privilege for database accounts
- Employ web application firewalls (WAF)
- Regular security testing and code reviews
- Comprehensive logging and monitoring

 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests with:
- New vulnerability examples
- Additional attack techniques
- Enhanced logging features
- Educational documentation
- Security improvements (for the educational components)

 📚 Resources

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PortSwigger SQL Injection Academy](https://portswigger.net/web-security/sql-injection)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.3.x/security/)

 ⚖️ Legal & Ethical Use

By using this software, you agree:
- To use only in environments you own or have explicit permission to test
- Not to use for malicious or illegal activities
- To comply with all applicable laws and regulations
- To assume all responsibility for your actions

 🐛 Reporting Issues

Found a bug or have a suggestion? Please open an issue on GitHub.

---

Remember: The best defense is understanding the offense. Use this lab to build more secure applications! 🔒

---

<div align="center">
  
*"Knowledge is the best defense against cyber threats"*

</div>
