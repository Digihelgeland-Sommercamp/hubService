from flask import Flask, request, jsonify
from requests.models import Response
from werkzeug.exceptions import HTTPException, InternalServerError, BadRequest
import waitress

from classFolder.application import Application
from classFolder.fetchApplication import FetchApplication
from classFolder.submitApplication import SubmitApplication
from classFolder.fetchChildren import FetchChildren
from classFolder.fetchPartner import FetchPartner
from classFolder.fetchApplicant import FetchApplicant
from classFolder.fetchApplicationStatus import FetchApplicationStatus
from classFolder.setApplicationStatus import SetApplicationStatus
from classFolder.uploadAttachment import UploadAttachment

app = Flask(__name__)


@app.route("/")
def root():
    return "Root Route!"


@app.route("/submit_application", methods=["POST"])
def submit_application():
    sub_application = SubmitApplication(request.get_json())
    saksnummer = sub_application.handle_application()
    res = {
        "saksnummer": saksnummer
    }
    del sub_application
    if not res:
        raise InternalServerError
    return jsonify(res)


@app.route("/get_application/<saksnummer>")
def get_application(saksnummer=None):
    fetch_application = FetchApplication(saksnummer)
    res = fetch_application.fetch_application_from_expose_user()
    del fetch_application
    if res == None:
        raise BadRequest
    return jsonify(res)


@app.route("/get_application_status/<saksnummer>")
def get_application_status(saksnummer=None):
    fetch_application_status = FetchApplicationStatus(saksnummer)
    res = fetch_application_status.fetch_application_status_from_expose_user()
    del fetch_application_status
    if res == None:
        raise BadRequest
    return jsonify(res)


@app.route("/set_application_status/<saksnummer>", methods=["POST"])
def set_application_status(saksnummer=None):
    data = request.get_json()
    if 'status' not in data.keys():
        raise BadRequest("Missing status key in json")
    set_application_status = SetApplicationStatus(saksnummer, data['status'])
    res = set_application_status.set_application_status()
    return jsonify(res)

#TODO: Add a filter for children returned, currently all children are returned
@app.route("/get_children/<personidentifikator>")
def get_children(personidentifikator):
    res = FetchChildren().get_related_children(personidentifikator)
    if res is None:
        raise BadRequest
    return jsonify(res)

#TODO: route get partner til frontend
@app.route("/get_partner/<personidentifikator>")
def get_partner(personidentifikator):
    res = FetchPartner().get_partner(personidentifikator)
    if res is None:
        raise BadRequest
    return jsonify(res)


@app.route("/get_applicant/<personidentifikator>")
def get_applicant(personidentifikator):
    res = FetchApplicant().get_applicant_data(personidentifikator)
    if res is None:
        raise BadRequest
    return jsonify(res)


@app.route("/add_attachment", methods=["POST"])
def add_attachment():
    data = request.files
    uploader = UploadAttachment(data)
    res = uploader.upload_attachment()
    return jsonify(res)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)