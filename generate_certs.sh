#!/bin/bash

# Variáveis
SERVER_IP="20.186.15.152"
DAYS=365
CA_KEY="ca_key.pem"
CA_CERT="ca_certificate.pem"
SERVER_KEY="server_key.pem"
SERVER_CERT="server_certificate.pem"
SERVER_CSR="server_csr.pem"
CLIENT_KEY="client_key.pem"
CLIENT_CERT="client_certificate.pem"
CLIENT_CSR="client_csr.pem"
CONFIG_FILE="openssl.cnf"

# Criar um arquivo de configuração openssl
cat > $CONFIG_FILE <<EOL
[ req ]
default_bits        = 2048
distinguished_name  = req_distinguished_name
x509_extensions     = v3_req
string_mask         = utf8only

[ req_distinguished_name ]
countryName                 = Country Name (2 letter code)
countryName_default         = US
stateOrProvinceName         = State or Province Name (full name)
stateOrProvinceName_default = California
localityName                = Locality Name (eg, city)
localityName_default        = San Francisco
organizationName            = Organization Name (eg, company)
organizationName_default    = My Company
commonName                  = Common Name (e.g. server FQDN or YOUR name)
commonName_max              = 64

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
IP.1 = $SERVER_IP
EOL

# Gerar chave privada para CA
openssl genpkey -algorithm RSA -out $CA_KEY

# Criar certificado autoassinado da CA
openssl req -x509 -new -nodes -key $CA_KEY -sha256 -days $DAYS -out $CA_CERT -subj "/C=US/ST=California/L=San Francisco/O=My Company/CN=My CA"

# Gerar chave privada para o servidor
openssl genpkey -algorithm RSA -out $SERVER_KEY

# Criar CSR (Certificate Signing Request) para o servidor
openssl req -new -key $SERVER_KEY -out $SERVER_CSR -subj "/C=US/ST=California/L=San Francisco/O=My Company/CN=$SERVER_IP" -config $CONFIG_FILE

# Assinar o certificado do servidor com a CA
openssl x509 -req -in $SERVER_CSR -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial -out $SERVER_CERT -days $DAYS -sha256 -extfile $CONFIG_FILE -extensions v3_req

# Gerar chave privada para o cliente
openssl genpkey -algorithm RSA -out $CLIENT_KEY

# Criar CSR (Certificate Signing Request) para o cliente
openssl req -new -key $CLIENT_KEY -out $CLIENT_CSR -subj "/C=US/ST=California/L=San Francisco/O=My Company/CN=Client"

# Assinar o certificado do cliente com a CA
openssl x509 -req -in $CLIENT_CSR -CA $CA_CERT -CAkey $CA_KEY -CAcreateserial -out $CLIENT_CERT -days $DAYS -sha256

# Limpar arquivos temporários
rm $SERVER_CSR $CLIENT_CSR $CONFIG_FILE

echo "Certificados gerados com sucesso!"
echo "Certificados CA: $CA_KEY, $CA_CERT"
echo "Certificados Servidor: $SERVER_KEY, $SERVER_CERT"
echo "Certificados Cliente: $CLIENT_KEY, $CLIENT_CERT"

