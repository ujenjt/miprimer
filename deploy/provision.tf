variable "digitalocean_token" {}

provider "digitalocean" {
  token = "${var.digitalocean_token}"
}

resource "digitalocean_droplet" "bio" {
  # Obtain your ssh_key id number via your account. See Document https://developers.digitalocean.com/documentation/v2/#list-all-keys
  ssh_keys           = [3601656]
  image              = "ubuntu-16-04-x64"
  region             = "ams2"
  size               = "512mb"
  private_networking = false
  backups            = false
  ipv6               = true
  name               = "bio"

  provisioner "file" {
    source      = "nginx.conf"
    destination = "/root/nginx.conf"

    connection {
      type     = "ssh"
      private_key = "${file("~/.ssh/id_rsa")}"
      user     = "root"
      timeout  = "2m"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D",
      "sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'",
      "sudo apt-get update",
      "sudo apt-get install -y docker-engine python-minimal python-pip",
      "sudo pip install docker-py",
      "sudo docker run -d --name nginx -v /root/nginx.conf:/etc/nginx/nginx.conf:ro -p 80:9000 nginx",
      "sudo docker run -d --name miprimer -p 172.17.0.1:4242:4242 ujenjt/miprimer"
    ]

    connection {
      type     = "ssh"
      private_key = "${file("~/.ssh/id_rsa")}"
      user     = "root"
      timeout  = "2m"
    }
  }
}

output "Public_ip" {
  value = "${digitalocean_droplet.bio.ipv4_address}"
}

output "Name" {
  value = "${digitalocean_droplet.bio.name}"
}
