from ultralytics import YOLO
from flask import request, Flask, jsonify
from waitress import serve
from PIL import Image
import json

app = Flask(__name__)

@app.route("/")
def root():
    try:
        with open("index.html") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: File 'index.html' not found."
    except IOError as e:
        return f"Error reading 'index.html': {e}"

@app.route("/detect", methods=["POST"])

def predict_image():
    try:   
        if predict_image_scenario():
            pass
        buf = request.files["image_file"]
        results, output_dict = detect_objects_on_image(buf.stream)
        print_result(results, output_dict)
        return jsonify(output_dict)
        
    except Exception as jsonify_error:
        return jsonify({'error': f'Error creating JSON response: {str(jsonify_error)}'})

def predict_image_scenario():
    try:
        scenario = request.form.get('scenario')
        if not scenario:
            print("\nerror: Scenario not provided")
        else:
            print("\nsuccess: Scenario provided")

        scenarios(scenario)
        
    except ValueError as e:
        return jsonify({'error': str(e)})

def detect_objects_on_image_predict(buf_scenario):
    try:
        model = YOLO("best09.pt")
    except Exception as model_error:
        print(f'Error loading model: [{str(model_error)}]')
        return jsonify({'error': 'Error loading model'})
    
    try:
        image = Image.open(buf_scenario)
    except (ValueError, IOError, OSError) as image_error:
        print(f'Error loading image: [{str(image_error)}]')
        return jsonify({'error': 'Error loading image'})

    try:
        results = model.predict(image)
    except Exception as detection_error:
        print(f'Error during object detection: [{str(detection_error)}]')
        return jsonify({'error': 'Error during object detection'})

    output_dict = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)

        cm_coordinates = {
            "x1": round((x1 / 96) * 2.54, 3),
            "y1": round((y1 / 96) * 2.54, 3),
            "x2": round((x2 / 96) * 2.54, 3),
            "y2": round((y2 / 96) * 2.54, 3),
        }

        output_dict.append({
            "etiqueta": results[0].names[class_id],
            "confianza": prob,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "cm": cm_coordinates,
        })

    return results, output_dict

def detect_objects_on_image(buf):
    try:
        model = YOLO("best09.pt")
    except Exception as model_error:
        print(f'Error loading model: [{str(model_error)}]')
        return jsonify({'error': 'Error loading model'})
    
    try:
        image = Image.open(buf)
    except (ValueError, IOError, OSError) as image_error:
        print(f'Error loading image: [{str(image_error)}]')
        return jsonify({'error': 'Error loading image'})

    try:
        results = model.predict(image)
    except Exception as detection_error:
        print(f'Error during object detection: [{str(detection_error)}]')
        return jsonify({'error': 'Error during object detection'})

    output_dict = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)

        cm_coordinates = {
            "x1": round((x1 / 96) * 2.54, 3),
            "y1": round((y1 / 96) * 2.54, 3),
            "x2": round((x2 / 96) * 2.54, 3),
            "y2": round((y2 / 96) * 2.54, 3),
        }

        output_dict.append({
            "etiqueta": results[0].names[class_id],
            "confianza": prob,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "cm": cm_coordinates,
        })

    return results, output_dict

def print_result(results, output_dict):
    print("\nCategories detected in the image:")
    for item in zip(results[0].boxes, output_dict):
        box, json_obj = item

        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)

        ppi = 96
        cm_coordinates = {
            "x1": round((x1 / ppi) * 2.54, 3),
            "y1": round((y1 / ppi) * 2.54, 3),
            "x2": round((x2 / ppi) * 2.54, 3),
            "y2": round((y2 / ppi) * 2.54, 3),
        }

        json_obj.update({
            "cm": cm_coordinates,
            "confianza": prob,
            "etiqueta": results[0].names[class_id],
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
        })

        print(json.dumps(json_obj, indent=4))

def scenarios(scenario):
    if scenario in ['A', 'B', 'C']:
        print(f'\nscenario: {scenario}')
    else:
        pass

if __name__ == "__main__":
    print("Connect to http://localhost:8080")
    print("Press Ctrl-c to quit.")
    serve(app, host='0.0.0.0', port=8080)
