from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import subprocess
import json
import os

app = Flask(__name__)
app.secret_key = 'AAHzWiN3raclU6Cia4Gwz1y7WNMDCP6obXw'
config_file_path = 'config.json'

def load_config():
    with open(config_file_path, 'r') as file:
        return json.load(file)

def save_config(config):
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        limit = request.form['limit']
        tag_card = request.form['tag_card']
        keyword = request.form['keyword']
        
        command = f"scrapy crawl data_spider -a url={url} -a limit={limit} -a tag_card={tag_card} -a keyword={keyword}"
        
        try:
            subprocess.run(command, shell=True, capture_output=True, text=True)
            return jsonify({'status': 'success'})
        except subprocess.CalledProcessError:
            return jsonify({'status': 'error'})
        
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():

    if request.method == 'POST':
        telegram_bot_token = request.form['telegram_bot_token']
        telegram_chat_id = request.form['telegram_chat_id']
        
        config = {
            "TELEGRAM_BOT_TOKEN": telegram_bot_token,
            "TELEGRAM_CHAT_ID": telegram_chat_id,
        }
        
        save_config(config)
        return jsonify({'status': 'success'})

    config = load_config()
    return render_template('config.html', config=config)

if __name__ == '__main__':
    app.run(debug=False)
