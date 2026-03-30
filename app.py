from flask import Flask, render_template, request, jsonify
from email_sender import send_emails
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send', methods=['POST'])
def send():
    data = request.json
    try:
        host = data.get('host')
        port = int(data.get('port'))
        address = data.get('address')
        password = data.get('password')
        contacts = data.get('contacts')
        template = data.get('template')
        subject = data.get('subject')
        
        if not all([host, port, address, password, contacts, template, subject]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400
            
        success, message = send_emails(
            host=host,
            port=port,
            my_address=address,
            password=password,
            contacts_text=contacts,
            template_text=template,
            subject=subject
        )
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Ensure template and static folders are properly referenced relative to the app file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app.run(debug=True, port=5000)
