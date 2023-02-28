#!/usr/bin/env python3

from pysquidconf.conf import ConfFile


def crear_fichero():
    conf=ConfFile()
    conf.add_network_acl("Oficina", "172.16.0.0/16", allow=False, comment="Denegar 172.16.0.0/16")
    conf.add_network_acl("Oficina", "192.168.0.0/24", allow=True, comment="Permitir 192.168.0.0/24")
    domains=[".marca.com", ".as.com", ".elpais.com"]
    conf.add_dstdomain_acl("periodicos", domains, allow=False, comment="Periodicos")

    conf.add_dstdomain_acl("webs", "lista_webs.txt", allow=False, comment="Periodicos")

    conf.add_url_regex("paginas_violentas", "viol", allow=False, comment="")

    conf.add_ssl_start("manipular_certificados", comment="Procesado de certificados")
    conf.add_ssl_end("/etc/squid/ficheros", 50,comment="Generacion de certificados")
    print (conf.get_text())

if __name__=="__main__":
    crear_fichero()