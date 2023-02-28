from dataclasses import dataclass

@dataclass
class CertificateData(object):
    country_name:str
    state_name:str
    locality_name:str
    organization_name:str
    organizational_unit:str
    common_name:str
    email:str
    def __str__(self) -> str:
        text=f'/C=<{self.country_name}>/ST=<{self.state_name}>/L=<{self.locality_name}>/O=<{self.organization_name}>/CN=<{self.common_name}>/OU=<{self.organizational_unit}>'
        return text

class Squid(object):
    def __init__(self, private_key_file, self_signed_certificate_file, rsa_key_length, validity_in_days, ssl_certs_directory, user_that_squid_uses="proxy", comment_http_port=False, conf_file="/etc/squid/conf.d/generated_file.conf", ssl_store_mb_limit_size=50, certificate_data:CertificateData=None) -> None:
        if certificate_data==None:
            raise Exception("Please provide certificate data")
        str_certificate=str(certificate_data)

        self.stop_service           = "sudo service squid stop"
        self.remove_squid           = "sudo apt-get purge -y squid-openssl"
        self.remove_confs           = "sudo rm -rf /etc/squid"
        self.install_squid          = "sudo apt-get install -y squid-openssl"
        self.copy_conf_file         = f'sudo cp {conf_file} /etc/squid/conf.d'
        self.certificate_generation = f'sudo openssl req -new -newkey rsa:{rsa_key_length} -days {validity_in_days} -nodes -x509 -keyout {private_key_file} -out {self_signed_certificate_file} -subj \"{str_certificate}\"'
        self.create_ssl_store       = f'sudo /usr/lib/squid/security_file_certgen  -c -s {ssl_certs_directory} -M {ssl_store_mb_limit_size}MB'
        self.assign_permission      = "sudo chown {0}:{0} {1}".format(user_that_squid_uses, ssl_certs_directory)
        self.comment_http_port      = comment_http_port
        
    def get_text(self):
        commands=[
            self.remove_squid,
            self.install_squid,
            self.certificate_generation,
            self.create_ssl_store,
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
