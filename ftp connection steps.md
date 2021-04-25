First, we need to expose the computer to the network. From what I remember of Networking class, it's done by getting your specific MAC Address on a network. (https://www.process.st/checklist/linux-ftp-server-setup-checklist/) If you want to expose it to the WWW, there's specific services that handle that for you.

Now, we need to ssh into the system every time. This is possible by setting a service daemon to start on startup of your linux system. 

That's it. By this time, you have the files technically mounted onto a physical location on your drive. Depending on network speeds, you'll be able to access files nearly instantly. 