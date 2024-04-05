from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, base58, Bip44Changes


class BlockChainAccount():

    def __init__(self, mnemonic='', coin_type=Bip44Coins.ETHEREUM, password='') -> None:

        self.mnemonic = mnemonic.strip()
        self.coin_type = coin_type
        self.password = password  # if have password

    @staticmethod
    def generate_mnemonic(strength=128):
        # 创建助记词
        mnemo = Mnemonic("english")
        return mnemo.generate(strength=strength)

    def get_address_pk(self):
        seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate(self.password)
        if self.coin_type != Bip44Coins.SOLANA:
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, self.coin_type).DeriveDefaultPath()
            return bip44_mst_ctx.PublicKey().ToAddress(), bip44_mst_ctx.PrivateKey().Raw().ToHex()
        else:
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, self.coin_type)

            bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
            bip44_chg_ctx = bip44_acc_ctx.Change(
                Bip44Changes.CHAIN_EXT)  # if you use "Solflare", remove this line and make a simple code modify and test
            priv_key_bytes = bip44_chg_ctx.PrivateKey().Raw().ToBytes()
            public_key_bytes = bip44_chg_ctx.PublicKey().RawCompressed().ToBytes()[1:]
            key_pair = priv_key_bytes + public_key_bytes

            return bip44_chg_ctx.PublicKey().ToAddress(), base58.Base58Encoder.Encode(key_pair)

    def generate_wallet_info(self):
        if self.mnemonic == '':
            self.mnemonic = BlockChainAccount.generate_mnemonic()
        # print(f'mnemonic: {self.mnemonic}')
        output = f'MNEMONIC: {self.mnemonic}\n'
        coin_types = {
            Bip44Coins.ETHEREUM: 'ethereum(evm)',
            Bip44Coins.SOLANA: 'solana',
            # Bip44Coins.TERRA: 'luna',
            # Bip44Coins.DASH: 'dash',
            # .....
            # also support other chain, such as file coin, eth classic, doge, dash, luna ....
            # example change coin_type as Bip44Coins.EOS, Bip44Coins.TERRA .....

        }
        for coin_type in coin_types.keys():
            chain_name = coin_types[coin_type]
            bca = BlockChainAccount(mnemonic=self.mnemonic, coin_type=coin_type)
            address, pk = bca.get_address_pk()
            # print(f'{chain_name} mainnet address: {address}, private key: {pk}\n')
            output = output + f'{chain_name.upper()} mainnet address: {address}\nPrivate key: {pk}\n'
        return output


if __name__ == "__main__":
    my_mnemonic = """
    tail inside tell hundred student accuse point spice useful august until toilet
    """
    bca = BlockChainAccount(mnemonic=my_mnemonic)
    print(bca.generate_wallet_info())
