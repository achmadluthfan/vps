# Contianer as a Service (CaaS)
## 🧐Overview
Container as a Service (CaaS) is a cloud computing service that provides users with scalable and flexible container management solutions. Our CaaS platform allows users to easily deploy, manage, and scale containerized applications with minimal effort.
## 🤩Key Features
- **SSH Access**: Users can securely access their containers via SSH through a public IP address, making remote management and configuration straightforward.
- **Web Accessibility**: Web content hosted within containers is accessible on the internet through a unique subdomain, ensuring that your applications are available to your audience without additional configuration.
## 😯How It Workds
How our CaaS platform works:
1. **Sign Up**: Create an account on our platform.
2. **Deploy Your Container**: Use our interface to deploy a new container.
3. **Access and Manage**: SSH into your container using the provided public IP and manage your applications.
4. **Publish Web Content**: Your web content will be live on the internet through your designated subdomain.
## 🤨Preparation
Before using this project, make sure you have the following software and tools installed:
1. **Proxmox VE**: Required for generate container that is Linux Container (LXC). [Download Proxmox VE ISO]([https://www.docker.com/get-started](https://www.proxmox.com/en/downloads)
2. **Virtual Private Server**: Deploy and manage the applications.
3. **VPN Server and Client**: Connect Proxmox from local with applications inside VPS using secure communication.
4. **Domain and Hosting**: Create subdomain and make it accessible from outside. [Cloudflare]([https://code.visualstudio.com/](https://dash.cloudflare.com/)
## 😏Getting Started
Here’s an overview of the installation structure:
```
caas/
├── automate
│ └── manage_ports.sh
├── docker-entrypoint-initdb.d
│ └── init.sql
└── docker-compose.yml
```
1. Create and copy file structure above inside `caas` folder in your VPS.
2. Change owned `automate` folder become `root:root` using `sudo chown root:root caas/automate`.
3. Run docker applications using `docker-compose up --build -d`.
4. Enjoy the service and create some containers.
## 👨‍💻Author
- **Backend and Architecture**: [Dzaki Maulana Asif](dzakimaulanaasif2004@mail.ugm.ac.id)
- **Frontend**: [Achmad Luthfan Nur](achmadluthfannurirsyad@mail.ugm.ac.id)
## 🥸Author's Message
Thank you for exploring our project! We’re excited to share it with you and appreciate your interest. As this is a growing project with many features still to be implemented, you might encounter some bugs or areas that need improvement.

We’re always eager to learn and improve, so if you have any suggestions or advice on how we can enhance the service, please don't hesitate to reach out. Your feedback is invaluable in helping us create a more robust and efficient project.

Happy developing, and we look forward to hearing from fellow developers!
