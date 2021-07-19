from flask import Flask, request, jsonify
from requests.models import Response
from werkzeug.exceptions import HTTPException, InternalServerError, BadRequest
import waitress

from classFolder.application import Application
from classFolder.fetchApplication import FetchApplication
from classFolder.submitApplication import SubmitApplication

app = Flask(__name__)


@app.route("/")
def root():
    return "Root Route!"


@app.route("/submit_application", methods=["POST"])
def submit_application():
    sub_application = SubmitApplication(request.get_json())
    res = sub_application.handle_application()
    del sub_application
    if not res:
        raise InternalServerError
    return Response("Success", 200)

@app.route("/get_application/<saksnummer>")
def get_application(saksnummer=None):
    fetch_application = FetchApplication(saksnummer)
    res = fetch_application.fetch_application_from_expose_user()
    del fetch_application
    if res == None:
        raise BadRequest
    return jsonify(res)



if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)