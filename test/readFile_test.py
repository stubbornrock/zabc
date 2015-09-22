import readFile
conf_file = readFile.ReadConfFile("./conf/vm_meters.conf")
meters=conf_file.read_option('vm_meters', 'meters')
print meters.split(',')

