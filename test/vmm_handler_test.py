import readFile
import nova_handler
import token_handler
import zabbix_handler
import project_handler
import vmm_handler
import zabbix_sender
import eventlet
from eventlet.greenpool import GreenPool

conf_file = readFile.ReadConfFile("./conf/proxy.conf")
vm_meters_file = readFile.ReadConfFile("./conf/vm_meters.conf")

# Creation of the Auth keystone-dedicated authentication class
# Responsible for managing AAA related requests
#keystone_auth = token_handler.Auth(conf_file.read_option('keystone_authtoken', 'keystone_host'),
#                                   conf_file.read_option('keystone_authtoken', 'keystone_public_port'),
#                                   conf_file.read_option('keystone_authtoken', 'admin_tenant'),
#                                   conf_file.read_option('keystone_authtoken', 'admin_user'),
#                                   conf_file.read_option('keystone_authtoken', 'admin_password'))
#
## Creation of the Zabbix Handler class
## Responsible for the communication with Zabbix
#zabbix_hdl = zabbix_handler.ZabbixHandler(conf_file.read_option('keystone_authtoken', 'keystone_host'),
#                                          conf_file.read_option('keystone_authtoken', 'keystone_admin_port'),
#                                          conf_file.read_option('nova_configs', 'nova_compute_host'),
#                                          conf_file.read_option('nova_configs', 'nova_compute_listen_port'),
#                                          conf_file.read_option('zabbix_configs', 'zabbix_host'),
#                                          conf_file.read_option('zabbix_configs', 'zabbix_admin_user'),
#                                          conf_file.read_option('zabbix_configs', 'zabbix_admin_pass'),
#                                          conf_file.read_option('zcp_configs', 'template_name'),
#                                          conf_file.read_option('zcp_configs', 'zabbix_proxy_name'),
#                                          keystone_auth,
#                                          vm_meters_file.read_option('vm_meters','meters').split(';'))
#zabbix_hdl.first_run()
#
#nova_hdl = nova_handler.NovaEvents(conf_file.read_option('os_rabbitmq', 'rabbit_host'),
#                                   conf_file.read_option('os_rabbitmq', 'rabbit_user'),
#                                   conf_file.read_option('os_rabbitmq', 'rabbit_pass'),
#                                   zabbix_hdl)
#nova_hdl.nova_amq()



# use green thread to send data to zabbix
pool = GreenPool(50)
# Creation of the Zabbix tcp Contact
zabbix_sender = zabbix_sender.ZabbixSender(conf_file.read_option('zabbix_configs', 'zabbix_host'),
                                           conf_file.read_option('zabbix_configs', 'zabbix_port'),
                                           conf_file.read_option('zcp_configs', 'zabbix_proxy_name'),
                                           vm_meters_file.read_option('vm_meters','meters').split(';'),
                                           pool)

vmm_hdl = vmm_handler.CeilometerEvents(conf_file.read_option('os_rabbitmq', 'rabbit_host'),
                                       conf_file.read_option('os_rabbitmq', 'rabbit_user'),
                                       conf_file.read_option('os_rabbitmq', 'rabbit_pass'),
                                       zabbix_sender,
                                       pool)

vmm_hdl.ceilometer_amq()

