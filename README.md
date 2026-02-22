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
├── lambda_handler.py        # AWS Lambda serverless function
├── autoagent.ipynb          # Content generation notebook
├── requirements-lambda.txt  # Lambda dependencies
├── .env                    # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # Documentation
```


---

##  Quick Start

### Prerequisites
- AWS Account
- AWS CLI installed and configured
- Python 3.10+
- CUDA GPU (recommended)
- Instagram Business Account
- Meta Developer Account

### Deploy to AWS Lambda

**Step 1: Create deployment package**

```bash
# Install dependencies
pip install requests python-dotenv -t lambda_package

# Copy handler
cp lambda_handler.py lambda_package/

# Create ZIP
cd lambda_package
zip -r ../lambda.zip .
cd ..
```

**Step 2: Create IAM role**

```bash
# Create trust policy
cat > trust-policy.json << 'POLICY'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
POLICY

# Create role
aws iam create-role \
    --role-name instagram-autodm-role \
    --assume-role-policy-document file://trust-policy.json

# Attach policy
aws iam attach-role-policy \
    --role-name instagram-autodm-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

**Step 3: Create Lambda function**

```bash
aws lambda create-function \
    --function-name instagram-autodm \
    --runtime python3.10 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/instagram-autodm-role \
    --handler lambda_handler.handler \
    --zip-file fileb://lambda.zip \
    --timeout 30 \
    --memory-size 512 \
    --region us-east-1
```

**Step 4: Set environment variables**

```bash
aws lambda update-function-configuration \
    --function-name instagram-autodm \
    --environment "Variables={
        INSTAGRAM_ACCESS_TOKEN=your_token,
        INSTAGRAM_USER_ID=your_user_id,
        WEBHOOK_VERIFY_TOKEN=your_verify_token,
        BRAND_NAME=YourBrand
    }" \
    --region us-east-1
```

**Step 5: Create Function URL**

```bash
# Create URL
aws lambda create-function-url-config \
    --function-name instagram-autodm \
    --auth-type NONE \
    --region us-east-1

# Add public permission
aws lambda add-permission \
    --function-name instagram-autodm \
    --statement-id FunctionURLAllowPublicAccess \
    --action lambda:InvokeFunctionUrl \
    --principal "*" \
    --function-url-auth-type NONE \
    --region us-east-1
```

**Step 6: Get your URL**

```bash
aws lambda get-function-url-config \
    --function-name instagram-autodm \
    --region us-east-1 \
    --query FunctionUrl \
    --output text
```

**Result:** `https://abc123xyz.lambda-url.us-east-1.on.aws/`

---

##  Configuration

Create `.env` file (for local testing):

```env
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
INSTAGRAM_USER_ID=your_user_id
WEBHOOK_VERIFY_TOKEN=your_verify_token
BRAND_NAME=YourBrand
```

---

##  Configure Meta Webhook

1. Go to [Meta Developers](https://developers.facebook.com)
2. Select your app
3. Click **Webhooks** → **Instagram**
4. Click **Edit Subscription**
5. Enter:
   - **Callback URL**: `https://YOUR_LAMBDA_URL/webhook`
   - **Verify Token**: (your WEBHOOK_VERIFY_TOKEN)
6. Click **Verify and Save**
7. Subscribe to:  **messages**

---

##  Auto-DM Capabilities

| Keyword Category | Example | Response |
|-----------------|---------|----------|
| **Greetings** | "Hi", "Hello" | Welcome message |
| **Price** | "How much?" | Pricing information |
| **Shipping** | "When ships?" | Delivery details |
| **Returns** | "Return policy?" | Return information |
| **Discounts** | "Any coupons?" | Promo codes |
| **Stock** | "In stock?" | Availability status |
| **Quality** | "Good quality?" | Reviews & ratings |

---

### Test Live Instagram DM

1. Send DM to your Instagram business account
2. Should receive instant auto-reply
3. Check logs:

```bash
aws logs tail /aws/lambda/instagram-autodm --follow --region us-east-1
```

---

##  Monitoring

### View Logs

```bash
# Real-time logs
aws logs tail /aws/lambda/instagram-autodm --follow --region us-east-1

# Last hour
aws logs tail /aws/lambda/instagram-autodm --since 1h --region us-east-1
```

### Check Metrics

```bash
# View invocation count
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=instagram-autodm \
    --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 3600 \
    --statistics Sum \
    --region us-east-1
```

---

##  Tech Stack

**Serverless:**
- AWS Lambda
- AWS CloudWatch (Logging)
- AWS IAM (Security)

**AI & ML:**
- PyTorch
- Stable Diffusion XL (SDXL)
- LLaMA 2
- Transformers

**APIs:**
- Instagram Graph API v24.0
- Cloudinary (Image hosting)
- Pinecone (Vector database)

**Languages:**
- Python 3.10+

---












- **Cost**: $0/month (AWS free tier)
- **Scalability**: Automatic (AWS Lambda)

---
