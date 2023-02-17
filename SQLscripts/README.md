AFIS Database
Setup README

The files mentioned for manual and automatic installation in this README located in /AFIS/server/setup/bin

For automatic install:
Step 1:
	Execute $./AFIS/server/setup/bin/setupDatabase
Step 2:
Follow all on screen prompts, choose and remember the password for the root user for the database.

For manual install
Step 1:
	Run the following commands from the terminal to install MySQL
	 $apt update
	 $apt upgrade
	 $wget -c https://repo.mysql.com//mysql-apt-config_0.8.13-1_all.deb
	 $dpkg -i mysql-apt-config_0.8.13-1_all.deb
	 $apt-get install default-mysql-server
	 $mysql_secure_installation
	 Follow on screen prompts and leave install options at their default settings
	 $systemctl start mysql
	 $systemctl enable mysql

Step 2:
	Open MySQL  with $mysql -r -p
	Type in root password when prompted
	Create an admin user by running ‘AFIS/server/setup/bin/createUser.sql’
	Build the tables by running   `AFIS/server/setup/bin/creatTables.sql` 
The Database is now built

Step 3:
Fill the tables by running ` AFIS/server/setup/bin/insertDB1.sql` and
`AFIS/server/setup/bin/ inserts.sql`. These are the two datasets that have been utilized so far on this project.


The Python files

The files ` AFIS/server/SQLscripts/OriginalNanoparticleImagesSeparatedbySubject /inserts.py` 
and `AFIS/server/SQLscripts/MOLF/DB1_Lumidgm/makeInsertDB1.py` were used to generate the insert SQL files. 
The scrips could be used to generate new insert.sql files if the Root variable is changed to a local path.
