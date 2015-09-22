import readFile
import token_handler
import zabbix_handler



conf_file = readFile.ReadConfFile("./conf/proxy.conf")



print ">>",conf_file.read_option('keystone_authtoken', 'keystone_host')
print ">>",conf_file.read_option('keystone_authtoken', 'keystone_admin_port')

print ">>",conf_file.read_option('nova_configs', 'nova_compute_host')
print ">>",conf_file.read_option('nova_configs', 'nova_compute_listen_port')

print ">>",conf_file.read_option('zabbix_configs', 'zabbix_host')
print ">>",conf_file.read_option('zabbix_configs', 'zabbix_admin_user')
print ">>",conf_file.read_option('zabbix_configs', 'zabbix_admin_pass')

print ">>",conf_file.read_option('zcp_configs', 'template_name')
print ">>",conf_file.read_option('zcp_configs', 'zabbix_proxy_name')


# Creation of the Auth keystone-dedicated authentication class
# Responsible for managing AAA related requests
keystone_auth = token_handler.Auth(conf_file.read_option('keystone_authtoken', 'keystone_host'),
                                   conf_file.read_option('keystone_authtoken', 'keystone_public_port'),
                                   conf_file.read_option('keystone_authtoken', 'admin_tenant'),
                                   conf_file.read_option('keystone_authtoken', 'admin_user'),
                                   conf_file.read_option('keystone_authtoken', 'admin_password'))

# Creation of the Zabbix Handler class
# Responsible for the communication with Zabbix
zabbix_hdl = zabbix_handler.ZabbixHandler(conf_file.read_option('keystone_authtoken', 'keystone_host'),
                                          conf_file.read_option('keystone_authtoken', 'keystone_admin_port'),
                                          conf_file.read_option('nova_configs', 'nova_compute_host'),
                                          conf_file.read_option('nova_configs', 'nova_compute_listen_port'),
                                          conf_file.read_option('zabbix_configs', 'zabbix_host'),
                                          conf_file.read_option('zabbix_configs', 'zabbix_admin_user'),
                                          conf_file.read_option('zabbix_configs', 'zabbix_admin_pass'),
                                          conf_file.read_option('zcp_configs', 'template_name'),
                                          conf_file.read_option('zcp_configs', 'zabbix_proxy_name'), 
                                          keystone_auth)


print zabbix_hdl.get_zabbix_auth()
print zabbix_hdl.get_proxy_id()
