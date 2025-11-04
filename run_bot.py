import multiprocessing
import subprocess
import time
import os

def run_telegram_bot():
    subprocess.run(["python", "main.py"])

def run_web_server():
    subprocess.run(["python", "web_server.py"])

if __name__ == "__main__":
    print("🚀 Starting Telegram Bot and Web Server...")
    
    bot_process = multiprocessing.Process(target=run_telegram_bot)
    web_process = multiprocessing.Process(target=run_web_server)
    
    web_process.start()
    time.sleep(2)
    bot_process.start()
    
    domain = os.getenv('RENDER_URL', 'localhost:5000')
    
    print("✅ Both services started!")
    print("🌐 Web Server: https://" + domain)
    print("📱 Telegram Bot: Running")
    
    try:
        bot_process.join()
        web_process.join()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        bot_process.terminate()
        web_process.terminate()
        bot_process.join()
        web_process.join()
        print("✅ Services stopped")
