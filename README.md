# feniks_ato


## Local development using docker
It is possible to build and run the docker image locally. Check the official docker documentation for more info on how to install docker(compose).

([Docker installation instructions](https://docs.docker.com/compose/install/))

This project should by run with a .env file in the directory, containing the url of the google sheet:

```yml
GOOGLESHEETS_URL='<my_super_secret_url>'
DOMAINNAME_CLOUD_SERVER=yourdomain.com
```

From the terminal run:
``` sh
docker-compose up -d --build
```

The app can be acces on http://0.0.0.0:88 aka http://localhost:88