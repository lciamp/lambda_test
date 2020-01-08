#!groovy

pipeline {
    agent {
        node {
            label 'master'
        }
    }
    options {
        skipDefaultCheckout false
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }
    triggers {
        pollSCM 'H/10 * * * *'
    }
    stages {
        stage('waffel lamda zip') {
            when {
                branch 'master'
            }
            steps {
                
                dir("waffel_checkin") {
                    withCredentials([[
                        $class: 'UsernamePasswordMultiBinding',
                        credentialsId: 'aws',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    ]]) {
                        sh 'pip install -r requirements.txt -t ./'
                        sh 'chmod -R 755 .'
                    }
                    echo "Deploying to qa environment"
                }
            }   
        }
        stage('terraform-plan') {
            when {
                branch 'master'
            }
            steps {
                sh 'terraform init'
                sh 'terraform plan'

                }
            }   
        }
    }
    post {
        failure {
            echo "bad"
        }
        success {
            echo "good"
        }
        always {
            echo 'Updating folder permissions.'
            sh "chmod -R 777 ."
        }
        cleanup {
            deleteDir()
        }
    } 
}
