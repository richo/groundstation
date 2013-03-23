groundstation uses RSA under the hood with (planned for now) experimental
support for ECDSA.

The rationale for this is that while other algorithms are more practical in
many ways, RSA keys are the most widespread amongst developers, and being able
to use your ssh keys as an identity will hopefully make significant strides
toward adoption. (See for example https://github.com/richo.keys)

We make sweeping assumptions about how we can verify data, namely that we can
ignore hashing algorithms and length extension attacks. Where it's reasonable
we assert that you not only have a 40 character SHA1 hash, but also one that
points to a valid object
