Provisining using Ansible instructions
======================================

1. Add the server to an Anisble inventory file named ``hosts``, for more information see https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html

2. Create a vars.yml file based on the ``vars-template.yml`` file and updater it using your favorite text editor, e.g.

```
cp vars-template.yml vars.yml
vi vars.yml
```

3. Run ansible

```ansible-playbook -i hosts playbook.yml```

4. Log into the server and finish the configuration:

```
ssh example.com
su webapp
cd
source activate.sh
cd sr-dispersal
python manage.py makemigrations
python manage.py migrate
exit
systemctl start gunicorn
```
