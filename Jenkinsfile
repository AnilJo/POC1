pipeline {
    agent any 

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REGISTRY = 'public.ecr.aws/w1u8a9m1'
        ECR_REPOSITORY = 'ajose'
        DOCKER_IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withAWS(region: "${AWS_REGION}", credentials: 'aws-credentials-id') {
                        def login = sh(script: "aws ecr-public get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}", returnStdout: true).trim()
                        sh("docker tag ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}")
                        sh("docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}")
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    withAWS(region: "${AWS_REGION}", credentials: 'aws-credentials-id') {
                        sh '''
                        rm -rf esk
                        git clone https://github.com/AnilJo/esk.git
                        cd esk
                        terraform init
                        terraform apply -auto-approve
                        '''
                    }
                }
            }
        }
    }
}
