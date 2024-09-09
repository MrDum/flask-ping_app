from flask import Flask, request, render_template
import subprocess
import netaddr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/ping', methods=['POST'])
def ping():
    ip_address = request.form.get('ip_address')
    
    if not ip_address:
        return render_template('error.html', message="IP address is required")

    try:
        netaddr.IPAddress(ip_address)
    except netaddr.AddrFormatError:
        return render_template('error.html', message="Invalid IP address")

    try:
        result = subprocess.run(['ping', '-c', '3', ip_address], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True)
        result.check_returncode()

        lines = result.stdout.splitlines()
        formatted_output = "\n".join(lines[2:])  # Include header lines
    except subprocess.CalledProcessError as e:
        return render_template('error.html', message=f"Ping failed: {e.stderr}")

    return render_template('ping.html', result=formatted_output)

if __name__ == '__main__':
    app.run(debug=True)
