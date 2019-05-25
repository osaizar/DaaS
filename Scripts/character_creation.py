import os
import grp

# prints group names of the user who runs it
# prints group names of the user who runs it
# user's groups ids
gid = os.getgroups()
# group's name
for group in gid:
    gname = grp.getgrgid(group)[0]
    print(gname)
