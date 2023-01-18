import smartpy as sp
FA2 = sp.io.import_script_from_url(
    "https://smartpy.io/dev/templates/fa2_lib.py")

def string_of_nat(params):
    c   = sp.map({x : str(x) for x in range(0, 10)})
    x   = sp.local('x', params)
    res = sp.local('res', [])
    with sp.if_(x.value == 0):
        res.value.push('0')
    with sp.while_(0 < x.value):
        res.value.push(c[x.value % 10])
        x.value //= 10
    return sp.concat(res.value)


class SingleAsset(FA2.Admin, FA2.MintSingleAsset, FA2.Fa2SingleAsset, FA2.BurnSingleAsset):
    def __init__(self, admin, admin_pub_key, **kwargs):
        FA2.Fa2SingleAsset.__init__(self, **kwargs)
        FA2.Admin.__init__(self, admin)
        self.update_initial_storage(admin_pub_key=admin_pub_key)

    @sp.entry_point
    def mint_signature(self, batch):
        """Admin can mint tokens."""
        sp.set_type(
            batch,
            sp.TList(
                sp.TRecord(to_=sp.TAddress, amount=sp.TNat, signature=sp.TSignature).layout(
                    ("to_", ("amount", "signature")))
            ),
        )
        # sp.verify(self.is_administrator(sp.sender), "FA2_NOT_ADMIN")
        with sp.for_("action", batch) as action:
            sp.verify(self.is_defined(0), "FA2_TOKEN_UNDEFINED")
            to_bytes = sp.slice(sp.pack(action.to_), 6, 22)
            # sp.verify(to_bytes.is_some(), "INVALID_ADDRESS_BYTES")
            msg = sp.concat([to_bytes.open_some(message = "INVALID_ADDRESS_BYTES"), sp.pack(string_of_nat(action.amount))])
            sp.verify(sp.check_signature(
                self.data.admin_pub_key, action.signature, msg))
            # self.data.msg=msg
            self.data.supply += action.amount
            self.data.ledger[action.to_] = (
                self.data.ledger.get(action.to_, 0) + action.amount
            )


sp.add_compilation_target("SingleAsset", SingleAsset(
    admin=sp.address("tz1VZqbrSBTiVcETFTzJj6fqbzEBSsuvHf5Y"),
    admin_pub_key=sp.key(
        "edpkuHHFnHeakQBfdf5NBQEeeYringQdX5ejsczc56eEmYVZEHcaGF"),
    metadata=sp.utils.metadata_of_url(
        "https://raw.githubusercontent.com/Ekoios-ThanhTran/Tezos-POC/main/metadata/singleAsset.json"),
    token_metadata=sp.map({"": sp.utils.bytes_of_string(
        "https://gitlab.com/tezos/tzip/-/raw/master/proposals/tzip-21/examples/example-010-fungible-tz21.json")})
))
