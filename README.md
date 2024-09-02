# Advanced End-to-End DevOps Project 

This repository contains an advanced end-to-end DevOps project that integrates various tools such as Git, Docker, Kubernetes, Helm, GitHub Actions, Jenkins, Terraform, Ansible, AWS, and Shell scripts. The project sets up a continuous integration and deployment pipeline.

## Architecture Diagram

![ArchitectureDiagram](Screenshots/Architecture.png)

## WebApp Overview

- We are going to deploy below game app on the K8s cluster.
![Exposed API /api/weather](Screenshots/webapp-weather.png)
![Exposed API /api/weather/stats](Screenshots/webapp-stats.png)


## Project Overview

### Step 1: Fork and Customize Repository

- Fork this repository and make any customizations if needed.

### Step 2: Set Up Jenkins Server on AWS EC2 Instance

- Create an EC2 instance on AWS with security group rules allowing ports 8080 and 50000.
- Install Docker on the instance.
- Configure Jenkins using the following command:
  ```bash
  docker run -d -v jenkins_home:/var/jenkins_home -p 8080:8080 -p 50000:50000 --restart=on-failure jenkins/jenkins:lts-jdk17
- Access Jenkins at http://<your-instance-ip>:8080, configure Jenkins, and install suggested plugins.

### Step 3: Configure Jenkins Worker Node
- Launch a second EC2 instance and configure it as a Jenkins worker node using the steps in the `JenkinsSlaveEc2Node` file.

### Step 4: Create Jenkins Pipeline
- Create a pipeline in Jenkins named "mypipeline" with the repository location and enable the webhook.

### Step 5 Configure GitHub Webhook 
- Add a webhook to your GitHub repository with the Jenkins URL: http://<your-jenkins-ip>:8080/github-webhook/.
- Select only the push event.

### Step 6 Configure DockerHub Credentials 
- As we are using GitHub Workflows for the Build, Testing, and publishing of my docker image, Hence we need to add DockerHub credentials to GitHub secrets with variables` DockerUsername` and `DockerPassword`.

### Step 7 Configure AWS Credentials
- Provide AWS credentials on the Jenkins slave node using _#awS configure_ or store them in Jenkins secrets, and then further add a step in `Jenkinsfile` to configure AWS credentials automatically. Terraform will use these credentials.

### Step 8 Run the Pipeline
- Trigger the pipeline in Jenkins and ensure all steps are executed correctly.

### Step 9 Make Changes and Test
- Make changes in your code locally, push to GitHub, and create a pull request.
- GitHub Actions will build, and push the Docker image.
- Merge the pull request to trigger the Jenkins pipeline, Which will deploy your app on top of k8s cluster

### Step 10: Jenkins Pipeline Stages
- Git
- Setup Ansible
- Setup Terraform
- Create Infrastructure for PROD
- Configure multi node k8s cluster on the created infrastructure
- Deploy the Model, Which will perform data ingestion and api expose
- ![Jenkins Pipeline Stage View](Screenshots/jenkinspipeline.png)

### Step 11: Access the Exposed API
- Visit http://<K8sMaster-ip>:5000 to see the deployed webserver.


# Action Required: Update CRI-O Installation URL

- Issue:

The CRI-O RPM file URL in the deploy/playbooks/rhel_common.yaml file on line 55 is subject to frequent changes. The current command used for installation is:

`yum install https://download.opensuse.org/repositories/isv:/kubernetes:/addons:/cri-o:/prerelease:/v1.29:/build/rpm/x86_64/cri-o-1.29.7~dev-150500.16.1.x86_64.rpm -y`

- Required Action:

1) Immediate Update:

Update the URL to the latest version. You can find the updated URL from the CRI-O artifacts here.
`https://download.opensuse.org/repositories/isv:/kubernetes:/addons:/cri-o:/prerelease:/v1.29:/build/rpm/x86_64/`

2) Long-term Solution:

Instead of manually updating the URL every time, we can consider configuring a yum repository for CRI-O. This will allow the playbook to pull the latest version automatically, reducing the need for manual intervention.
This approach will streamline the process and ensure that the playbook remains up-to-date with the latest CRI-O version.
