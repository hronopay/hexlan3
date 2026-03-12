#include "blockbrowser.h"
#include "ui_blockbrowser.h"
#include "main.h"
#include "wallet.h"
#include "base58.h"
#include "clientmodel.h"
#include "walletmodel.h"
#include "rpcconsole.h"
#include "transactionrecord.h"
#include "bech32.h"
#include "segwit_addr.h"

#include <sstream>
#include <string>
#include <iomanip>

// HEXLAN: Локальная конвертация 8-bit в 5-bit для Bech32
namespace {
    bool ConvertBits8to5(const std::vector<uint8_t>& in, std::vector<uint8_t>& out) {
        uint32_t val = 0;
        int bits = 0;
        for (size_t i = 0; i < in.size(); ++i) {
            val = (val << 8) | in[i];
            bits += 8;
            while (bits >= 5) {
                out.push_back((uint8_t)((val >> (bits - 5)) & 31));
                bits -= 5;
            }
        }
        if (bits > 0) {
            out.push_back((uint8_t)((val << (5 - bits)) & 31));
        }
        return true;
    }
}

// HEXLAN: Универсальный экстрактор адресов для UI
static std::string ExtractUIAddress(const CScript& scriptPubKey, const std::string& fallback) {
    if (scriptPubKey.size() == 22 && scriptPubKey[0] == 0x00 && scriptPubKey[1] == 0x14) {
        std::vector<uint8_t> program(scriptPubKey.begin() + 2, scriptPubKey.end());
        std::vector<uint8_t> data;
        data.push_back(0); // Witness version 0
        std::vector<uint8_t> conv;
        ConvertBits8to5(program, conv);
        data.insert(data.end(), conv.begin(), conv.end());
        return bech32::Encode("hx", data);
    }
    
    CTxDestination address;
    if (ExtractDestination(scriptPubKey, address)) {
        if (const CKeyID* keyID = boost::get<CKeyID>(&address)) {
            std::vector<uint8_t> program(keyID->begin(), keyID->end());
            std::vector<uint8_t> data;
            data.push_back(0); // Witness version 0
            std::vector<uint8_t> conv;
            ConvertBits8to5(program, conv);
            data.insert(data.end(), conv.begin(), conv.end());
            return bech32::Encode("hx", data);
        }
        return EncodeDestination(address);
    }
    
    return fallback;
}

double getBlockHardness(int height)
{
    const CBlockIndex* blockindex = getBlockIndex(height);

    int nShift = (blockindex->nBits >> 24) & 0xff;

    double dDiff =
        (double)0x0000ffff / (double)(blockindex->nBits & 0x00ffffff);

    while (nShift < 29)
    {
        dDiff *= 256.0;
        nShift++;
    }
    while (nShift > 29)
    {
        dDiff /= 256.0;
        nShift--;
    }

    return dDiff;
}

int getBlockHashrate(int height)
{
    int lookup = height;

    double timeDiff = getBlockTime(height) - getBlockTime(1);
    double timePerBlock = timeDiff / lookup;

    return (boost::int64_t)(((double)getBlockHardness(height) * pow(2.0, 32)) / timePerBlock);
}

const CBlockIndex* getBlockIndex(int height)
{
    std::string hex = getBlockHash(height);
    uint256 hash(hex);
    return mapBlockIndex[hash];
}

std::string getBlockHash(int Height)
{
    if(Height > pindexBest->nHeight) { return "351c6703813172725c6d660aa539ee6a3d7a9fe784c87fae7f36582e3b797058"; }
    if(Height < 0) { return "351c6703813172725c6d660aa539ee6a3d7a9fe784c87fae7f36582e3b797058"; }
    int desiredheight;
    desiredheight = Height;
    if (desiredheight < 0 || desiredheight > nBestHeight)
        return 0;

    CBlock block;
    CBlockIndex* pblockindex = mapBlockIndex[hashBestChain];
    while (pblockindex->nHeight > desiredheight)
        pblockindex = pblockindex->pprev;
    return pblockindex->phashBlock->GetHex();
}

int getBlockTime(int Height)
{
    std::string strHash = getBlockHash(Height);
    uint256 hash(strHash);

    if (mapBlockIndex.count(hash) == 0)
        return 0;

    CBlock block;
    CBlockIndex* pblockindex = mapBlockIndex[hash];
    return pblockindex->nTime;
}

std::string getBlockMerkle(int Height)
{
    std::string strHash = getBlockHash(Height);
    uint256 hash(strHash);

    if (mapBlockIndex.count(hash) == 0)
        return 0;

    CBlock block;
    CBlockIndex* pblockindex = mapBlockIndex[hash];
    return pblockindex->hashMerkleRoot.ToString().substr(0,10).c_str();
}

int getBlocknBits(int Height)
{
    std::string strHash = getBlockHash(Height);
    uint256 hash(strHash);

    if (mapBlockIndex.count(hash) == 0)
        return 0;

    CBlock block;
    CBlockIndex* pblockindex = mapBlockIndex[hash];
    return pblockindex->nBits;
}

int getBlockNonce(int Height)
{
    std::string strHash = getBlockHash(Height);
    uint256 hash(strHash);

    if (mapBlockIndex.count(hash) == 0)
        return 0;

    CBlock block;
    CBlockIndex* pblockindex = mapBlockIndex[hash];
    return pblockindex->nNonce;
}

std::string getBlockDebug(int Height)
{
    std::string strHash = getBlockHash(Height);
    uint256 hash(strHash);

    if (mapBlockIndex.count(hash) == 0)
        return 0;

    CBlock block;
    CBlockIndex* pblockindex = mapBlockIndex[hash];
    return pblockindex->ToString();
}

int blocksInPastHours(int hours)
{
    int wayback = hours * 3600;
    bool check = true;
    int height = pindexBest->nHeight;
    int heightHour = pindexBest->nHeight;
    int utime = (int)time(NULL);
    int target = utime - wayback;

    while(check)
    {
        if(getBlockTime(heightHour) < target)
        {
            check = false;
            return height - heightHour;
        } else {
            heightHour = heightHour - 1;
        }
    }

    return 0;
}

double convertCoins(int64_t amount)
{
    return (double)amount / (double)COIN;
}

double getTxTotalValue(std::string txid)
{
    uint256 hash;
    hash.SetHex(txid);

    CTransaction tx;
    uint256 hashBlock = 0;
    if (!GetTransaction(hash, tx, hashBlock))
        return 0.0;

    double value = 0;
    for (unsigned int i = 0; i < tx.vout.size(); i++)
    {
        value += convertCoins(tx.vout[i].nValue);
    }
    return value;
}

std::string getOutputs(std::string txid)
{
    uint256 hash;
    hash.SetHex(txid);

    CTransaction tx;
    uint256 hashBlock = 0;
    if (!GetTransaction(hash, tx, hashBlock))
        return "Transaction not found (requires -txindex=1)\n";

    std::string str = "";
    for (unsigned int i = 0; i < tx.vout.size(); i++)
    {
        const CTxOut& txout = tx.vout[i];
        std::string addrStr = ExtractUIAddress(txout.scriptPubKey, "Unknown/Non-Standard");
        
        double buffer = convertCoins(txout.nValue);
        std::ostringstream ss;
        ss << std::fixed << std::setprecision(4) << buffer;
        str += addrStr + ": " + ss.str() + " HEXLAN\n";
    }

    return str;
}

std::string getInputs(std::string txid)
{
    uint256 hash;
    hash.SetHex(txid);

    CTransaction tx;
    uint256 hashBlock = 0;
    if (!GetTransaction(hash, tx, hashBlock))
        return "Transaction not found (requires -txindex=1)\n";

    if (tx.IsCoinBase())
        return "Coinbase (Mined)\n";

    std::string str = "";
    for (unsigned int i = 0; i < tx.vin.size(); i++)
    {
        const CTxIn& vin = tx.vin[i];
        uint256 prevHash = vin.prevout.hash;
        
        CTransaction wtxPrev;
        uint256 hashBlockPrev = 0;
        if (!GetTransaction(prevHash, wtxPrev, hashBlockPrev)) {
            str += "Unknown Input: ? HEXLAN\n";
            continue;
        }

        if (vin.prevout.n < wtxPrev.vout.size()) {
            const CTxOut& prevOut = wtxPrev.vout[vin.prevout.n];
            std::string addrStr = ExtractUIAddress(prevOut.scriptPubKey, "Unknown");
            
            double buffer = convertCoins(prevOut.nValue);
            std::ostringstream ss;
            ss << std::fixed << std::setprecision(4) << buffer;
            str += addrStr + ": " + ss.str() + " HEXLAN\n";
        }
    }

    return str;
}

int64_t getInputValue(CTransaction tx, CScript target)
{
    for (unsigned int i = 0; i < tx.vout.size(); i++)
    {
        const CTxOut& txout = tx.vout[i];
        if(txout.scriptPubKey == target)
        {
            return txout.nValue;
        }
    }
    return 0;
}

double getTxFees(std::string txid)
{
    uint256 hash;
    hash.SetHex(txid);

    CTransaction tx;
    uint256 hashBlock = 0;
    if (!GetTransaction(hash, tx, hashBlock))
        return 0.0;

    if (tx.IsCoinBase()) return 0.0; // No fee for mining

    double valueOut = 0;
    for (unsigned int i = 0; i < tx.vout.size(); i++) {
        valueOut += convertCoins(tx.vout[i].nValue);
    }

    double valueIn = 0;
    for (unsigned int i = 0; i < tx.vin.size(); i++)
    {
        uint256 prevHash = tx.vin[i].prevout.hash;
        CTransaction wtxPrev;
        uint256 hashBlockPrev = 0;
        if (GetTransaction(prevHash, wtxPrev, hashBlockPrev)) {
             if (tx.vin[i].prevout.n < wtxPrev.vout.size()) {
                 valueIn += convertCoins(wtxPrev.vout[tx.vin[i].prevout.n].nValue);
             }
        }
    }

    double fee = valueIn - valueOut;
    // Coinstake transactions have negative fee (Output > Input), so return 0
    if (fee < 0) return 0.0; 
    
    return fee;
}


BlockBrowser::BlockBrowser(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::BlockBrowser)
{
    ui->setupUi(this);

    setFixedSize(400, 420);
        
    connect(ui->blockButton, SIGNAL(pressed()), this, SLOT(blockClicked()));
    connect(ui->txButton, SIGNAL(pressed()), this, SLOT(txClicked()));
}

// HEXLAN: Функция вызывается снаружи (из BitcoinGUI) для автопоиска
void BlockBrowser::setSearchQuery(QString query)
{
    ui->txBox->setText(query);
    updateExplorer(false);
}

void BlockBrowser::updateExplorer(bool block)
{    
    if(block)
    {
        ui->heightLabel->show();
        ui->heightLabel_2->show();
        ui->hashLabel->show();
        ui->hashBox->show();
        ui->merkleLabel->show();
        ui->merkleBox->show();
        ui->nonceLabel->show();
        ui->nonceBox->show();
        ui->bitsLabel->show();
        ui->bitsBox->show();
        ui->timeLabel->show();
        ui->timeBox->show();
        ui->hardLabel->show();
        ui->hardBox->show();;
        int height = ui->heightBox->value();
        if (height > pindexBest->nHeight)
        {
            ui->heightBox->setValue(pindexBest->nHeight);
            height = pindexBest->nHeight;
        }
        std::string hash = getBlockHash(height);
        std::string merkle = getBlockMerkle(height);
        int nBits = getBlocknBits(height);
        int nNonce = getBlockNonce(height);
        int atime = getBlockTime(height);
        double hardness = getBlockHardness(height);
        QString QHeight = QString::number(height);
        QString QHash = QString::fromUtf8(hash.c_str());
        QString QMerkle = QString::fromUtf8(merkle.c_str());
        QString QBits = QString::number(nBits);
        QString QNonce = QString::number(nNonce);
        QString QTime = QString::number(atime);
        QString QHardness = QString::number(hardness, 'f', 6);
        ui->heightLabel->setText(QHeight);
        ui->hashBox->setText(QHash);
        ui->merkleBox->setText(QMerkle);
        ui->bitsBox->setText(QBits);
        ui->nonceBox->setText(QNonce);
        ui->timeBox->setText(QTime);     
        ui->hardBox->setText(QHardness);
    } 
    else 
    {
        ui->txID->show();
        ui->txLabel->show();
        ui->valueLabel->show();
        ui->valueBox->show();
        ui->inputLabel->show();
        ui->inputBox->show();
        ui->outputLabel->show();
        ui->outputBox->show();
        ui->feesLabel->show();
        ui->feesBox->show();
        
        std::string query = ui->txBox->text().trimmed().toUtf8().constData();
        uint256 hash;
        hash.SetHex(query);

        // HEXLAN: Умное распознавание (Хэш Блока или Хэш Транзакции)
        if (mapBlockIndex.count(hash) > 0) {
            // Это Хэш Блока!
            CBlockIndex* pblockindex = mapBlockIndex[hash];
            CBlock blockData;
            ReadBlockFromDisk(blockData, pblockindex); // Читаем сам блок с диска, чтобы достать транзакции

            ui->txLabel->setText("Block Hash:");
            ui->txID->setText(QString::fromStdString(query));
            
            ui->valueLabel->setText("Block Height:");
            ui->valueBox->setText(QString::number(pblockindex->nHeight));
            
            ui->feesLabel->setText("Tx Count:");
            ui->feesBox->setText(QString::number(blockData.vtx.size()));
            
            ui->inputLabel->setText("Block Time:");
            ui->inputBox->setText(QString::number(pblockindex->nTime));

            ui->outputLabel->setText("Transactions:");
            std::string txList = "";
            for (unsigned int i = 0; i < blockData.vtx.size(); i++) {
                txList += blockData.vtx[i].GetHash().GetHex() + "\n";
            }
            ui->outputBox->setText(QString::fromStdString(txList));
        } else {
            // Это обычная Транзакция
            ui->txLabel->setText("Transaction ID:");
            ui->valueLabel->setText("Value out:");
            ui->feesLabel->setText("Fees:");
            ui->inputLabel->setText("Inputs:");
            ui->outputLabel->setText("Outputs:");

            double value = getTxTotalValue(query);
            double fees = getTxFees(query);
            std::string outputs = getOutputs(query);
            std::string inputs = getInputs(query);
            
            QString QValue = QString::number(value, 'f', 6);
            QString QID = QString::fromUtf8(query.c_str());
            QString QOutputs = QString::fromUtf8(outputs.c_str());
            QString QInputs = QString::fromUtf8(inputs.c_str());
            QString QFees = QString::number(fees, 'f', 6);
            
            ui->valueBox->setText(QValue + " HEXLAN");
            ui->txID->setText(QID);
            ui->outputBox->setText(QOutputs);
            ui->inputBox->setText(QInputs);
            ui->feesBox->setText(QFees + " HEXLAN");
        }
    }
}


void BlockBrowser::txClicked()
{
    updateExplorer(false);
}

void BlockBrowser::blockClicked()
{
    updateExplorer(true);
}

void BlockBrowser::setModel(WalletModel *model)
{
    this->model = model;
}

BlockBrowser::~BlockBrowser()
{
    delete ui;
}