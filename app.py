import zipfile

from flask import Flask, render_template, request, Response
# from flask import Flask, request, Response
from PIL import Image
import io

import function_coloring
import function_defog
import function_denoise
import function_onekey
import function_super_resolution

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/superresolution", methods=["GET"])
def superresolution():
    return render_template("superresolution.html")


@app.route("/denoise", methods=["GET"])
def denoise():
    return render_template("denoise.html")


@app.route("/split", methods=["GET"])
def webptopng():
    return render_template("split.html")


@app.route("/defog", methods=["GET"])
def defog():
    return render_template("defog.html")


@app.route("/coloring", methods=["GET"])
def coloring():
    return render_template("coloring.html")


@app.route("/onekey", methods=["GET"])
def onekey():
    return render_template("onekey.html")


@app.route('/api/superresolution', methods=['POST'])
def Super_resolution():
    zip_file = request.files["zip"]
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        result_files = []
        for filename in zip_ref.namelist():
            with zip_ref.open(filename) as image_file:
                image = Image.open(image_file)
                image = image.convert('RGB')
                image_buffer = io.BytesIO()
                image.save(image_buffer, 'JPEG')
                image_buffer = image_buffer.getvalue()
                image_buffer = function_super_resolution.pic_super_resolution(image_buffer)
                result_files.append((filename, image_buffer))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        for filename, image_buffer in result_files:
            zip_ref.writestr(filename, image_buffer)

    response = Response(zip_buffer.getvalue(), content_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=converted.zip"
    return response


@app.route("/api/denoise", methods=["POST"])
def Denoise():
    zip_file = request.files["zip"]
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        result_files = []
        for filename in zip_ref.namelist():
            with zip_ref.open(filename) as image_file:
                image = Image.open(image_file)
                image = image.convert('RGB')
                image_buffer = io.BytesIO()
                image.save(image_buffer, 'JPEG')
                image_buffer = image_buffer.getvalue()
                image_buffer = function_denoise.pic_denoise(image_buffer)
                result_files.append((filename, image_buffer))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        for filename, image_buffer in result_files:
            zip_ref.writestr(filename, image_buffer)

    response = Response(zip_buffer.getvalue(), content_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=converted.zip"
    return response


@app.route("/api/split", methods=["POST"])
def Split():
    return ""


@app.route("/api/defog", methods=["POST"])
def Defog():
    zip_file = request.files["zip"]
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        result_files = []
        for filename in zip_ref.namelist():
            with zip_ref.open(filename) as image_file:
                image = Image.open(image_file)
                image = image.convert('RGB')
                image_buffer = io.BytesIO()
                image.save(image_buffer, 'JPEG')
                image_buffer = image_buffer.getvalue()
                image_buffer = function_defog.pic_defog(image_buffer)
                result_files.append((filename, image_buffer))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        for filename, image_buffer in result_files:
            zip_ref.writestr(filename, image_buffer)

    response = Response(zip_buffer.getvalue(), content_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=converted.zip"
    return response


@app.route("/api/coloring", methods=["POST"])
def Coloring():
    zip_file = request.files["zip"]
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        result_files = []
        for filename in zip_ref.namelist():
            with zip_ref.open(filename) as image_file:
                image = Image.open(image_file)
                image = image.convert('RGB')
                image_buffer = io.BytesIO()
                image.save(image_buffer, 'JPEG')
                image_buffer = image_buffer.getvalue()
                image_buffer = function_coloring.pic_coloring(image_buffer)
                result_files.append((filename, image_buffer))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        for filename, image_buffer in result_files:
            zip_ref.writestr(filename, image_buffer)

    response = Response(zip_buffer.getvalue(), content_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=converted.zip"
    return response


@app.route("/api/onekey", methods=["POST"])
def Onekey():
    zip_file = request.files["zip"]
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        result_files = []
        for filename in zip_ref.namelist():
            with zip_ref.open(filename) as image_file:
                image = Image.open(image_file)
                image = image.convert('RGB')
                image_buffer = io.BytesIO()
                image.save(image_buffer, 'JPEG')
                image_buffer = image_buffer.getvalue()
                rotate = request.form.get("rotate")
                zoom = request.form.get("zoom")
                cut = request.form.get("cut")
                flip = request.form.get("flip")
                color = request.form.get("color")
                noise = request.form.get("noise")
                image_buffer = function_onekey.pic_onekey(image_buffer, rotate, zoom, cut, flip, color, noise)
                result_files.append((filename, image_buffer))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_ref:
        for filename, image_buffer in result_files:
            zip_ref.writestr(filename, image_buffer)

    response = Response(zip_buffer.getvalue(), content_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=converted.zip"
    return response


if __name__ == "__main__":
    app.run(debug=True)
