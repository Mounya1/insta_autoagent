# AI-Powered Instagram Marketing Automation

An intelligent Instagram automation system combining **SDXL image generation**, **LLaMA captions**, and **real-time DM responses** to create and manage social media content at scale.
##  Features

###  AI Content Generation
- **SDXL Image Generation**: Professional product photos using Stable Diffusion XL
- **LLaMA Captions**: AI-powered engaging Instagram captions
- **Automated Posting**: Publishes content to Instagram automatically
- **Budget Management**: Tracks spending and post limits

###  Intelligent Auto-DM
- **Real-time Webhook**: Instant response to Instagram DMs
- **15+ Keyword Categories**: Price, shipping, returns, discounts, etc.
- **Natural Conversations**: Context-aware human-like responses
- **Analytics Dashboard**: Track messages, responses, engagement

###  Technical Stack
- **Backend**: Flask (Python)
- **AI Models**: SDXL, LLaMA 2
- **Image Hosting**: Cloudinary
- **Vector DB**: Pinecone
- **Instagram API**: Graph API v24.0

---

##  Project Structure

```
instagram-ai-agent/
├── app.py                 # Auto-DM webhook server
├── autoagent.ipynb       # Content generation notebook
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

---

##  Quick Start

### Prerequisites

- Python 3.10+
- CUDA GPU (recommended)
- Instagram Business Account
- Meta Developer Account

### Installation


1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

---

##  Configuration

Create `.env` file:

```env
# Instagram API
INSTAGRAM_ACCESS_TOKEN=your_token
INSTAGRAM_USER_ID=your_user_id
PAGE_ACCESS_TOKEN=your_page_token
FACEBOOK_PAGE_ID=your_page_id

# Webhook
WEBHOOK_VERIFY_TOKEN=your_verify_token

# Brand
BRAND_NAME=YourBrand

# Optional Services
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
PINECONE_API_KEY=your_key
```

---

##  Usage

### Auto-DM Server

```bash
python app.py
```

Server starts on `http://localhost:5000`

### Content Generator

```bash
jupyter notebook autoagent.ipynb
```

Run cells 1-14, then: `tier2.run(num_posts=3)`

---

##  Auto-DM Capabilities

| Keyword | Example | Response |
|---------|---------|----------|
| Greetings | "Hi", "Hello" | Welcome message |
| Price | "How much?" | Pricing info |
| Shipping | "When ships?" | Delivery details |
| Returns | "Return policy?" | Return info |
| Discounts | "Any coupons?" | Promo codes |


---

##  Performance

- Image Generation: 3-5 seconds (GPU)
- Caption Generation: 1-2 seconds  
- DM Response: <1 second
- Handles 1000+ DMs/day

---

##  Deployment

### Heroku

```bash
heroku create your-app
heroku config:set INSTAGRAM_ACCESS_TOKEN=your_token
git push heroku main
```

### Railway

1. Connect GitHub repo
2. Add environment variables
3. Deploy

---

##  Tech Stack

**AI:** PyTorch • SDXL • LLaMA 2 • Transformers

**Backend:** Flask • Python 3.10+ • Gunicorn

**APIs:** Instagram Graph API • Cloudinary • Pinecone

---
