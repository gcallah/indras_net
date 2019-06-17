#!/bin/bash
# This shell file deploys a new version to our server.

eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 ~/.ssh/id_rsa # Allow read access to the private key
ssh-add ~/.ssh/id_rsa # Add the private key to SSH

echo "SSHing to PythonAnywhere."
ssh -o "StrictHostKeyChecking no" indrasnet@ssh.pythonanywhere.com << EOF
    cd ~/indras_net; ~/indras_net/rebuild.sh
EOF
