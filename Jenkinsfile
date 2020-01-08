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
            agent {
                docker {
                    image 'python:3.7.2'
                    args '-u root'
                }
            }
            steps {
                dir("waffle_checkin") {
                    
                    withCredentials([[
                        $class: 'UsernamePasswordMultiBinding',
                        credentialsId: 'aws',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    ]]) {
                        sh 'pip install -r requirements.txt -t ./'
                        sh 'chmod -R 755 .'
                    }
                    sh "ls -l"
                    echo "getting files"
                }
            }
        }
        stage('terraform-plan') {
            when {
                branch 'master'
            }
            steps {
                sh "pwd"
                sh 'terraform init'
                sh 'terraform plan'
            

                }
        }
        stage ("Apply") {
            steps {
                input "Do you approve deployment?"
                echo "appying"
                sh "echo 'yes' | terraform apply"
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
