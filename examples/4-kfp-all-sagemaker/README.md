KFP Demo with Mlctl

This example is for demo purposes only. 

Infrastructure Set Up

To get started with a Kubernetes cluster quickly on the cloud, consider using Bitnami's Kubernetes Sandbox.

https://aws.amazon.com/marketplace/pp/prodview-hy5b54ebhfcsm

Install Kubeflow Pipelines using a standalone, self hosted Kubernetes deployment

https://www.kubeflow.org/docs/components/pipelines/installation/standalone-deployment/

The Kubernetes config will need to be copied over to your local environment for using kubectl. Kubectl is installed 

Data and Security Provisions

- Upload data to S3
- Add AWS Secret to kubeflow namespace

Pipeline Instructions

From there run python kfp-test.py