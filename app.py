import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 🔑 TELEGRAM SECURITY CONFIGURATION (VERIFIED)
TELEGRAM_BOT_TOKEN = "8996971871:AAFzlNUHwrsERTh8qROZumnlYjNN0WnKvQ4"
TELEGRAM_CHAT_ID = "8162053627"

if not os.path.exists('templates'):
    os.makedirs('templates')

@app.route('/')
@app.route('/admission')
def admission_portal():
    return render_template('admission_form.html')

@app.route('/submit-admission', methods=['POST'])
def submit_admission():
    name = request.form.get('student_name')
    father = request.form.get('father_name')
    phone = request.form.get('mobile_number')
    address = request.form.get('address')
    preparing = request.form.get('preparing_for')
    fee_date = request.form.get('fee_date') # Fees ki tarikh read karne ke liye
    
    photo_file = request.files.get('student_photo')
    
    alert_text = (
        "👑 **RADHA KRISHN LIBRARY — NEW ADMISSION** 👑\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Student Name:** {name}\n"
        f"👴 **Father's Name:** {father}\n"
        f"📞 **Mobile Number:** {phone}\n"
        f"📍 **Complete Address:** {address}\n"
        f"🎯 **Preparing For:** {preparing}\n"
        f"💰 **Fee Promise Date:** {fee_date}\n" # Telegram par show hone ke liye
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ *Dispatched via Secure Background Server*"
    )
    
    try:
        if photo_file:
            files = {'photo': (photo_file.filename, photo_file.stream, photo_file.mimetype)}
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'caption': alert_text, 'parse_mode': 'Markdown'}
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto", data=payload, files=files)
        else:
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': alert_text, 'parse_mode': 'Markdown'}
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=payload)
    except Exception:
        pass
        
    return """
    <body style="background-color: #0b0b0b; color: #f5f5f5; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center;">
        <div style="border: 1px solid #b89734; padding: 30px; border-radius: 10px; background-color: #141414; box-shadow: 0 4px 20px rgba(184, 151, 52, 0.2);">
            <h1 style="color: #b89734; margin-bottom: 15px;">🎉 Admission Form Submitted!</h1>
            <p style="color: #888;">Your details and photo have been successfully recorded. You can close this page now.</p>
        </div>
    </body>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
