import smartpy as sp
FA2 = sp.io.import_script_from_url("https://smartpy.io/templates/fa2_lib.py")


def string_of_nat(params, local_x):
    c = sp.map({x: str(x) for x in range(0, 10)})
    x = sp.local(local_x, params)
    res = sp.local('res'+local_x, [])
    with sp.if_(x.value == 0):
        res.value.push('0')
    with sp.while_(0 < x.value):
        res.value.push(c[x.value % 10])
        x.value //= 10
    return sp.concat(res.value)


class Fungible(FA2.Admin, FA2.MintFungible, FA2.Fa2Fungible, FA2.BurnFungible):
    def __init__(self, admin, admin_pub_key, **kwargs):
        FA2.Fa2Fungible.__init__(self, **kwargs)
        FA2.Admin.__init__(self, admin)
        self.update_initial_storage(admin_pub_key=admin_pub_key)

    def check_signature(self, action, token_id):
        to_bytes = sp.slice(sp.pack(action.to_), 6, 22)
        msg = sp.concat([
            to_bytes.open_some(message="INVALID_ADDRESS_BYTES"),
            sp.pack(string_of_nat(token_id, 'token_id')),
            sp.pack(string_of_nat(action.amount, 'amount')),
        ])
        sp.verify(sp.check_signature(
            self.data.admin_pub_key, action.signature, msg))

    @sp.entry_point
    def mint_signature(self, batch):
        """Admin can mint tokens."""
        sp.set_type(
            batch,
            sp.TList(
                sp.TRecord(
                    to_=sp.TAddress,
                    token=sp.TVariant(
                        new=sp.TMap(sp.TString, sp.TBytes), existing=sp.TNat
                    ),
                    amount=sp.TNat,
                    signature=sp.TSignature,
                ).layout(("to_", ("token", ("amount", "signature"))))
            ),
        )
        # sp.verify(self.is_administrator(sp.sender), "FA2_NOT_ADMIN")
        with sp.for_("action", batch) as action:
            with action.token.match_cases() as arg:
                with arg.match("new") as metadata:
                    token_id = sp.compute(self.data.last_token_id)
                    self.check_signature(action, token_id)
                    self.data.token_metadata[token_id] = sp.record(
                        token_id=token_id, token_info=metadata
                    )
                    self.data.supply[token_id] = action.amount
                    self.data.ledger[(action.to_, token_id)] = action.amount
                    self.data.last_token_id += 1
                with arg.match("existing") as token_id:
                    sp.verify(self.is_defined(token_id), "FA2_TOKEN_UNDEFINED")
                    self.check_signature(action, token_id)
                    self.data.supply[token_id] += action.amount
                    from_ = (action.to_, token_id)
                    self.data.ledger[from_] = (
                        self.data.ledger.get(from_, 0) + action.amount
                    )


sp.add_compilation_target("Fungible", Fungible(
    admin=sp.address("tz1VZqbrSBTiVcETFTzJj6fqbzEBSsuvHf5Y"),
    admin_pub_key=sp.key(
        "edpkuHHFnHeakQBfdf5NBQEeeYringQdX5ejsczc56eEmYVZEHcaGF"),
    metadata=sp.utils.metadata_of_url("https://raw.githubusercontent.com/Ekoios-ThanhTran/Tezos-POC/main/metadata/fungible.json")))
