#!/usr/bin/python
import errno
import os

try:
    from OpenSSL import crypto
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.exceptions import InvalidSignature
except ImportError:
    pyopenssl_found = False
else:
    pyopenssl_found = True

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


def compare_x509(x509_a, x509_b):
    ''' Compares the digest of each cert.  Returns True if equal.'''
    x509_a_digest = x509_a.digest('sha256')
    x509_b_digest = x509_b.digest('sha256')
    return x509_a_digest == x509_b_digest


def compare_ca_certs(chain_a, chain_b):
    ''' Compare two X509 ca_cert chains. The chains must be in the same order.'''
    if chain_a is not None:
        if chain_b is None:
            return False
        if len(chain_a) != len(chain_b):
            return False
        for idx in range(0, len(chain_a)):
            if not compare_x509(chain_a[idx], chain_b[idx]):
                return False
    return True


def compare_privatekey_with_encrypt(pkey_a, pkey_b):
    ''' Compare two private keys using encrypt/decrypt'''
    data = b'abcdefghijklmnopqrstuvwxyz0123456789'
    pad = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    pkey_a_c = pkey_a.to_cryptography_key()
    pkey_b_c = pkey_b.to_cryptography_key()

    ciphertext = pkey_a_c.public_key().encrypt(data, pad)
    plaintext = pkey_b_c.decrypt(ciphertext, pad)
    return data == plaintext


def compare_private_keys_with_signature(pkey_a, pkey_b):
    ''' Compare two private keys using a quich sign/verify'''
    data = b'abcdefghijklmnopqrstuvwxyz0123456789'
    pad = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)
    alg = hashes.SHA256()
    pkey_a_c = pkey_a.to_cryptography_key()
    pkey_b_c = pkey_b.to_cryptography_key()
    signature = pkey_a_c.sign(data, pad, alg)
    try:
        pkey_b_c.public_key().verify(signature, data, pad, alg)
        return True
    except InvalidSignature:
        return False


class PKCS12Error(Exception):
    pass


class PKCS12(object):

    def __init__(self, module):
        self.module = module
        self.state = module.params['state']
        self.ca_certs = module.params['ca_certs']
        self.ca_certs_paths = module.params['ca_certs_paths']
        self.cert_path = module.params['cert_path']
        self.cert = module.params['cert']
        self.force = module.params['force']
        self.path = module.params['path']
        self.privatekey = module.params['privatekey']
        self.privatekey_path = module.params['privatekey_path']
        self.privatekey_passphrase = module.params['privatekey_passphrase']
        self.passphrase = module.params['passphrase']
        self.iterations = module.params['iterations']
        self.mac_iterations = module.params['mac_iterations']
        self.friendlyname = module.params['friendlyname']
        self.changed = True

        if self.cert is None:
            cert_content = open(self.cert_path).read()
            self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_content)

        if self.ca_certs is None and self.ca_certs_paths is not None:
            self.ca_certs = []
            for path in self.ca_certs_paths:
                cert_content = open(path).read()
                self.ca_certs.append(crypto.load_certificate(crypto.FILETYPE_PEM, cert_content))

        if self.privatekey is None:
            privatekey_content = open(self.privatekey_path).read()
            self.privatekey = crypto.load_privatekey(crypto.FILETYPE_PEM, privatekey_content, self.privatekey_passphrase)

    def compare(self):
        '''If the PKCS12 already exists, compare it to see if any of the DN values
        have changed. Returns True if the values match'''

        if not os.path.exists(self.path):
            return False

        pkcs12_content = open(self.path, 'rb').read()
        pkcs12 = crypto.load_pkcs12(pkcs12_content, self.passphrase)

        if not compare_x509(self.cert, pkcs12.get_certificate()):
            return False
        if not compare_ca_certs(self.ca_certs, pkcs12.get_ca_certificates()):
            return False
        if not compare_privatekey_with_encrypt(self.privatekey, pkcs12.get_privatekey()):
            return False
        return True

    def generate(self):
        '''Generate the certificate signing request.'''

        if not os.path.exists(self.path) or self.force or not self.compare():

            try:
                pkcs12 = crypto.PKCS12()
                pkcs12.set_certificate(self.cert)
                pkcs12.set_ca_certificates(self.ca_certs)
                pkcs12.set_privatekey(self.privatekey)
                if self.friendlyname:
                    pkcs12.set_friendlyname(self.friendlyname)

                pkcs12_file = open(self.path, 'wb')
                pkcs12_file.write(pkcs12.export(self.passphrase, self.iterations, self.mac_iterations))
                pkcs12_file.close()
            except (IOError, OSError) as exc:
                raise PKCS12Error(exc)
        else:
            self.changed = False

        file_args = self.module.load_file_common_arguments(self.module.params)
        if self.module.set_fs_attributes_if_different(file_args, False):
            self.changed = True

    def remove(self):
        '''Remove the existing PKCS12.'''
        try:
            os.remove(self.path)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise PKCS12Error(exc)
            else:
                self.changed = False

    def dump(self):
        '''Serialize the object into a dictionary.'''

        return {
            'pkcs12': self.path,
            'changed': self.changed
        }


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            force=dict(default=False, type='bool'),
            path=dict(required=True, type='path'),
            cert=dict(type='str'),
            cert_path=dict(type='path'),
            privatekey=dict(type='str'),
            privatekey_path=dict(type='path'),
            privatekey_passphrase=dict(type='str'),
            ca_certs=dict(type='list'),
            ca_certs_paths=dict(type='list'),
            passphrase=dict(required=True, type='str'),
            friendlyname=dict(type='str'),
            iterations=dict(type='int', default=2048),
            mac_iterations=dict(type='int', default=1)
        ),
        add_file_common_args=True,
        supports_check_mode=True,
        required_one_of=[['cert', 'cert_path'], ['privatekey', 'privatekey_path']]
    )

    path = module.params['path']
    base_dir = os.path.dirname(module.params['path'])

    if not os.path.isdir(base_dir):
        module.fail_json(name=path, msg='The directory %s does not exist' % path)

    pkcs12 = PKCS12(module)

    if module.params['state'] == 'present':
        if module.check_mode:
            result = pkcs12.dump()
            result['changed'] = module.params['force'] or not os.path.exists(path) or not pkcs12.compare()
            module.exit_json(**result)
        try:
            pkcs12.generate()
        except PKCS12Error as exc:
            module.fail_json(msg=to_native(exc))

    else:
        if module.check_mode:
            result = pkcs12.dump()
            result['changed'] = os.path.exists(path)
            module.exit_json(**result)
        try:
            pkcs12.remove()
        except PKCS12Error as exc:
            module.fail_json(msg=to_native(exc))

    result = pkcs12.dump()
    module.exit_json(**result)


if __name__ == "__main__":
    main()