[![Build Status](https://gitlab.com/canyan/rating-api/badges/master/pipeline.svg)](https://gitlab.com/canyan/rating-api/pipelines) [![codecov](https://codecov.io/gh/canyanio/rating-api/branch/master/graph/badge.svg)](https://codecov.io/gh/canyanio/rating-api) [![Docker pulls](https://img.shields.io/docker/pulls/canyan/rating-api.svg?maxAge=3600)](https://hub.docker.com/repository/docker/canyan/rating-api)

# Canyan Rating: API

Canyan Rating is an open source real-time highly scalable rating system. It is composed of an Agent Service, an API, and a Rating Engine.

The rating system is a critical component in any business, especially when real-time features are a strict requirement to ensure business continuity and congruence of transactions. Any compromise to availability, integrity, and authentication in the billing system makes a huge impact on the services provided.

Canyan aims to address these challenges with a cloud-native scalable solution, easily deployable and easily usable. It has been designed to work atomically ensuring the system status is always consistent, reproducible and coherent. Asynchronous processing of no real-time, consolidation events, prioritization, and time-boxed tasks provide the basics to ensure lightning-fast transaction processing without compromises.

Ease of use is addressed with comprehensive documentation, examples and high-quality software (see the test coverage badge).

Canyan Rating is designed as a microservice architecture and comprises [several repositories](https://github.com/canyanio). Its components are stateless and easily deployable via containers on-premises or in the cloud. This repository contains the Canyan Rating API. 

![Canyan logo](https://canyanio.github.io/rating-integration/canyan-logo.png) 


## Getting started

To start using Canyan Rating, we recommend that you begin with the Getting started
section in [the Canyan Rating documentation](https://canyanio.github.io/rating-integration/).


## Contributing

We welcome and ask for your contribution. If you would like to contribute to Canyan Rating, please read our guide on how to best get started [contributing code or documentation](https://canyanio.github.io/rating-integration/contributing/).

## License

Canyan is licensed under the GNU General Public License version 3. See
[LICENSE](https://canyanio.github.io/rating-integration/license/) for the full license text.

## Security disclosure

We take Canyan's security and our users trust very seriously.
If you believe you have found a security issue in Canyan, please responsibly
disclose by contacting us at [security@canyan.io](mailto:security@canyan.io).

## Running

### Requirements
Canyan Rating API depends on MongoDB and RabbitMQ. You can easily run them via the provided [docker-compose](docker-compose.yaml) file with:
```
docker-compose up -d
```
If you're not familiar with docker-compose read [the documentation](https://docs.docker.com/compose/) on the official docker website.
You can also install and run MondoDB and RabbitMQ as local services.

### Running with the docker image
The Rating API is available at [docker hub](https://hub.docker.com/repository/docker/canyan/rating-api) and can be easily run with the following command:
```
docker run -d -p 8000:8000 canyan/rating-api:master rating-api -h 0.0.0.0 -p 8000
```

### Running from source
If you want to run the API locally you need to create a Python3 virtual environment with:
```
make venv
```

Then install the [requirements](requirements.txt):
```
source venv/bin/activate
make setup
```

You need to have MongoDB and RabbitMQ now running and then you can run the API with:
```
make api
```

## Connect with us

* Follow us on [Twitter](https://twitter.com/canyan_io). Please
  feel free to tweet us questions.
* Connect with us on [LinkedIN](https://www.linkedin.com/company/canyan/).
* Join us on [Slack](http://slack.canyan.io)
* Fork us on [Github](https://github.com/canyanio)
* Email us at [info@canyan.io](mailto:info@canyan.io)
