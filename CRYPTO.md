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

## Sync Strategy

In the name of being reasonable, it should probably be possible to run a node
with two different sync stragegies, to match both your intent and some security
concerns:

#### Paranoid

In this mode, the sync procedure should be as follows:

1. LISTALLCHANNELS from peer
2. Inspect all tips, discard all signatures that aren't trusted
3. Fetch all missing objects in that set of tips
4. Fetch all their parents which are missing, etc.

This leaves you with a fairly git-ish lazy sync, but with some protection
against people feeding you terrabyte long objects.

#### Eager

Basically, sync as it currently stands.
