# Friday Hacks:  Apache Airflow x Kubernetes

## About Friday Hacks

Friday Hacks is an informal event that takes place on most Fridays at 1pm, at the Valuemotive office.

Valuemotive has a culture of sharing interesting ideas. Our employees are curious, which leads to ad hoc exchanges. Folks will test the validity of their ideas, ask for feedback on complicated things and discuss their work with others.

We play with an interesting piece of tech and have a discussion about it with an expert present. We often weight on pros and cons of using the tech at work. We always learn something new! You are looking at a demo/boilerplate/guide that was prepared in advance to support the ’Hack.

Examples of previous Friday Hacks: AWS Lambda + Serverless framework, Apache Airflow, Rust, Elm.

## About this 'Hack

Demo of Airflow (running in Kubernetes cluster with Kubernetes Executor and Kubernetes Operator) with AWS EKS and Helm

# Usage

Reference: 
https://aws.amazon.com/blogs/startups/from-zero-to-eks-with-terraform-and-helm/
https://towardsdatascience.com/kubernetesexecutor-for-airflow-e2155e0f909c

## AWS EKS

To deploy AWS EKS cluster:
```
cd aws-eks/
terraform init
terraform plan
terraform apply
```

To get kubeconfig:
```
terraform output kubeconfig
```

Then, update kubeconfig with above value
```
vi ~/.kube/config
```

To get aws_configmap:
```
terraform output config_map_aws_auth > aws-configmap.yml
kubectl apply -f aws-configmap.yml
```

## Helm

Install helm: https://github.com/helm/helm/blob/master/docs/install.md
```
kubectl apply -f tiller-user.yaml
helm init --service-account tiller
```

Example helm charts:
```
helm install stable/nginx-ingress --name nginx-ingress --set rbac.create=true
helm install stable/airflow --name airflow -f airflow-values.yaml
```

## Airflow

Note: remember to create PostgreSQL server and provide info in values-k8s.yaml

Build airflow-k8s image:
```
cd airflow-helm/docker
./build-docker.sh
docker tag airflow:latest <docker-registry>/airflow-k8s:latest
docker push <docker-registry>/airflow-k8s:latest
```

To install airflow chart:
```
cd airflow-helm/airflow
helm upgrade --install airflow ./ -f values.yaml -f values-k8s.yaml
```

To access airflow-web UI:
```
kubectl port-forward $(kubectl get pod --selector="app=airflow-web,release=airflow" --output jsonpath='{.items[0].metadata.name}') 8080:8080
```

## Cleaning up

helm del --purge airflow
terraform destroy

Note: remember to take down Database resource also if that is set up on cloud
