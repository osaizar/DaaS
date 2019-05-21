# FILE SYSTEM STRUCTURE

Each character (not user) is a Linux user
Master => root

In the web server, each user shall have different character in different instances.

---

USER

Each user shall access his/her instance account with the WebServer password. This grants access to his/her character in the instance.
Password hashes are computed in the WS the same way in which it is computed in Unix.

/etc/passwd -> The user shall have a custom script as a command interpreter.
This script, when accessed the first time, will prompt the user with the 'Character Cration and Management' script. In the forthcoming times the user accesses, the initial script will redirect to stardard bash.

---

DIRECTORIES

```/root/sp_lvl/1, 2, ...9/```
Contains the Spell levels, which determines the requirements to use that spell.

```/root/ch_class/wizard/1, 2, ...9/```
Contains the character level, which later defines the habilities (spells) to which it can have access.
