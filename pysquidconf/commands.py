

class Squid(object):
    def __init__(self, private_key_file, self_signed_certificate_file, rsa_key_length, validity_in_days, ssl_certs_directory, user_that_squid_uses="proxy", comment_http_port=False) -> None:
        
        self.remove_squid           = "sudo apt-get purge -y squid-openssl"
        self.remove_confs           = "sudo rm -rf /etc/squid"
        self.install_squid          = "sudo apt-get install -y squid-openssl"
        self.certificate_generation = f'sudo openssl req -new -newkey rsa:{rsa_key_length} -days {validity_in_days} -nodes -x509 -keyout {private_key_file} -out {self_signed_certificate_file}'
        self.assign_permission      ="sudo chown {0}:{0} {1}".format(user_that_squid_uses, ssl_certs_directory)
        self.comment_http_port      =comment_http_port
        
    def get_text(self):
        commands=[
            self.remove_squid,
            self.install_squid,
            self.certificate_generation,
            self.assign_permission
        ]
        if self.comment_http_port:
            commands.append("sed -i 's/http_port 3128/#http_port 3128/g' /etc/squid/squid.conf")
        return "\n".join(commands)
    
    def save(self, filename):
        with open(filename, "w") as fd:
            fd.write("#!/bin/bash\n")
            fd.write(self.get_text())
            fd.write("\n\n")
