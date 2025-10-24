from flask import Flask, request, abort
import os
import subprocess
import glob
import hmac
import hashlib

app = Flask(__name__)

GITHUB_SECRET = os.getenv("GITHUB_SECRET", "")


def verify_github_signature(payload, signature):
    if not GITHUB_SECRET:
        return False
    if not signature:
        return False

    sha_name, signature = signature.split("=")
    if sha_name != "sha256":
        return False

    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Hub-Signature-256")
    payload = request.data

    if not verify_github_signature(payload, signature):
        abort(403, "Invalid signature")

    try:
        deploy_dir = "/app/Deploy"
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
