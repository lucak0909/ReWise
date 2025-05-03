# ReWise

ReWise is an AI-powered educational platform that helps children study smarter — and get rewarded for it. Parents upload learning materials and fund a study budget. Children earn real money by answering quiz questions correctly, creating a powerful incentive to study effectively and consistently. Quizzes are generated automatically from notes or books, and parents can track their child’s progress and pain points in real time.

---

## ✨ Key Features

* 🔐 Dual Login System
  Separate interfaces and access for parents and children.

* 📚 AI Quiz Generator
  Upload PDFs, text files, or images — ReWise creates multiple-choice quizzes from the content automatically.

* 💸 Real Rewards, Real Learning
  Children earn a parent-defined reward for each correct answer, up to the total budget invested.

* 📊 Insightful Parent Dashboard
  Track quiz results, weak topics, and study consistency.

* 🔁 Budget-Based Learning
  Once the reward budget is used up, no further earnings are possible until parents invest again — keeping the reward system fair and controlled.

* 🛡️ Anti-Cheat Measures
  Reward only on first attempt, randomized questions, and optional explanation prompts to promote honest effort.

---

## 🛠 Tech Stack

* Backend: Python 3 + Flask
* Frontend: HTML, CSS (Bootstrap or Tailwind), JavaScript
* AI/NLP: OpenAI API or custom NLP pipeline for quiz generation
* Database: PostgreSQL or SQLite (dev)
* Authentication: Flask-Login + Role-based access
* Optional: Stripe/PayPal API integration for real-world payment logic

---

## 🔁 User Flow

1. Parent signs up and sets a study budget (e.g., €10) and reward rate (e.g., €0.10/question).
2. Parent uploads study material (PDF/text/image).
3. ReWise generates quizzes from the uploaded content using AI.
4. Child logs in, completes quizzes, and earns money for correct answers.
5. Parent monitors stats, earnings, and weak subjects.
6. Once the budget is reached, earnings pause until renewed or reset.

---

## 🚀 Getting Started (Dev Setup)

Clone and run the app locally:

```bash
git clone https://github.com/yourusername/rewise.git
cd rewise
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

Set up environment variables in a .env file:

```
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

---

## 📁 Project Structure

```
/rewise
│
├── app/
│   ├── static/
│   ├── templates/
│   ├── routes/
│   ├── models.py
│   └── quiz_generator.py
│
├── tests/
├── requirements.txt
├── config.py
└── run.py
```

---

## 🛣️ Roadmap

* [x] Role-based auth (Parent / Child)
* [x] Quiz generator from text uploads
* [x] Reward system with budget cap
* [ ] OCR for image-based notes
* [ ] In-app quiz streaks & badges
* [ ] Mobile app version (React Native or Flutter)
* [ ] Voice prompts / accessibility enhancements

---

## 🙌 Contributing

ReWise is in early-stage development. PRs and feedback are welcome. If you're interested in helping develop features, improve AI accuracy, or enhance UI/UX, please open an issue or submit a pull request.

📫 Contact: [team@rewise.app](mailto:team@rewise.app) (placeholder)
