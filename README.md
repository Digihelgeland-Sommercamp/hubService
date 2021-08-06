# Hub Service

Hub service is intended to be a communication layer between the front and back-end.
It is coupled with the following microservices:
* [Expose user](https://github.com/Digihelgeland-Sommercamp/exposeUser)
* [Skatteetaten](https://github.com/Digihelgeland-Sommercamp/skatteservice)
* [Folkeregisteret](https://github.com/Digihelgeland-Sommercamp/fregService)
* [Evaluator](https://github.com/Digihelgeland-Sommercamp/evaluator)

##API
Every route can be found in [app.py](https://github.com/Digihelgeland-Sommercamp/hubService/blob/main/app.py)
Each [GET] route below links to the return of the request, while [POST] links to an example body that should be sent.

* [POST] [/submit_application]()
  * Returns the "saksnummer" of the application
* [POST] [/add_attachment]()
* [GET] [/get_application/\<saksnummer>]()
* [GET] [/get_all_applications/\<personidentifikator>]()
* [GET] [/get_application_status/\<saksnummer>]()
* [GET] [/set_application_status/\<saksnummer>]()
* [GET] [/get_children/\<personidentifikator>]()
* [GET] [/get_partner/\<personidentifikator>]()
* [GET] [/get_applicant/\<personidentifikator>]()

###Installation
This service is intended to run in a kubernetes cluster with the micro services it is coupled with, mentioned at the top of this document. It makes no sense for this service to run alone.
The intention is to only expose this service with a public IP, but this is not mandatory.

Update [config.py](https://github.com/Digihelgeland-Sommercamp/hubService/blob/main/classFolder/config.py) to reflect the hostnames and ports of the other services.

You can use the [deployment.yaml](https://github.com/Digihelgeland-Sommercamp/hubService/blob/main/deployment.yaml) to create a deployment in kubernetes, and [service.yaml](https://github.com/Digihelgeland-Sommercamp/hubService/blob/main/service.yaml) to create a service.

[The latest docker image can be found here](https://hub.docker.com/repository/docker/johannesdigdir/hub_service)

###Architecture

![alt text](https://github.com/Altinn/summer-camp-2021/blob/main/Documentation/Architecture/Microservice%20overview.png "Picture of the architecture and coupling of the services")