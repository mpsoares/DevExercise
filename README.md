# DevExercise
# DevExercise

This README provides instructions on how to clone and run the DevExercise application using different deployment methods.

## Cloning the Repository

To get started, clone the repository using the following command:

```bash
git clone https://github.com/mpsoares/devexercise.git
```

## Prerequisites

Before running the application, ensure you have the following prerequisites installed:

- Docker
- Docker Compose
- Kubernetes


## Running the Application

### Choose one of the following methods to run the application

### Using Docker Compose

Navigate to the `Docker` directory and run the following command to start the application:

```bash
docker-compose up -d
```
This will spin up a container with a MongoDB instance and the python application.
You can access the application at http://localhost:8000
To register a product, you can use the following curl command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"description": "Product Description", "price": 100, "categories": ["Category1", "Category2"]}' http://localhost:8000/register_product
```
Copy the product id from the response and use it to retrieve the product details with the following curl command:

```bash
curl http://localhost:8000/product/$product_id
```


### Using Kubernetes

Navigate to the `k8s` directory and run the following command to start the application:

```bash
kubectl apply -f deployment.yaml
```

This will spin up a pod with a MongoDB instance and the python application.
port forward the service to access the application at http://localhost:8000 (reference: https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)

To register a product, you can use the following curl command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"description": "Product Description", "price": 100, "categories": ["Category1", "Category2"]}' http://localhost:8000/register_product
``` 

Copy the product id from the response and use it to retrieve the product details with the following curl command:

```bash
curl http://localhost:8000/product/$product_id
```

### A few Improvements to do if this was a real application:
- implement authentication
- implement authorization
- implement logging
- implement monitoring
- implement feature flags
- implement error handling
- implement data validation




