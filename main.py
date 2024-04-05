from blockChainAccount import blockChainAccount


def save_wallet_info_to_file(info='', file_path=''):
    with open(file_path, 'a') as file:
        file.write(f"{info}\n")


def save_wallets(file_name, num_wallets):
    file_path = f'{file_name}.txt'  # 修改为实际的文件路径
    for _ in range(num_wallets):
        bca = blockChainAccount.BlockChainAccount().generate_wallet_info()
        print(bca)
        save_wallet_info_to_file(bca, file_path)
    print(f"Successfully generated and saved {num_wallets} wallets to {file_path}")


# 调用函数示例
save_wallets('new_wallets', 10)  # create 10 accounts, saving in new_wallets.txt
