from flask import Flask, request, jsonify
import vercel_wsgi  

app = Flask(__name__)

def perform_calculation(operation, num1, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "sub":
        return num1 - num2
    elif operation == "mul":
        return num1 * num2
    elif operation == "div":
        if num2 == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return num1 / num2
    elif operation == "pow":
        return num1 ** num2
    elif operation == "mod":
        if num2 == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return num1 % num2
    else:
        raise ValueError("Invalid operation")

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data:
        response = jsonify({
            "operation": None,
            "num1": None,
            "num2": None,
            "success": False,
            "message": "Invalid JSON payload"
        })
        response.status_code = 418
        return response

    operation = data.get("operation")
    num1 = data.get("num1")
    num2 = data.get("num2")

    if not operation or not isinstance(operation, str):
        response = jsonify({
            "operation": None,
            "num1": num1,
            "num2": num2,
            "success": False,
            "message": "Missing or invalid operation"
        })
        response.status_code = 418
        return response

    try:
        num1 = float(num1)
        num2 = float(num2)
    except (TypeError, ValueError):
        response = jsonify({
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "success": False,
            "message": "Missing or invalid numbers (must be numeric values)"
        })
        response.status_code = 418
        return response

    try:
        result = perform_calculation(operation, num1, num2)
        return jsonify({
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "result": result,
            "success": True
        })
    except ZeroDivisionError as zde:
        response = jsonify({
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "success": False,
            "message": str(zde)
        })
        response.status_code = 418
        return response
    except Exception as e:
        response = jsonify({
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "success": False,
            "message": str(e)
        })
        response.status_code = 418
        return response

handler = vercel_wsgi.handler(app)
