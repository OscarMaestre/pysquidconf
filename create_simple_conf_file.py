#!/usr/bin/env python3

from pysquidconf.conf import ConfFile
from pysquidconf.commands import Squid, CertificateData


def get_certificate_data():
    certificate_data=CertificateData("ES", "CLM", "CR", "IES Maestre de Calatrava","Dep Informatica", "Profesor", "nada@gmail.com")
    print(certificate_data)
    return certificate_data

def crear_fichero():
    filename="mifichero.conf"
    mb_cache_size=75
    certificate_file_for_browser="FirefoxCertificate.crt"
    private_key_file="PrivateKey.key"
    
    conf=ConfFile()
    conf.add_network_acl("Oficina", "172.16.0.0/16", allow=False, comment="Denegar 172.16.0.0/16")
    conf.add_network_acl("Oficina", "192.168.0.0/24", allow=True, comment="Permitir 192.168.0.0/24")
    domains=[".marca.com", ".as.com", ".elpais.com"]
    conf.add_dstdomain_acl("periodicos", domains, allow=False, comment="Periodicos")

    conf.add_dstdomain_acl("webs", "lista_webs.txt", allow=False, comment="Periodicos")

    conf.add_url_regex("paginas_violentas", "viol", allow=False, comment="")

    conf.add_ssl_start("manipular_certificados", comment="Procesado de certificados")
    conf.add_ssl_end("/etc/squid/ficheros", mb_cache_size,comment="Generacion de certificados")
    conf.add_http_port(mb_cache_size,certificate_file_for_browser,private_key_file)
    conf.save(filename)

    certificate=get_certificate_data()
    squid_commands=Squid(private_key_file, certificate_file_for_browser,
                         validity_in_days=365, rsa_key_length=2048,
                         ssl_certs_directory="/etc/squid/certificados_squid_ssl",
                         comment_http_port=True, conf_file=filename, ssl_store_mb_limit_size=mb_cache_size,
                         certificate_data=certificate)
    squid_commands.save("squid.sh")

if __name__=="__main__":
    crear_fichero()