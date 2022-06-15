### INFO
```
This is a email Auto Forwarding Service(AFS)
* Parse email
    Determine the decoding method according to Content-Type.(Currently supports text/plain, text/html)
* Send email
    Use SMTP
*  Email log
    Record the IP, From, To, and subject of the email received
```

### Project structure
```
< PROJECT ROOT >
   |
   |-- runtime_package/
   |    |-- Dockerfile.runtime_package
   |    |-- requirements.txt               # Development modules
   |
   |-- src/
   |    |-- runserver.py                   # Start the app 
   |
   |-- tool/
   |    |-- check_afs.py                   # Check whether the service is normal, currently placed in 
   |                                       # placed in the crontab of 192.168.55.26
   |
   |-- docker-compose.yaml                 # Docker-compose use
   |
   |-- ************************************************************************

```