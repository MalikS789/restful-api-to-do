from flask import Blueprint, request, jsonify
from .models import Task
from . import db
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    } for task in tasks]), 200


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }), 200


@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()
    data = request.json

    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        completed=data.get('completed', False),
        user_id=current_user_id
    )

    if (data['title'] == ''):
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }), 400
    else:
        db.session.add(new_task)
        db.session.commit()
        jsonify({
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        }), 201


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()

    if (task.title == ''):
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }), 400
    else:
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }), 200


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"}), 200
