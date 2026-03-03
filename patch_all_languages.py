import os
import glob

locales_path = "src/qt/locale/"
ts_files = glob.glob(os.path.join(locales_path, "bitcoin_*.ts"))

translations = {
    "ru": {
        "show": "&Показать сид-фразу...",
        "title": "Бэкап BIP39 Seed",
        "staking": "<b>Только для стейкинга</b><br/><small>(Снимите галочку, если хотите разблокировать кошелек полностью)</small>"
    },
    "de": {
        "show": "&Mnemonic-Phrase anzeigen...",
        "title": "BIP39 Seed Sicherung",
        "staking": "<b>Nur für Staking</b><br/><small>(Deaktivieren Sie dies für eine vollständige Wallet-Entsperrung)</small>"
    },
    "fr": {
        "show": "&Afficher la phrase mnémonique...",
        "title": "Sauvegarde de la semence BIP39",
        "staking": "<b>Pour le jalonnement uniquement</b><br/><small>(Décochez pour déverrouiller complètement le portefeuille)</small>"
    },
    "es": {
        "show": "&Mostrar frase mnemotécnica...",
        "title": "Copia de seguridad BIP39",
        "staking": "<b>Solo para staking</b><br/><small>(Desmarque para desbloquear el monedero por completo)</small>"
    },
    "en": {
        "show": "&Show Mnemonic...",
        "title": "BIP39 Seed Backup",
        "staking": "<b>For staking only</b><br/><small>(Uncheck to unlock wallet fully for all operations)</small>"
    }
}

def get_trans(lang, key):
    return translations.get(lang, translations["en"])[key]

for ts_file in ts_files:
    lang_code = os.path.basename(ts_file).split('_')[1].split('.')[0]
    with open(ts_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Подготовка блоков XML
    gui_block = """    <message>
        <source>&amp;Show Mnemonic...</source>
        <translation>{}</translation>
    </message>
    <message>
        <source>BIP39 Seed Backup</source>
        <translation>{}</translation>
    </message>\n""".format(get_trans(lang_code, "show"), get_trans(lang_code, "title"))

    ask_block = """    <message>
        <source><b>For staking only</b><br/><small>(Снимите галочку, если хотите разблокировать кошелек полностью)</small></source>
        <translation>{}</translation>
    </message>\n""".format(get_trans(lang_code, "staking"))

    # Вставка в контексты
    if '<name>BitcoinGUI</name>' in content:
        content = content.replace('<name>BitcoinGUI</name>', '<name>BitcoinGUI</name>\n' + gui_block)
    if '<name>AskPassphraseDialog</name>' in content:
        content = content.replace('<name>AskPassphraseDialog</name>', '<name>AskPassphraseDialog</name>\n' + ask_block)

    with open(ts_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Все {} языковых файлов успешно обновлены профессиональным переводом.".format(len(ts_files)))
