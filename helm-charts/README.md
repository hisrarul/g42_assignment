## Deploy in k8s using helm chart

#### Deploy elasticsearch helm chart
```bash
helm upgrade --install elasticsearch elasticsearch -f elasticsearch/values.yaml
```

#### Deploy app1 helm chart
```bash
helm upgrade --install app1 app1 -f app1/values.yaml
```
