# increment-ex
this is a test repo to show some functions

There are two ways to make it run

1.> Using docker [https://www.docker.com/] and docker compose [https://docs.docker.com/compose/]. Steps are - 
  
  a) Make sure that you have both the docker and docker-compose command running.
  
  b) Clone the repo and cd to the repo
  
  c) Run - 
  
      docker-compose build
      docker-compose up
      
  
  d) That's it!! (Of course you have to connect to it via port 5000)

2.> If you are not having those two things then OR you do not want to use them OR you are having a trouble to set it up then

  a) Make sure you have Python and virtualenv installed and working
  
  b) Clone the repo
  
  c) cd to the repo
  
  d) Open settings_default.py and change this
  
      USING_DOCKER = True
      
  to 
  
      USING_DOCKER = False
      
  e) Make sure you have an instance of MongoDB [https://www.mongodb.org/] running and ready to be used. Also please check the host name, port number etc and if necessary change them in the settings_default.py file.
  
  f) Run 
  
      ./insall.sh
      ./run.sh
      
  g) If everything goes right then the application is ready and serving at port 5000. (* ./install.sh is an one time command. Use it only once. Whereas whenever you want to run the app use ./run.sh and to stop it simply use Ctrl-C *)
  

## Usage -

Whether you are using Docker or normal way, always, if running, the application will be accessible via http://localhost:5000

For the increment API to work please access http://localhost:5000/mykey   (*Please note that you can use any value at the place 'mykey' to set any key*)
  
## Caution -  

1.> This application does not use nginx or anything like this in front of Flask default dev server. This is something different and standard. No need to do it at this stage. Of course we can surely do it later. Docker has standard nginx container.

2.> This application is just for the demo purpose. Use of this code is subject to permission.
