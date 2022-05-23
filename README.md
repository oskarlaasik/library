# library
simple crowdsourced library app


Build the image:
```
$ docker-compose build
```

Once the image is built, run the container:
```
$ docker-compose up -d
```

Mock data can be generated
```
docker exec library_library_1 python mock_data_generator.py
```
