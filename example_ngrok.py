"""
Example: Using pyngrok to expose Flask to Internet
"""
from flask import Flask
from pyngrok import ngrok

app = Flask(__name__)

# Your Flask routes here...

if __name__ == '__main__':
    # Open ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f"\n🌍 Public URL: {public_url}")
    print(f"   Share this URL with anyone!\n")
    
    # Run Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
