# g42_assignment

#### Build docker image
```bash
docker build -t g42_app .
```

#### RUN app container with host network
```bash
docker run -d --network=host -e URL=192.168.0.201 -e INDEX_NAME='cities' g42_app
```

## Deploy the app
The helm chart of app1 and elasticsearch have deployed and tested in minikube cluster 1.23.0.

The cli to deploy helm charts are given in helm-charts directory. Read README.md file

## Access the app


#### Get all cities details
```bash
curl --location --request GET 'http://192.168.59.103:30007/citydetails'
```


#### Update population of a city if not exist then create new entry
```bash
curl --location --request POST 'http://192.168.59.103:30007/citymodify' \
--header 'Content-Type: application/json' \
--data-raw '{
    "city": "delhi",
    "population": 15500000
}'
```

Note: The app service exposed on nodeport hence it may change in your case 

`http://192.168.59.103:30007` will be replaced with your `http://<node_ip>:<app1_svc_node_port>`

Get the node ip:- `kubectl get pod -o wide`

Get the svc port:- `kubectl get svc`
