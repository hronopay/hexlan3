import os

file_path = "src/wallet.cpp"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Патч 1: GenerateNewKey
old_1 = """    if (!strMnemonic.empty()) {
        std::vector<uint8_t> vchSeed;
        SecureString secureMnemonic(strMnemonic.begin(), strMnemonic.end());
        SecureString securePassphrase(strMnemonicPassphrase.begin(), strMnemonicPassphrase.end());
        BIP39::MnemonicToSeed(secureMnemonic, securePassphrase, vchSeed);
        
        CExtKey masterKey;
        masterKey.SetMaster(&vchSeed[0], vchSeed.size());

        // Стандарт деривации BIP44: m / 44' / 0' / 0' / 0 / nBip39Counter
        // 0x80000000 означает hardened (усиленную) деривацию
        CExtKey purposeKey, coinTypeKey, accountKey, changeKey, childKey;
        masterKey.Derive(purposeKey, 84 | 0x80000000); // BIP84 Native SegWit
        purposeKey.Derive(coinTypeKey, 0 | 0x80000000);
        coinTypeKey.Derive(accountKey, 0 | 0x80000000);
        accountKey.Derive(changeKey, 0); // Внешние адреса (change = 0)
        changeKey.Derive(childKey, nBip39Counter);

        secret = childKey.key;
        
        // Увеличиваем счетчик выданных адресов и фиксируем его в БД
        nBip39Counter++;
        CWalletDB(strWalletFile).WriteBip39Counter(nBip39Counter);
    } else {
        // Резервный механизм случайной генерации до ввода сид-фразы
        secret.MakeNewKey(fCompressed);
    }"""

new_1 = """    if (strMnemonic.empty()) {
        throw std::runtime_error("CWallet::GenerateNewKey() : Wallet is not initialized with BIP39 seed phrase");
    }

    std::vector<uint8_t> vchSeed;
    SecureString secureMnemonic(strMnemonic.begin(), strMnemonic.end());
    SecureString securePassphrase(strMnemonicPassphrase.begin(), strMnemonicPassphrase.end());
    BIP39::MnemonicToSeed(secureMnemonic, securePassphrase, vchSeed);
    
    CExtKey masterKey;
    masterKey.SetMaster(&vchSeed[0], vchSeed.size());

    // Стандарт деривации BIP44: m / 44' / 0' / 0' / 0 / nBip39Counter
    // 0x80000000 означает hardened (усиленную) деривацию
    CExtKey purposeKey, coinTypeKey, accountKey, changeKey, childKey;
    masterKey.Derive(purposeKey, 84 | 0x80000000); // BIP84 Native SegWit
    purposeKey.Derive(coinTypeKey, 0 | 0x80000000);
    coinTypeKey.Derive(accountKey, 0 | 0x80000000);
    accountKey.Derive(changeKey, 0); // Внешние адреса (change = 0)
    changeKey.Derive(childKey, nBip39Counter);

    secret = childKey.key;
    
    // Увеличиваем счетчик выданных адресов и фиксируем его в БД
    nBip39Counter++;
    CWalletDB(strWalletFile).WriteBip39Counter(nBip39Counter);"""

if old_1 in content:
    content = content.replace(old_1, new_1)
else:
    print("Ошибка: Блок 1 не найден")

# Патч 2: TopUpKeyPool
old_2 = """    // Hexlan: Если кошелек еще не инициализирован HD-фразой, генерируем только 1 резервный ключ
    if (strMnemonic.empty())
        nTargetSize = 1;
        else
            nTargetSize = max(GetArg("-keypool", 100), (int64_t)0);"""

new_2 = """    // Hexlan: Жесткий превентивный запрет на генерацию пула ключей до ввода сид-фразы
    if (strMnemonic.empty())
        return true;

    nTargetSize = max(GetArg("-keypool", 100), (int64_t)0);"""

if old_2 in content:
    content = content.replace(old_2, new_2)
else:
    print("Ошибка: Блок 2 не найден")

# Патч 3: GetKeyFromPool
old_3 = """bool CWallet::GetKeyFromPool(CPubKey& result)
{
    int64_t nIndex = 0;
    CKeyPool keypool;
    {
        LOCK(cs_wallet);
        ReserveKeyFromKeyPool(nIndex, keypool);"""

new_3 = """bool CWallet::GetKeyFromPool(CPubKey& result)
{
    int64_t nIndex = 0;
    CKeyPool keypool;
    {
        LOCK(cs_wallet);

        if (strMnemonic.empty())
            return false;

        ReserveKeyFromKeyPool(nIndex, keypool);"""

if old_3 in content:
    content = content.replace(old_3, new_3)
else:
    print("Ошибка: Блок 3 не найден")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("wallet.cpp успешно пропатчен для превентивной блокировки генерации ключей!")
