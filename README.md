# honoursProj


Demo for a distributed system to connect databases of hospitals, suppliers, and manufacturers. The project also generates analytics for each case, and provides a time-accurate simulation for fetches and writes at different databases. 

This project was implemented in Django to better simulate database access times. 
***
## Instructions to run on Linux/WSL:


Clone the project with `git clone https://github.com/NegaMage/honoursProj`

`cd honoursProj`

`sudo pip3 install django numpy`

`python3 manage.py makesuperuser`, then follow the prompts to make a superuser account. There's a default account in the database, with username 'feyaz' and password 'password'.

`python3 manage.py runserver` will start the server on your localhost.

***
## Demo

Navigate to `http://localhost:8000/` on your web browser. You've reached the first page anyone sees when they open up the project.

The navbar at the top has some handy helper functions. They're self explanatory.

The eight metrics implemented are also accessible from the navbar. 

***
## Limitations

Due to hardware constraints, I haven't been able to test out the code that fetches across different systems on the same network. The assumption is that all the entities on the network have a shared folder with their neighbours. For any files that can be located on the system itself, it's easy to add to the databases to be searched : https://docs.djangoproject.com/en/3.2/topics/db/multi-db/#:~:text=Django's%20admin%20doesn't%20have,a%20specific%20database%20for%20content. 

As for setting up such a connection, it's a straightforward process with an FTP link. I'll put up some code here as proof that it is easy, and the only reason I haven't done it is because I can't reasonably verify correctness :-)




