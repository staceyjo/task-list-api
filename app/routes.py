from app import db

from flask import Blueprint, jsonify, make_response, request, abort

from app.models.task import Task

# DEFINING THE TASK BLUEPRINT
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task


# ============================= CRUD ROUTES =============================
# CREATE TASK- POST request to /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    # return make_response(f"Task {new_task.title} successfully created", 201)
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": True if new_task.completed_at else False  
    }}, 201
    

# READ ALL TASKS- GET request to /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False 
        })
    return jsonify(tasks_response), 200


# READ ONE TASK- GET request to /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    # task = Task.query.get(task_id)
    task = validate_model(task_id)

    return { "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": True if task.completed_at else False
        }
    }, 200

# UPDATE TASK- PUT request to /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    # return make_response(f"Task #{task.task_id} successfully updated"), 200

    return { "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": True if task.completed_at else False
        }
    }, 200
    
# DELETE TASK- DELETE request to /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_book(task_id):
    task = validate_model(task_id)

    db.session.delete(task)
    db.session.commit()

    # return make_response(f"Task {task.task_id} \"{task.title}\" successfully deleted")
    return { "details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200

    
    