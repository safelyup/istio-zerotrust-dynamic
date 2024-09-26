import jwcrypto.jwk as jwk

RSAkey_ext = jwk.JWK.generate(kty='RSA', size=4096)
ext_private_key = RSAkey_ext.export_private()
ext_public_key = RSAkey_ext.export_public()

RSAkey_int = jwk.JWK.generate(kty='RSA', size=4096)
int_private_key = RSAkey_int.export_private()
int_public_key = RSAkey_int.export_public()
int_jwks = '{"keys":[' + int_public_key + ']}'

print("\nprivate external (for auth server):\n" + ext_private_key)
print("\npublic external (for internal auth):\n" + ext_public_key)

print("\nprivate internal (for internal auth):\n" + int_private_key)
print("\nistio jwks internal (for internal services):\n" + int_jwks)
