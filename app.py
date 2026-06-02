from flask import Flask, jsonify, request
from datetime import datetime
import os
import uuid

app = Flask(__name__)

# In-memory store (replace with a real DB in production)
tasks = {}

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV     = os.getenv("APP_ENV", "development")
PORT        = int(os.getenv("PORT", 5000))


# ── Health & Info ──────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Liveness probe."""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}), 200


@app.route("/ready", methods=["GET"])
def ready():
    """Readiness probe."""
    return jsonify({"status": "ready"}), 200


@app.route("/info", methods=["GET"])
def info():
    """App metadata — useful for verifying deployments."""
    return jsonify({
        "app": "task-manager",
        "version": APP_VERSION,
        "environment": APP_ENV,
    }), 200


# ── Tasks CRUD ─────────────────────────────────────────────────────────────────

@app.route("/tasks", methods=["GET"])
def list_tasks():
    status = request.args.get("status")  # ?status=pending|done
    result = list(tasks.values())
    if status:
        result = [t for t in result if t["status"] == status]
    return jsonify({"tasks": result, "count": len(result)}), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    body = request.get_json(silent=True) or {}
    title = body.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    task = {
        "id":          str(uuid.uuid4()),
        "title":       title,
        "description": body.get("description", ""),
        "status":      "pending",
        "priority":    body.get("priority", "medium"),   # low | medium | high
        "created_at":  datetime.utcnow().isoformat(),
        "updated_at":  datetime.utcnow().isoformat(),
    }
    tasks[task["id"]] = task
    return jsonify(task), 201


@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task), 200


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404

    body = request.get_json(silent=True) or {}
    for field in ("title", "description", "status", "priority"):
        if field in body:
            task[field] = body[field]
    task["updated_at"] = datetime.utcnow().isoformat()
    return jsonify(task), 200


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404
    del tasks[task_id]
    return jsonify({"message": "task deleted"}), 200


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=(APP_ENV == "development"))
