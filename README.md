# AI Autonomous Brand Growth Agent

An intelligent Instagram automation system combining **SDXL image generation**, **LLaMA captions**, and **real-time DM responses** to create and manage social media content at scale.
##  Features

###  AI Content Generation
- **SDXL Image Generation**: Professional product photos using Stable Diffusion XL
- **Zero Server Management**: Runs on AWS Lambda
- **LLaMA Captions**: AI-powered engaging Instagram captions
- **Automated Posting**: Publishes content to Instagram automatically
- **Budget Management**: Tracks spending and post limits

###  Intelligent Auto-DM
- **Real-time Webhook**: Instant response to Instagram DMs
- **Zero Server Management**: Runs on AWS Lambda
- **15+ Keyword Categories**: Price, shipping, returns, discounts, etc.
- **Natural Conversations**: Context-aware human-like responses
- **Analytics Dashboard**: Track messages, responses, engagement

##  What This Project Does

### Two Main Parts:

**1. Auto-Post Bot** (Jupyter Notebook)
- Creates product images using AI
- Generates captions automatically
- Posts to Instagram


**2. Auto-DM Bot** (AWS Lambda)
- Responds to Instagram messages instantly
- Handles customer questions 24/7
- Runs serverless

---

##  What You Need

### Accounts Required:
-  Instagram Business Account
-  Facebook Developer Account
-  AWS Account 
-  Cloudinary Account 

### Software Required:
- AWS CLI (command line tool)
- Python 3.10
- Web browser

---

##  Complete Setup Guide

---

## PART 1: Instagram & Facebook Setup

### Step 1: Create Instagram Business Account

**If you have personal account:**
1. Open Instagram app
2. Go to **Profile** → **Settings**
3. Tap **Account**
4. Tap **Switch to Professional Account**
5. Choose **Business**
6. Complete setup

**If creating new:**
1. Download Instagram app
2. Sign up for new account
3. Immediately switch to Business (follow above)


---

### Step 2: Create Facebook Page

1. Go to facebook.com
2. Click **Pages** (left menu)
3. Click **Create New Page**
4. Enter page name (match your Instagram)
5. Choose category (Shopping/Retail)
6. Click **Create Page**



---

### Step 3: Link Instagram to Facebook Page

1. On your Facebook Page
2. Click **Settings** (left menu)
3. Click **Instagram**
4. Click **Connect Account**
5. Login to your Instagram Business account
6. Confirm connection


---

### Step 4: Create Facebook Developer App

1. Go to developers.facebook.com
2. Click **My Apps** (top right)
3. Click **Create App**
4. Choose **Business** type
5. Enter app name (e.g., "Instagram Bot")
6. Enter contact email
7. Click **Create App**


---

### Step 5: Add Instagram Product to App

1. In your app dashboard
2. Find **Instagram** in products list
3. Click **Set Up**
4. Follow prompts to add product



---

### Step 6: Get Your IDs and Tokens

#### A. Get Instagram User ID

1. Go to developers.facebook.com/tools/explorer
2. Select your app (top right dropdown)
3. In the field, type: `me?fields=instagram_business_account`
4. Click **Submit**
5. Copy the number shown (looks like `17841415236594174`)
6. Save this - it's your **Instagram User ID**

#### B. Get Facebook Page ID

1. Go to your Facebook Page
2. Click **Settings**
3. Click **Page Info**
4. Look for **Page ID**
5. Copy the number
6. Save this - it's your **Facebook Page ID**

#### C. Get Page Access Token (for posting)

1. Go to developers.facebook.com/tools/explorer
2. Select your app
3. Click **Generate Access Token**
4. Select these permissions:
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `instagram_basic`
   - `instagram_content_publish`
5. Click **Generate Token**
6. Copy token (starts with `EAAU...`)
7. Save this - it's your **Page Access Token**

#### D. Get Instagram User Access Token (for DMs)

1. Same Graph API Explorer
2. Click **Generate Access Token** again
3. Select these permissions:
   - `instagram_manage_messages`
   - `instagram_basic`
4. Click **Generate Token**
5. Copy token (starts with `IGAA...`)
6. Save this - it's your **Instagram Access Token**


**Save these somewhere safe:**
- Instagram User ID: `17841415236594174`
- Facebook Page ID: `966806373184726`
- Page Access Token: `EAAU...`
- Instagram Access Token: `IGAA...`

---

## PART 2: Auto-DM Bot Setup (AWS Lambda)

### What You're Building:
A serverless bot that responds to Instagram DMs automatically, 24/7

---

### Step 7: Install AWS CLI

**Windows:**
1. Download: https://awscli.amazonaws.com/AWSCLIV2.msi
2. Run installer
3. Restart computer



**Verify:**
1. Open Command Prompt/Terminal
2. Type: `aws --version`
3. Should show version number



---

### Step 8: Create AWS Account



---

### Step 9: Configure AWS CLI

1. Go to AWS Console
2. Search for **IAM**
3. Click **Users** → **Create User**
4. Username: `lambda-deployer`
5. Attach policies:
   - `AWSLambda_FullAccess`
   - `IAMFullAccess`
6. Click **Create User**
7. Go to user → **Security credentials**
8. Click **Create access key**
9. Choose **CLI**
10. Copy **Access Key ID** and **Secret Access Key**

**In Command Prompt:**
```
aws configure
```
Enter:
- Access Key ID: (paste yours)
- Secret Access Key: (paste yours)
- Region: us-east-1
- Format: json



---

### Step 10: Create Project Files

**Create folder:**
1. Create folder: `instagram-autodm`
2. Inside, create file: `lambda_handler.py`
3. Copy the Lambda code into this file (from project files)
4. Create file: `.env` with your tokens


### Step 11: Deploy to AWS Lambda

**Run these commands in order:**

1. Create package folder
2. Install dependencies
3. Create ZIP file
4. Create IAM role for Lambda
5. Create Lambda function
6. Set environment variables
7. Create public URL
8. Add permissions

---

### Step 12: Configure Instagram Webhook

1. Go to developers.facebook.com
2. Your app → **Webhooks**
3. Find **Instagram** section
4. Click **Edit Subscription**
5. Enter:
   - **Callback URL:** Your Lambda URL + `/webhook`
   - **Verify Token:** `my_secret_token_123`
6. Click **Verify and Save**
7. Should show  **Successfully verified**
8. Check box: **messages**
9. Click **Save**


---

### Step 13: Test Auto-DM

1. Open Instagram app
2. Send DM to your business account
3. Type: "Hello"
4. Should get instant reply!



---

## PART 3: Auto-Post Bot Setup (Jupyter Notebook)

### What You're Building:
AI that generates product images and captions, then posts to Instagram

---





### Step 14: Configure Tokens in Notebook

1. Find **Cell 4** (Config section)
2. Update these values:
   - `PAGE_ACCESS_TOKEN` → Your EAAU... token
   - `FACEBOOK_PAGE_ID` → Your page ID
   - `INSTAGRAM_USER_ID` → Your IG user ID
   - `BRAND_NAME` → Your brand name


---

### Step 15: Setup Cloudinary (Optional but Recommended)

1. Go to cloudinary.com
2. Sign up (free)
3. Dashboard → Copy:
   - Cloud Name
   - API Key
   - API Secret
4. Add to notebook Cell 4



### Step 16: Run Notebook

1. Click **Run All** (or Ctrl+Shift+Enter)
2. Wait 2-3 minutes for setup
3. All cells should complete
4. Last output: "Tier2 ready"



### Step 20: Generate and Post

1. Go to last cell
2. Run: `tier2.run(num_posts=3)`
3. Watch it:
   - Generate 3 AI images
   - Create 3 AI captions
   - Post 3 times to Instagram
4. Check Instagram - posts should be live!



##  Complete Setup Summary

### What You Have Now:

**Auto-DM Bot:**
- ✅ Runs on AWS Lambda (serverless)
- ✅ Responds to DMs in <1 second
- ✅ Handles unlimited messages
- ✅ Works 24/7 automatically

**Auto-Post Bot:**
- ✅ Runs on Kaggle (free GPU)
- ✅ Generates AI images (SDXL)
- ✅ Generates AI captions (LLaMA)
- ✅ Posts to Instagram
- ✅ You control when to post

---

##  Daily Usage

### Posting Content:
1. Open notebook
2. Run last cell: `tier2.run(num_posts=3)`
3. Wait 5 minutes
4. Done! 3 new posts live on Instagram

### DM Responses:
- Nothing to do!
- Bot handles all DMs automatically
- Works 24/7 without you

### Monitoring:
**Check DM logs:**
```
aws logs tail /aws/lambda/instagram-autodm --follow --region us-east-1
```

**Check Lambda is healthy:**
- Visit: `https://YOUR_LAMBDA_URL/health`
- Should show: `{"status":"healthy"}`

---

##  Maintenance

### Update Auto-DM Responses:

1. Edit `lambda_handler.py`
2. Change the responses in `generate_reply()` function
3. Re-create ZIP file
4. Update Lambda function

### Update Post Settings:

1. Open notebook
2. Edit Cell 4 (Config)
3. Change brand name, hashtags, etc.
4. Run all cells again

---


## Project Structure

```
instagram-ai-agent/
├── lambda_handler.py        # AWS Lambda serverless function
├── autoagent.ipynb          # Content generation notebook
├── requirements-lambda.txt  # Lambda dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # Documentation
```

---


### Technologies Used:
- Instagram Graph API v24.0
- AWS Lambda (serverless)
- Python 3.10
- Stable Diffusion XL (SDXL)
- LLaMA 2 (AI language model)
- Cloudinary (image hosting)
- Meta Webhooks

---


