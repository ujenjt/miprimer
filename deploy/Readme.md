# Environment

Host machine requirements
`Ansible >= 2.2`
`Terraform >= 0.9`

Remote machine requirements
`python >= 2.6`
`docker-py >= 1.7`
`Docker API >= 1.20`

# Deploy tips

How to update miprimer

1. Build container with miprimer locally and test
2. Push them to Docker Hub
3. Deploy `ansible-playbook deploy.yml -i IP_ADDRESS,`

# Provision digital ocean droplet

1. Create token https://cloud.digitalocean.com/settings/api/tokens with
read and write permissions.
2. `export TF_VAR_digitalocean_token=YOUR_TOKEN_HERE`
3. `terrafrom plan`
4. `terrafrom apply`
5. `terrafrom destroy`
