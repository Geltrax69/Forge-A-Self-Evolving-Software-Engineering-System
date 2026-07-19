url: https://docs.docker.com/guides/nodejs/deploy/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Deploy your Node.js application

***

Table of contents

***

## [Prerequisites](#prerequisites)

* Complete all the previous sections of this guide, starting with [Containerize a Node.js application](https://docs.docker.com/guides/nodejs/containerize/).
* [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## [Overview](#overview)

In this section, you'll deploy your containerized Node.js application to a local Kubernetes cluster using Docker Desktop. You'll create a Kubernetes manifest that describes how the application should run, including the application deployment, the PostgreSQL database, and the services that connect them.

## [Create a Kubernetes manifest](#create-a-kubernetes-manifest)

Create a new file called `nodejs-docker-example-kubernetes.yaml` in your project root:

nodejs-docker-example

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nodejs-docker-example

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: nodejs-docker-example
data:
  POSTGRES_SERVER: 'postgres'
  POSTGRES_DB: 'example'
  POSTGRES_USER: 'postgres'

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: nodejs-docker-example
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: nodejs-docker-example
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: dhi.io/postgres:18
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: db-password
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql
          readinessProbe:
            exec:
              command: [pg_isready]
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: nodejs-docker-example
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    app: postgres

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: server
  namespace: nodejs-docker-example
spec:
  replicas: 2
  selector:
    matchLabels:
      app: server
  template:
    metadata:
      labels:
        app: server
    spec:
      containers:
        - name: server
          image: DOCKER_USERNAME/nodejs-docker-example:latest
          ports:
            - containerPort: 3000
          env:
            - name: POSTGRES_SERVER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_SERVER
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: db-password
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: server
  namespace: nodejs-docker-example
spec:
  type: ClusterIP
  ports:
    - port: 3000
      targetPort: 3000
  selector:
    app: server
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir nodejs-docker-example && cd nodejs-docker-example
cat > nodejs-docker-example-kubernetes.yaml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
apiVersion: v1
kind: Namespace
metadata:
  name: nodejs-docker-example

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: nodejs-docker-example
data:
  POSTGRES_SERVER: 'postgres'
  POSTGRES_DB: 'example'
  POSTGRES_USER: 'postgres'

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: nodejs-docker-example
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: nodejs-docker-example
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: dhi.io/postgres:18
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: db-password
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql
          readinessProbe:
            exec:
              command: [pg_isready]
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: nodejs-docker-example
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    app: postgres

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: server
  namespace: nodejs-docker-example
spec:
  replicas: 2
  selector:
    matchLabels:
      app: server
  template:
    metadata:
      labels:
        app: server
    spec:
      containers:
        - name: server
          image: DOCKER_USERNAME/nodejs-docker-example:latest
          ports:
            - containerPort: 3000
          env:
            - name: POSTGRES_SERVER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_SERVER
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: db-password
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: server
  namespace: nodejs-docker-example
spec:
  type: ClusterIP
  ports:
    - port: 3000
      targetPort: 3000
  selector:
    app: server
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
Set-Location nodejs-docker-example
WriteFile 'nodejs-docker-example-kubernetes.yaml' @'
apiVersion: v1
kind: Namespace
metadata:
  name: nodejs-docker-example

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: nodejs-docker-example
data:
  POSTGRES_SERVER: 'postgres'
  POSTGRES_DB: 'example'
  POSTGRES_USER: 'postgres'

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: nodejs-docker-example
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: nodejs-docker-example
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: dhi.io/postgres:18
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: db-password
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql
          readinessProbe:
            exec:
              command: [pg_isready]
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: nodejs-docker-example
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    app: postgres

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: server
  namespace: nodejs-docker-example
spec:
  replicas: 2
  selector:
    matchLabels:
      app: server
  template:
    metadata:
      labels:
        app: server
    spec:
      containers:
        - name: server
          image: DOCKER_USERNAME/nodejs-docker-example:latest
          ports:
            - containerPort: 3000
          env:
            - name: POSTGRES_SERVER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_SERVER
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: db-password
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: server
  namespace: nodejs-docker-example
spec:
  type: ClusterIP
  ports:
    - port: 3000
      targetPort: 3000
  selector:
    app: server
'@
```

Before applying the manifest, replace `DOCKER_USERNAME` in the `server` deployment's image field with your Docker Hub username.

## [Deploy to Kubernetes](#deploy-to-kubernetes)

Apply the manifest to your local Kubernetes cluster:

```console
$ kubectl apply -f nodejs-docker-example-kubernetes.yaml
```

You should see output confirming that the resources were created:

```console
namespace/nodejs-docker-example created
configmap/app-config created
persistentvolumeclaim/postgres-pvc created
deployment.apps/postgres created
service/postgres created
deployment.apps/server created
service/server created
```

Then create the database secret from your password file:

```console
$ kubectl create secret generic app-secrets \
  --namespace nodejs-docker-example \
  --from-file=db-password=db/password.txt
```

## [Verify the deployment](#verify-the-deployment)

Check that your pods are running:

```console
$ kubectl get pods -n nodejs-docker-example
```

Wait until all pods show `Running` in the STATUS column. Then verify your services:

```console
$ kubectl get services -n nodejs-docker-example
```

## [Access the application](#access-the-application)

Use port forwarding to access the application from your local machine:

```console
$ kubectl port-forward -n nodejs-docker-example service/server 3000:3000
```

Open a new terminal and make a request to the application:

```console
$ curl http://localhost:3000
{"message":"Hello World"}
```

You can also create a hero:

```console
$ curl -X POST http://localhost:3000/heroes/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "my hero", "secret_name": "austing", "age": 12}'
```

## [Clean up](#clean-up)

When you're done testing, remove the deployment:

```console
$ kubectl delete -f nodejs-docker-example-kubernetes.yaml
```

## [Summary](#summary)

In this section, you deployed your containerized Node.js application to Kubernetes. You created a manifest that defines the application and database deployments, applied it to a local cluster, and verified the application is accessible.

Related information:

* [Kubernetes documentation](https://kubernetes.io/docs/home/)
* [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
* [`kubectl` CLI reference](https://kubernetes.io/docs/reference/kubectl/)
* [Kubernetes Deployment resource](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* [Kubernetes Service resource](https://kubernetes.io/docs/concepts/services-networking/service/)

----
