from flask import Flask, request, abort
import os
import subprocess
import glob
import hmac
import hashlib

app = Flask(__name__)


@app.route("/thB2B22uit/webhook", methods=["POST"])
def webhook():
    try:
        deploy_dir = "./Deploy"
        sh_files = sorted(glob.glob(os.path.join(deploy_dir, "*.sh")))

        if not sh_files:
            return "No .sh files found in Deploy directory", 404

        for script in sh_files:
            subprocess.run(["chmod", "+x", script])
            subprocess.run(["/bin/bash", script], check=True)

        return "All deploy scripts executed successfully!", 200

    except subprocess.CalledProcessError as e:
        return f"Error executing script: {e}", 500
    except Exception as e:
        return f"Unexpected error: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7787)
