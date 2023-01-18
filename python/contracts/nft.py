import smartpy as sp
FA2 = sp.io.import_script_from_url(
    "https://smartpy.io/dev/templates/fa2_lib.py")


def string_of_nat(params):
    c = sp.map({x: str(x) for x in range(0, 10)})
    x = sp.local('x', params)
    res = sp.local('res', [])
    with sp.if_(x.value == 0):
        res.value.push('0')
    with sp.while_(0 < x.value):
        res.value.push(c[x.value % 10])
        x.value //= 10
    return sp.concat(res.value)


class Nft(FA2.Admin, FA2.MintNft, FA2.Fa2Nft, FA2.BurnNft):
    def __init__(self, admin, admin_pub_key, **kwargs):
        FA2.Fa2Nft.__init__(self, **kwargs)
        FA2.Admin.__init__(self, admin)
        self.update_initial_storage(admin_pub_key=admin_pub_key)

    @sp.entry_point
    def mint_signature(self, batch):
        """Admin can mint new or existing tokens."""
        sp.set_type(
            batch,
            sp.TList(
                sp.TRecord(
                    to_=sp.TAddress,
                    metadata=sp.TMap(sp.TString, sp.TBytes),
                    signature=sp.TSignature,
                ).layout(("to_", ("metadata", "signature")))
            ),
        )
        # sp.verify(self.is_administrator(sp.sender), "FA2_NOT_ADMIN")
        with sp.for_("action", batch) as action:
            token_id = sp.compute(self.data.last_token_id)
            to_bytes = sp.slice(sp.pack(action.to_), 6, 22)
            msg = sp.concat([to_bytes.open_some(
                message="INVALID_ADDRESS_BYTES"), sp.pack(string_of_nat(token_id))])
            sp.verify(sp.check_signature(
                self.data.admin_pub_key, action.signature, msg))

            metadata = sp.record(token_id=token_id, token_info=action.metadata)
            self.data.token_metadata[token_id] = metadata
            self.data.ledger[token_id] = action.to_
            self.data.last_token_id += 1


sp.add_compilation_target("Nft", Nft(
    admin=sp.address("tz1VZqbrSBTiVcETFTzJj6fqbzEBSsuvHf5Y"),
    admin_pub_key=sp.key(
        "edpkuHHFnHeakQBfdf5NBQEeeYringQdX5ejsczc56eEmYVZEHcaGF"),
    metadata=sp.utils.metadata_of_url("https://raw.githubusercontent.com/Ekoios-ThanhTran/Tezos-POC/main/metadata/nft.json")))
