### Blue Green Test 



![N|BG](https://media-exp1.licdn.com/dms/image/D5612AQH4QEyK2cgvaw/article-cover_image-shrink_720_1280/0/1662593126144?e=1668643200&v=beta&t=4Dw1RpJyrtlhCvPXeZnT9q-BosSs-DyoJUZwQsz1Hqc)

The purpose of this article is to demonstrate the power of Blue Green Deployments and their value in the software lifecycle. In addition, this serves as a great proof of concept (POC) for this type of deployment.
- Repositories:
- Blue-Green-Application
- Blue-Green-Kubernetes

Blue-Green Deployments allow developers of software to deploy application releases to vm's/microservice in a rollout fashion where the production application is isolate from the development release. This model like canary focus on pushing/testing your applications in a replicated production environment and thus mitigates the risk of pushing directly to production.

In this demonstration we are deploying a simple Nginx webserver image from my Docker Hub (kmgoddard/bgapp), this application is a basic webpage (see image.) As you can see from below I simply change the dot to display which one is the green, which is the blue whenever I make a change to the application.

![N|BG](https://media-exp1.licdn.com/dms/image/D5612AQGE_CNKG2rOrA/article-inline_image-shrink_1500_2232/0/1662594310268?e=1668643200&v=beta&t=XgYybdhGhne5v14CFKuVjWpHf6UZRUlzE-zv9Wek9ss)

![N|BG](https://media-exp1.licdn.com/dms/image/D5612AQGmRyJ1_MTCyA/article-inline_image-shrink_1500_2232/0/1662594339088?e=1668643200&v=beta&t=nRh6tzaZERv78hM0VTqpvqExlLw649sX3u1Gc6fom8Y)

The Kubernetes deployment in this lab is relatively simple, but it it is something you could definitely build on.

### Deployment Breakdown:
#### Replica Set: 3
Each Pod will have 3 nodes in it with a load balancer in front of it, so if you wanted to get fancy you could show the server changes by echoing the host.

#### Networking:
There are two ingress controllers and 2 (MetalLB Load Balancers)
Note: If you are not familiar with load balancers in Kubernetes, the packaged ones are intended for cloud applications, you will never get a public IPv4 on your on-premise setup, so because the lab is on prem I am using MetalLB, awesome product. #MetalLB

#### Docker Image (Nginx web server)
A docker image built with my custom html page, I say custom laughing out loud. Any you get the idea, it is a simple app for testing.
Bash Script

This script looks at the last version, or deployment (blue/green) and then make a decision based on this. (In a live scenario, you would use a parameter on the pipeline)
Tree:



The Kubernetes Deployment above is broken down pretty logically and simple to read and understand. As I said if you wanted to implement this you could apply more security, you could apply vulnerability scans on the image, you will see I have that commented in the Jenkinsfile as I know the source and that process was running a bit slow on my lab. Mind you I have a 1u small Dell Server I am running things on.
Kustomization scripts. (You can learn [Here](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/) that make it simple to deploy and update with

`kubectl apply -k ./` 

Here is a break down of the directory tree for the Kube Deployment.
#### Root Directory:
You have the two ingress controller configurations, a name space configuration.
Note: Name spaces help you manage your Kubernetes Infrastructure with a single command.

##### Service:
Under service are the two load balancers and if you have never used MetalLB for an on prem deployment then check them out [here](https://metallb.universe.tf/). Awesome stuff!

##### Blue:
Under this directory you also have kustumize files so you can just as easily deploy those individually. Along with the kustumize script here you have the deployment scripts which allow you to push production updates once they have been proven and tested in the green pod.

#### Green:
Under this directory you also have kustumize files so you can just as easily deploy those individually. Along with the kustumize script here you have deployment scripts which allow you to push production updates, Under there you have the deployment scripts which allow you to push stage updates and roll them out to the green pods for testing and bug checks prior to production.

#### How it Works
Once you have updated your application, you add/commit and push your updates to the Git repository which then triggers a pipeline in Jenkins updating your version to the latest version e.g. 1.7 and tagging it in the docker hub, then updates the scripts to update the green deployment to the latest version.

Once you have tested everything you can with the simple change in the services and stage becomes blue and stable becomes green. Just as quickly if something goes awry you can switch them back.

- servicestable.yaml
- servicestage.yaml

`selector
    app: ilab
    version: green #simply change this from green to blue or visaversa  
  type: LoadBalancer`
  
  #### Then simply run this and it will push the networking change:
  
  `kubectl apply -k ./
`  
#### Jenkinsfile:
This pipeline works through the following steps:
- Checks out the application
- Checks the last build version and writes the new one.
- If the docker image still exists it cleans it up and builds the new one.
- It then runs the new build.
- Runs a python test on it, it is a simple test that opens the browser, screenshots it and post to imgur.com, checks for the xpath and then moves on.
- Once the test passes it pushes the new build to docker hub.

At this point it calls the Kubernetes Pipeline, that pipeline applies the changes, updates the changes and pushes them to github.

```pipeline 
    agent {
        label 'ilab-dev'
    }
    stages {
        stage('Get Workspace Directory') {
            steps {
                echo "Workspace is in ${WORKSPACE}"
            }
        }
        stage('Git Checkout Blue Green App'){
            steps{
                git branch: 'main', url:             
                'https://github.com/01010101Basics/blue-green.git'
            }
        }
          stage('Ensure version.txt is writeable'){
            steps{
                sh 'sudo chmod 777 version.txt'
            }
        }
        stage('Create Build Number'){
            steps{ 
                script{
                       def readcounter =    readFile(file: 'version.txt')
                       readcounter = readcounter.toInteger() +1
                       env.VERSION= readcounter
                       echo env.VERSION
                       writeFile(file: 'version.txt',          
                       text:readcounter.toString())
                       writeFile(file: '$HOME/blue-green/version.txt', 
                       text:readcounter.toString())
                }
            }
        }       
        stage('If Docker Image Exist Remove It') {
            steps {
                sh 'sudo docker rm -f wsite'
            }
        }
         stage('Docker Build Image') {
            steps {
                sh 'sudo docker build . -t test'
            }
        }
        stage('Docker Run') {
            steps {
                sh 'sudo docker run --name wsite -it -p 82:80 -d test'
            }
        }
        stage('Test') {
            steps {
                sh '''#!/bin/bash
                sudo chmod +x runpytest.sh
                ./runpytest.sh
                '''
            }
        }
        stage('Test Was Successful Building New Image'){
            steps{
                sh "docker build . -t kmgoddard/bgapp:1.${env.VERSION}"
            }
        }
        stage('Push tne New Version'){
            steps{
                sh "docker push kmgoddard/bgapp:1.${env.VERSION}"
            }
        }
       /* stage('Scan the image for vulnerabilities'){
            steps{
                sh "docker scan kmgoddard/bgapp:1.${env.VERSION}"
            }
        }*/
        stage('It is good lets push it to the repository'){
            steps{
                sh "docker push kmgoddard/bgapp:1.${env.VERSION}"
            }
        }
        stage('Cleanup the Xvfb '){
            steps{
                sh 'killall Xvfb'
            }
        }
        stage('Push Blue-Green to Git'){
            steps{
                sshagent(['github-01010101basics']) {
                sh '''
                sudo chmod +x pushrep.sh
                ./pushrep.sh
                '''}
            }
        }
        stage('Build ilab-ci-cd-kube-bg-deploy') {
            steps{
        
                build job: 'ilab-ci-cd-kube-bg-deploy', parameters: [
                string(name: 'version', value: "${env.VERSION}")]
            } 
        } 
    }
}``

#### Kube Pipeline 
``pipeline 
    agent {
        label "ilab-control"
    }
    stages {
        stage('git main branch') {
            steps {
                git branch: 'main', url: 'https://github.com/01010101Basics/k8s-bg-deployment.git'
            }
        }
        stage('Build'){
            steps{
                sh "./updateimgdeployed.sh \"        image: kmgoddard/bgapp:1.${version}\""
            }
        }
        stage('Build k8s BG Application'){
            steps{
            sh '''
            ./runkube.sh
            '''
            }
        }
    }
}``
