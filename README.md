### INFO
```
This is a email Auto Forwarding Service(AFS)
* Parse email
    Determine the decoding method according to Content-Type.
* Send email
    Use SMTP
* Email history
    Only log IP, stat_code, From, to, Subject, Content of the received email


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
   |                                       # placed in the crontab of 192.168.55.25
   |
   |-- docker-compose.yaml                 # Docker-compose use
   |
   |-- ************************************************************************

```