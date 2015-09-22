import readFile
import token_handler

conf_file = readFile.ReadConfFile("./conf/proxy.conf")

print ">>",conf_file.read_option('keystone_authtoken', 'keystone_host')
print ">>",conf_file.read_option('keystone_authtoken', 'keystone_public_port')
print ">>",conf_file.read_option('keystone_authtoken', 'admin_tenant')
print ">>",conf_file.read_option('keystone_authtoken', 'admin_user')
print ">>",conf_file.read_option('keystone_authtoken', 'admin_password')

# Creation of the Auth keystone-dedicated authentication class
# Responsible for managing AAA related requests
keystone_auth = token_handler.Auth(conf_file.read_option('keystone_authtoken', 'keystone_host'),
                                   conf_file.read_option('keystone_authtoken', 'keystone_public_port'),
                                   conf_file.read_option('keystone_authtoken', 'admin_tenant'),
                                   conf_file.read_option('keystone_authtoken', 'admin_user'),
                                   conf_file.read_option('keystone_authtoken', 'admin_password'))

print keystone_auth.getToken()
