
import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import requests

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

# Instagram ID 
IG_ID = os.getenv("INSTAGRAM_USER_ID")

# Webhook verify token 
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "your_verify_token")

# Brand settings
BRAND_NAME = os.getenv("BRAND_NAME", "YourBrand")

# Instagram Graph API URL 
GRAPH_API_BASE = "https://graph.instagram.com/v24.0"
MESSAGES_ENDPOINT = f"{GRAPH_API_BASE}/{IG_ID}/messages"

# ══════════════════════════════════════════════════════════
# LOGGING SETUP
# ══════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════
# MESSAGE TRACKING
# ══════════════════════════════════════════════════════════

processed_messages = set()  # Prevent duplicate replies
conversation_history = []    # Store all conversations
stats = {
    "total_received": 0,
    "total_sent": 0,
    "total_errors": 0,
    "start_time": datetime.now().isoformat()
}

# ══════════════════════════════════════════════════════════
# FLASK APP
# ══════════════════════════════════════════════════════════

app = Flask(__name__)

# ══════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════

@app.route("/")
def home():
    """Server status page"""
    uptime = (datetime.now() - datetime.fromisoformat(stats['start_time'])).total_seconds()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Auto DM - Production Server</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 30px;
                text-align: center;
            }}
            h1 {{ 
                color: #E1306C;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .subtitle {{
                color: #666;
                font-size: 1.1em;
            }}
            .status-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .card {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            .card h2 {{
                color: #333;
                font-size: 1.3em;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .icon {{
                font-size: 1.5em;
            }}
            .stat-row {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }}
            .stat-row:last-child {{
                border-bottom: none;
            }}
            .stat-label {{
                color: #666;
                font-weight: 500;
            }}
            .stat-value {{
                color: #333;
                font-weight: 600;
            }}
            .status-badge {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: 600;
            }}
            .status-online {{
                background: #d4edda;
                color: #155724;
            }}
            .endpoint-list {{
                list-style: none;
            }}
            .endpoint-list li {{
                padding: 12px;
                margin: 8px 0;
                background: #f8f9fa;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
            }}
            .endpoint-method {{
                display: inline-block;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.85em;
                font-weight: 600;
                margin-right: 10px;
            }}
            .method-get {{ background: #d1ecf1; color: #0c5460; }}
            .method-post {{ background: #fff3cd; color: #856404; }}
            code {{
                background: #f8f9fa;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 0.9em;
            }}
            .footer {{
                text-align: center;
                color: white;
                margin-top: 30px;
                padding: 20px;
            }}
            @media (max-width: 768px) {{
                h1 {{ font-size: 1.8em; }}
                .status-grid {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Instagram Auto DM Server</h1>
                <p class="subtitle">Production-Ready Webhook System</p>
                <div style="margin-top: 15px;">
                    <span class="status-badge status-online">● ONLINE</span>
                </div>
            </div>

            <div class="status-grid">
                <div class="card">
                    <h2><span class="icon">📊</span> Live Statistics</h2>
                    <div class="stat-row">
                        <span class="stat-label">Messages Received</span>
                        <span class="stat-value">{stats['total_received']}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Replies Sent</span>
                        <span class="stat-value">{stats['total_sent']}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Errors</span>
                        <span class="stat-value">{stats['total_errors']}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Conversations</span>
                        <span class="stat-value">{len(conversation_history)}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Uptime</span>
                        <span class="stat-value">{int(uptime)} seconds</span>
                    </div>
                </div>

                <div class="card">
                    <h2><span class="icon">⚙️</span> Configuration</h2>
                    <div class="stat-row">
                        <span class="stat-label">Brand</span>
                        <span class="stat-value">{BRAND_NAME}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Instagram ID</span>
                        <span class="stat-value">{IG_ID}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Token Type</span>
                        <span class="stat-value">IGAA</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">API Version</span>
                        <span class="stat-value">v24.0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Verify Token</span>
                        <span class="stat-value">{WEBHOOK_VERIFY_TOKEN}</span>
                    </div>
                </div>

                <div class="card">
                    <h2><span class="icon">🔗</span> API Endpoints</h2>
                    <ul class="endpoint-list">
                        <li>
                            <span class="endpoint-method method-get">GET</span>
                            <code>/webhook</code>
                        </li>
                        <li>
                            <span class="endpoint-method method-post">POST</span>
                            <code>/webhook</code>
                        </li>
                        <li>
                            <span class="endpoint-method method-get">GET</span>
                            <code>/stats</code>
                        </li>
                        <li>
                            <span class="endpoint-method method-get">GET</span>
                            <code>/test</code>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="footer">
                <p>🚀 Powered by Flask + Instagram Graph API v24.0</p>
                <p style="margin-top: 10px; opacity: 0.8;">Running 24/7 • Auto-responds in real-time</p>
            </div>
        </div>
    </body>
    </html>
    """

# ══════════════════════════════════════════════════════════
# WEBHOOK ENDPOINT
# ══════════════════════════════════════════════════════════

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    """Handle webhook verification and DM events"""
    
    # ─── GET: Webhook Verification ───
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        logger.info("="*60)
        logger.info("🔍 WEBHOOK VERIFICATION REQUEST")
        logger.info("="*60)
        logger.info(f"Mode:          {mode}")
        logger.info(f"Verify Token:  {token}")
        logger.info(f"Challenge:     {challenge}")
        logger.info("="*60)
        
        if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
            logger.info(" VERIFICATION SUCCESS - Returning challenge")
            return challenge, 200
        else:
            logger.warning(" VERIFICATION FAILED")
            logger.warning(f"Expected token: {WEBHOOK_VERIFY_TOKEN}")
            logger.warning(f"Got token:      {token}")
            return "Forbidden", 403
    
    # ─── POST: Receive DM Events ───
    elif request.method == "POST":
        try:
            data = request.get_json()
            
            logger.info("="*60)
            logger.info(" WEBHOOK EVENT RECEIVED")
            logger.info("="*60)
            logger.info(f"Payload: {json.dumps(data, indent=2)}")
            logger.info("="*60)
            
            stats["total_received"] += 1
            
            # Process Instagram events
            if 'entry' in data:
                for entry in data['entry']:
                    if 'messaging' in entry:
                        for event in entry['messaging']:
                            process_message_event(event)
            
            return jsonify({"status": "ok"}), 200
            
        except Exception as e:
            logger.error(f" Error processing webhook: {e}")
            import traceback
            traceback.print_exc()
            stats["total_errors"] += 1
            return jsonify({"error": str(e)}), 500

# ══════════════════════════════════════════════════════════
# PROCESS MESSAGE EVENT
# ══════════════════════════════════════════════════════════

def process_message_event(event):
    """Process incoming DM and send auto-reply"""
    try:
        # Extract message details
        sender_id = event.get('sender', {}).get('id')
        recipient_id = event.get('recipient', {}).get('id')
        message = event.get('message', {})
        message_id = message.get('mid')
        message_text = message.get('text', '')
        
        logger.info("-"*60)
        logger.info(" MESSAGE DETAILS")
        logger.info("-"*60)
        logger.info(f"From:       {sender_id}")
        logger.info(f"To:         {recipient_id}")
        logger.info(f"Message ID: {message_id}")
        logger.info(f"Text:       {message_text}")
        logger.info("-"*60)
        
        # Validate message
        if recipient_id != IG_ID:
            logger.info(" Not for our account, skipping")
            return
        
        if not message_text:
            logger.info(" No text content, skipping")
            return
        
        if message_id in processed_messages:
            logger.info(" Already processed, skipping")
            return
        
        # Mark as processed
        processed_messages.add(message_id)
        
        # Generate reply
        reply_text = generate_reply(message_text)
        logger.info(f" Generated reply: {reply_text}")
        
        # Send reply
        success = send_dm(sender_id, reply_text)
        
        # Log conversation
        conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "sender_id": sender_id,
            "inbound": message_text,
            "reply": reply_text,
            "sent": success
        })
        
    except Exception as e:
        logger.error(f" Error processing message: {e}")
        import traceback
        traceback.print_exc()
        stats["total_errors"] += 1

# ══════════════════════════════════════════════════════════
# GENERATE AUTO-REPLY (15+ Keyword Categories)
# ══════════════════════════════════════════════════════════

def generate_reply(text):
    """Generate auto-reply based on message keywords"""
    t = text.lower().strip()
    
    # Greetings
    if any(word in t for word in ["hi", "hello", "hey", "hola", "good morning", "good evening", "sup", "yo"]):
        return f"Hi there!  Welcome to {BRAND_NAME}! How can I help you today?"
    
    # Price inquiries
    if any(word in t for word in ["price", "cost", "how much", "$", "expensive", "cheap", "pricing"]):
        return "Great question!  All our prices are shown on each post. Looking for something specific?"
    
    # Shipping & delivery
    if any(word in t for word in ["ship", "delivery", "deliver", "arrive", "tracking", "when will", "how long"]):
        return " We ship fast! Most orders arrive in 3-5 business days. Need tracking info?"
    
    # Stock & availability
    if any(word in t for word in ["stock", "available", "in stock", "out of stock", "restock", "sold out"]):
        return "We restock regularly!  Follow us to stay updated. Want me to check a specific item?"
    
    # Returns & refunds
    if any(word in t for word in ["return", "refund", "exchange", "money back", "cancel"]):
        return "No worries!  We have a hassle-free return policy. Share your order number and I'll help!"
    
    # Discounts & promotions
    if any(word in t for word in ["discount", "coupon", "promo", "code", "deal", "sale", "offer"]):
        return "Love a good deal!  Keep an eye on our feed — we drop exclusive promos regularly!"
    
    # Product questions
    if any(word in t for word in ["size", "color", "material", "spec", "detail", "dimension"]):
        return "Good question!  Check the product post for full specs. Which item are you asking about?"
    
    # Order status
    if any(word in t for word in ["order", "purchase", "buy", "bought", "ordered"]):
        return "Thanks for your order!  Check your email for confirmation. Questions about your order?"
    
    # Thanks / gratitude
    if any(word in t for word in ["thank", "thanks", "thx", "ty", "appreciate", "thank you"]):
        return "You're welcome!  Anything else I can help with? I'm here!"
    
    # Quality questions
    if any(word in t for word in ["quality", "good", "worth", "recommend", "review", "rating"]):
        return "All our products are carefully selected!  Check the ratings on each post. Interested in something specific?"
    
    # Payment methods
    if any(word in t for word in ["payment", "pay", "credit card", "paypal", "cash", "venmo"]):
        return "We accept all major payment methods! 💳 Secure checkout. Link in bio!"
    
    # Complaints / issues
    if any(word in t for word in ["problem", "issue", "broken", "damaged", "wrong", "complaint"]):
        return "I'm sorry to hear that! 😟 Let me help fix this. Can you share your order number or more details?"
    
    # Contact / support
    if any(word in t for word in ["contact", "call", "email", "support", "help", "customer service"]):
        return "You've reached the right place! 💬 I'm here to help. What do you need assistance with?"
    
    # Yes/No responses
    if t in ["yes", "yeah", "yep", "yup", "ok", "okay", "sure", "k"]:
        return "Great! How can I assist you further? 😊"
    
    if t in ["no", "nope", "nah", "not really"]:
        return "No problem! Let me know if you change your mind or need anything else. 👍"
    
    # Default response
    return f"Hey! 👋 Thanks for reaching out to {BRAND_NAME}. How can I help you today?"

# ══════════════════════════════════════════════════════════
# SEND DM VIA INSTAGRAM GRAPH API
# ══════════════════════════════════════════════════════════

def send_dm(recipient_id, text):
    """
    Send a DM via Instagram Graph API using Instagram User Access Token
    
    Endpoint: POST https://graph.instagram.com/v24.0/{ig-user-id}/messages
    """
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text[:1000]}  # Instagram 1000 char limit
    }
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f" Sending DM to {recipient_id}...")
        logger.info(f"Endpoint: {MESSAGES_ENDPOINT}")
        
        response = requests.post(
            MESSAGES_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            msg_id = result.get('message_id', 'unknown')
            logger.info(f" Reply sent successfully! (msg_id: {msg_id})")
            stats["total_sent"] += 1
            return True
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', response.text)
            error_code = error_data.get('error', {}).get('code', 'unknown')
            logger.error(f" Send failed ({response.status_code}, code: {error_code}): {error_msg}")
            stats["total_errors"] += 1
            return False
    
    except Exception as e:
        logger.error(f" Send error: {e}")
        import traceback
        traceback.print_exc()
        stats["total_errors"] += 1
        return False

# ══════════════════════════════════════════════════════════
# STATS ENDPOINT (JSON)
# ══════════════════════════════════════════════════════════

@app.route("/stats")
def get_stats():
    """Return statistics as JSON"""
    uptime = (datetime.now() - datetime.fromisoformat(stats['start_time'])).total_seconds()
    
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": uptime,
        "config": {
            "ig_id": IG_ID,
            "brand": BRAND_NAME,
            "api_version": "v24.0",
            "token_type": "Instagram User Access Token"
        },
        "stats": stats,
        "conversations": len(conversation_history),
        "messages_processed": len(processed_messages),
        "recent_conversations": conversation_history[-5:]  # Last 5
    })

# ══════════════════════════════════════════════════════════
# TEST PAGE
# ══════════════════════════════════════════════════════════

@app.route("/test")
def test_page():
    """Interactive test page"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Auto DM</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ 
                font-family: Arial; 
                max-width: 900px; 
                margin: 50px auto; 
                padding: 20px; 
                background: #fafafa; 
            }}
            h1 {{ color: #E1306C; text-align: center; }}
            .container {{ 
                background: white; 
                padding: 30px; 
                border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            }}
            .test-section {{ 
                margin: 20px 0; 
                padding: 15px; 
                background: #fceff5; 
                border-left: 4px solid #E1306C; 
                border-radius: 5px; 
            }}
            button {{ 
                background: #E1306C; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 5px; 
                cursor: pointer; 
                margin: 5px; 
                font-size: 14px; 
            }}
            button:hover {{ background: #c13584; }}
            button:active {{ transform: scale(0.98); }}
            .result {{ 
                margin-top: 15px; 
                padding: 15px; 
                border-radius: 5px; 
                display: none; 
            }}
            .result.show {{ display: block; }}
            .result.success {{ background: #d4edda; color: #155724; }}
            .result.error {{ background: #f8d7da; color: #721c24; }}
            input {{ 
                width: 70%; 
                padding: 10px; 
                border: 1px solid #ddd; 
                border-radius: 5px; 
            }}
            .test-msg {{ 
                background: #fff; 
                padding: 10px; 
                border-radius: 5px; 
                margin: 10px 0; 
                font-style: italic; 
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 Test Instagram Auto DM</h1>
            <p style="text-align: center; color: #666;">
                Simulate incoming messages and see auto-replies in your terminal
            </p>
            
            <div class="test-section">
                <h2>Quick Tests</h2>
                
                <div style="margin: 20px 0;">
                    <h3>👋 Greeting</h3>
                    <div class="test-msg">"Hi there!"</div>
                    <button onclick="test('Hi there!')">Send Test</button>
                    <div id="result-1" class="result"></div>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3>💰 Price Inquiry</h3>
                    <div class="test-msg">"How much does this cost?"</div>
                    <button onclick="test('How much does this cost?')">Send Test</button>
                    <div id="result-2" class="result"></div>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3>📦 Shipping Question</h3>
                    <div class="test-msg">"When will my order ship?"</div>
                    <button onclick="test('When will my order ship?')">Send Test</button>
                    <div id="result-3" class="result"></div>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3>🏷️ Discount Request</h3>
                    <div class="test-msg">"Any discount codes?"</div>
                    <button onclick="test('Any discount codes?')">Send Test</button>
                    <div id="result-4" class="result"></div>
                </div>
            </div>
            
            <div class="test-section">
                <h2>💬 Custom Message Test</h2>
                <p>Type any message to see the auto-response:</p>
                <input type="text" id="custom" placeholder="Type your test message here..." />
                <button onclick="testCustom()">Send Custom Test</button>
                <div id="result-custom" class="result"></div>
            </div>
            
            <div class="test-section">
                <h2>📊 Live Stats</h2>
                <button onclick="loadStats()">Refresh Statistics</button>
                <div id="stats-display" style="margin-top: 15px;"></div>
            </div>
        </div>
        
        <script>
            let resultCounter = 1;
            
            function test(msg) {{
                const resultId = 'result-' + resultCounter;
                const resultDiv = document.getElementById(resultId);
                if (!resultDiv) return;
                
                resultDiv.className = 'result';
                resultDiv.innerHTML = '⏳ Sending...';
                resultDiv.classList.add('show');
                
                const event = {{
                    object: "instagram",
                    entry: [{{
                        id: "{IG_ID}",
                        time: Math.floor(Date.now() / 1000),
                        messaging: [{{
                            sender: {{ id: "test_" + Date.now() }},
                            recipient: {{ id: "{IG_ID}" }},
                            timestamp: Math.floor(Date.now() / 1000),
                            message: {{
                                mid: "mid.test_" + Date.now(),
                                text: msg
                            }}
                        }}]
                    }}]
                }};
                
                fetch('/webhook', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(event)
                }})
                .then(r => r.json())
                .then(data => {{
                    resultDiv.className = 'result show success';
                    resultDiv.innerHTML = '✅ Test sent successfully!<br>' +
                                        '<strong>Message:</strong> "' + msg + '"<br>' +
                                        '<em>Check your server terminal to see the auto-reply generated.</em>';
                }})
                .catch(err => {{
                    resultDiv.className = 'result show error';
                    resultDiv.innerHTML = '❌ Error: ' + err;
                }});
            }}
            
            function testCustom() {{
                const msg = document.getElementById('custom').value.trim();
                const resultDiv = document.getElementById('result-custom');
                
                if (!msg) {{
                    resultDiv.className = 'result show error';
                    resultDiv.innerHTML = ' Please enter a message';
                    return;
                }}
                
                resultDiv.className = 'result';
                resultDiv.innerHTML = ' Sending...';
                resultDiv.classList.add('show');
                
                const event = {{
                    object: "instagram",
                    entry: [{{
                        id: "{IG_ID}",
                        messaging: [{{
                            sender: {{ id: "custom_test_" + Date.now() }},
                            recipient: {{ id: "{IG_ID}" }},
                            message: {{
                                mid: "mid.custom_" + Date.now(),
                                text: msg
                            }}
                        }}]
                    }}]
                }};
                
                fetch('/webhook', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(event)
                }})
                .then(r => r.json())
                .then(data => {{
                    resultDiv.className = 'result show success';
                    resultDiv.innerHTML = ' Custom test sent!<br>' +
                                        '<strong>Your message:</strong> "' + msg + '"<br>' +
                                        '<em>Check your server terminal to see the auto-reply.</em>';
                }})
                .catch(err => {{
                    resultDiv.className = 'result show error';
                    resultDiv.innerHTML = ' Error: ' + err;
                }});
            }}
            
            function loadStats() {{
                fetch('/stats')
                    .then(r => r.json())
                    .then(data => {{
                        document.getElementById('stats-display').innerHTML = 
                            '<div style="background: white; padding: 15px; border-radius: 5px;">' +
                            '<strong>Messages Received:</strong> ' + data.stats.total_received + '<br>' +
                            '<strong>Replies Sent:</strong> ' + data.stats.total_sent + '<br>' +
                            '<strong>Errors:</strong> ' + data.stats.total_errors + '<br>' +
                            '<strong>Conversations:</strong> ' + data.conversations + '<br>' +
                            '<strong>Uptime:</strong> ' + data.uptime_seconds.toFixed(0) + ' seconds' +
                            '</div>';
                    }})
                    .catch(err => {{
                        console.error('Error loading stats:', err);
                    }});
            }}
            
            // Load stats on page load
            loadStats();
        </script>
    </body>
    </html>
    """

# ══════════════════════════════════════════════════════════
# RUN SERVER
# ══════════════════════════════════════════════════════════

if __name__ == '__main__':
    logger.info("="*60)
    logger.info(" INSTAGRAM AUTO DM WEBHOOK SERVER (PRODUCTION)")
    logger.info("="*60)
    logger.info(f"Brand:            {BRAND_NAME}")
    logger.info(f"Instagram ID:     {IG_ID}")
    logger.info(f"Token Type:       Instagram User Access Token (IGAA...)")
    logger.info(f"API Version:      v24.0")
    logger.info(f"Messages API:     {MESSAGES_ENDPOINT}")
    logger.info(f"Verify Token:     {WEBHOOK_VERIFY_TOKEN}")
    logger.info("="*60)
    logger.info("\n Server starting on port 5000...")
    logger.info(" This server runs independently of your Jupyter notebook")
    logger.info(" It will respond to DMs in real-time 24/7")
    logger.info("\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)  # Set debug=False for production
