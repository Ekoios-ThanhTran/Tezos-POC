import smartpy as sp
FA2 = sp.io.import_script_from_url("https://smartpy.io/dev/templates/fa2_lib.py")

class Nft(FA2.Admin, FA2.MintNft, FA2.Fa2Nft):
    def __init__(self, admin, **kwargs):
        FA2.Fa2Nft.__init__(self, **kwargs)
        FA2.Admin.__init__(self, admin)

sp.add_compilation_target("Nft", Nft(
    admin=sp.address("tz1VZqbrSBTiVcETFTzJj6fqbzEBSsuvHf5Y"),
    metadata=sp.utils.metadata_of_url("https://raw.githubusercontent.com/Ekoios-ThanhTran/tezos-contract/main/metadata/fa2.json")))
