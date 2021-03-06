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
    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
    }
    stages {
        stage('waffel lamda zip') {
            when {
                branch 'master'
            }
            steps {
                dir("waffle_checkin") {
                    echo "getting files"
                    withCredentials([[
                        $class: 'UsernamePasswordMultiBinding',
                        credentialsId: 'aws',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    ]]) {
                        sh 'python3 -m pip install -r requirements.txt -t ./'
                        sh 'chmod -R 755 .'
                    }
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
        stage ("terraform-apply") {
            steps {
                input "Do you approve deployment?"
                echo "appying"
                sh "echo 'yes' | terraform apply"
            }
        }
        //stage ("artifact to s3") {
        //    steps {
        //        withAWS(credentials:'aws') {
        //            s3Upload(file: 'waffle_checkin.zip', bucket: 'lous-test-bucket', path: 'archives/waffle_checkin.zip')
        //        }        
        //    }
        //}
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
