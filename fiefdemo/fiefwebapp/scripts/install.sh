#!/bin/bash

if ! command -v pip &> /dev/null; then
    echo "PIP is not installed. Install pip..."
    . /etc/os-release
    case $ID in
        ubuntu|debian|raspbian)
            sudo apt update
            sudo apt install -y python3-pip
            ;;
        rhel|centos|fedora)
            sudo yum update
            sudo yum install -y python3-pip
            ;;
        *)
            echo "Unsupported operating system."
            exit 1
            ;;
    esac
fi

if ! python3 -c "import jinja2" &> /dev/null; then
    echo "Jinja2 is not installed. Install Jinja2..."
    pip3 install Jinja2
fi
