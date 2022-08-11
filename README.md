# g42_assignment

#### Build docker image
docker build -t g42-app .

#### RUN app container with host network
```bash
docker run -d --network=host -e URL=192.168.0.201 -e INDEX_NAME='cities' g42_app
```
