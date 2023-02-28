import logging


class ConfFile(object):
    NUMBER_OF_HASHES=60
    def __init__(self) -> None:
        self.ssl_start = []
        self.http_port = []
        self.blocks    = []
        self.allows    = []
        self.ssl_end   = []
        
        self.acl_network_template       = "acl               {0} {1}"
        self.http_allow_access_template = "http_access allow {0}"
        self.http_deny_access_template  = "http_access deny  {0}"
        self.dstdomain_template         = "acl               {0} dstdomain  {1}"
        self.url_regex_template         = "acl               {0} url_regex  {1}"

        self.logger=logging.getLogger("ConfFile")
        logging.basicConfig(level=logging.ERROR)

    def _add_http_access(self, allow, name):
        self.logger.debug("Adding http access")
        if allow:
            self.allows.append( self.http_allow_access_template.format(name)      ) 
        else:
            self.blocks.append( self.http_deny_access_template.format(name)      ) 

    def _get_list_to_add(self, allow):
        list_to_add=None
        if allow:
            list_to_add=self.allows
        else:
            list_to_add=self.blocks
        return list_to_add
    
    

    def _add_begin_section(self, list_to_add, comment):
        
        list_to_add.append("\n")
        if comment=="":
            list_to_add.append("#"*ConfFile.NUMBER_OF_HASHES)
        else:
            comment_string="  Inicio {0}  ".format(comment).center(ConfFile.NUMBER_OF_HASHES, "#")
            list_to_add.append(comment_string)

    def _add_end_section(self, list_to_add, comment):
        
        if comment=="":
            list_to_add.append("#"*ConfFile.NUMBER_OF_HASHES)
        else:
            comment_string="  Fin {0}  ".format(comment).center(ConfFile.NUMBER_OF_HASHES, "#")
            list_to_add.append(comment_string)
        list_to_add.append("\n")

    def add_network_acl(self, name, ip, allow=True, comment=""):
        list_to_add=self._get_list_to_add(allow)    
        self._add_begin_section(list_to_add, comment)

        list_to_add.append( self.acl_network_template.format(name, ip) )
        self._add_http_access(allow, name)

        self._add_end_section(list_to_add, comment)

    def add_dstdomain_acl(self, name, domains, allow=True, comment=""):
        list_to_add=self._get_list_to_add(allow)    
        
        self._add_begin_section(list_to_add, comment)

        if isinstance(domains, list):
            domain_string=" ".join(domains)
        else:
            domain_string="\"{0}\"".format(domains)
        list_to_add.append(self.dstdomain_template.format(name, domain_string))
        self._add_http_access(allow, name)

        self._add_end_section(list_to_add, comment)

    def add_url_regex(self, name, url_regex, allow=True, comment=""):
        list_to_add=self._get_list_to_add(allow)    
        self._add_begin_section(list_to_add, comment)
        list_to_add.append(self.url_regex_template.format(name, url_regex))
        
        self._add_http_access(allow, name)
        self._add_end_section(list_to_add, comment)

    def add_ssl_start(self, acl_name, comment=""):
        self._add_begin_section(self.ssl_start, comment)
        self.ssl_start.append("acl {0} transaction_initiator certificate-fetching".format(acl_name))
        self.ssl_start.append("http_access allow {0}".format(acl_name))
        self._add_end_section(self.ssl_start, comment)

    def add_ssl_end(self, ssl_store_path, mb_limit, comment=""):
        self._add_begin_section(self.ssl_end, comment)
        sslcrtd="sslcrtd_program /usr/lib/squid/security_file_certgen -s {0} -M {1}MB"
        ssl_cert_error="sslproxy_cert_error allow all"
        ssl_stare="ssl_bump stare all"
        self.ssl_end.append(sslcrtd.format(ssl_store_path, mb_limit))
        self.ssl_end.append(ssl_cert_error)
        self.ssl_end.append(ssl_stare)
        self._add_end_section(self.ssl_end, comment)
    
    def add_http_port(self, cache_size, certificate_file, private_key, comment=""):
        
        http_port_template=f'http_port 3128 tcpkeepalive=60,30,3 ssl-bump \
            generate-host-certificates=on \
            dynamic_cert_mem_cache_size={cache_size}MB \
            tls-cert={certificate_file} \
            tls-key={private_key}'
        
    def get_text(self):
        lines=self.ssl_start+self.http_port+self.blocks + self.allows + self.ssl_end
        
        return "\n".join(lines)
        
    def save(self, filename):
        with open(filename, "w") as fd:
            fd.write(self.get_text())
            fd.write("\n\n")