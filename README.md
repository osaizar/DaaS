# DaaS

## Dungeons&Dragons as a Service

Dungeons & Dragons as a Service is born to pave the way for fast and automated 21st-century role-game campaign creation and configuration. DaaS works as a framework in which one can quickly start playing D&D in a Cloud instance automatically launched by the service, already configured for a _launch-and-play_ experience. 

All participants can choose the details of their characters through a Web-Server wizard, guiding them through the process, including class, stats and race selection. Once chosen, DaaS takes charge of the rest and ensures a Cloud instance is created, in which the characters are setup for login for the users and Dungeon Master to do so. When logging in, characters will find the access to their spells already configured. All spell access will be based on the character’s level and class, as there will be an Access Control List running to make sure each character is limited to their legitimate capabilities. 

The Web Server runs in an Apache Server, and uses Ansible to tell the machine in charge of the instances (CentOS) to launch a new instance to host the new campaign. This Cloud Campaign will be a CentOS as well, which will be remotely configured via Ansible with everything necessary for the game to go smoothly. Spells are organized as files in a file tree separating character classes and levels while these spells’ permissions to be used are remotely configured
too through an Access Control list based on the character’s attributes.
