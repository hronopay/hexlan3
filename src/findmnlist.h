#include <string>
#include <vector>
#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <string.h>
//#include <conio.h>

using namespace std;

static const int LBLOCK=3;
static const unsigned int SIGNALON=10286;
static const unsigned int SIGNALOFF=20219;
static const unsigned int LOCKFROM=2095091600; //  1595091600 = 07/18/2020T17:00:00// - time to lock from in historical list 
static const unsigned int STARTCHECKTX2=30000; // 30k for bull
static const unsigned int NVACCEPTABLESHIFT=1000000; // 

string short0string = "0000000000000000000000000000000000";
string long0string = "0000000000000000000000000000000000000000000000000000000000000000";

int LDebug = GetArg("-ldebug", 0); 


class Char35Adr
{
public:
    char sca[35];
    Char35Adr(string scamadr){
        strcpy (sca, scamadr.c_str());
    }

    void f()
    {
        //cout << "Char35Adr::f - " << sca << endl;
        LogPrintf("Address:  %s \n", sca); 

    }

    string toString()
    {
        return sca;
    }

    int elemsize(){
        return sizeof(sca);
    }
};


class MnTxHash
{
public:
    char txha[65];
    MnTxHash(string txhash){
        strcpy (txha, txhash.c_str());
    }

    void f()
    {
        //cout << "MnTxHash::f - " << txha << endl;
        LogPrintf("MnTxHash::f -  %s \n", txha); 
    }

    string toString()
    {
        return txha;
    }

    int elemsize(){
        return sizeof(txha);
    }
};


class FindMnList
{
private:
    bool erasefirstisdone;
    int lastcollateral;
 
public:
    vector<Char35Adr> arr;
    vector<MnTxHash> txhash;
    vector<int> outInd;
    FindMnList(){
        erasefirstisdone = false;
        lastcollateral = 0;
        arr.push_back( Char35Adr(short0string) );
        outInd.push_back(0);
        txhash.push_back( MnTxHash(long0string) );
    }

    void reInitialyze(){
        if(erasefirstisdone){
            erasefirstisdone = false;
        }
        for(int k=0; k<this->sizeMn(); k++){
            outInd[k] = 0;
            arr[k] = Char35Adr(short0string);
            txhash[k] = MnTxHash(long0string);
        }
        for(int k=(this->sizeMn()-1); k>0; k--){
            this->erase(k);
            LogPrintf("reInitialyze(): ERASE k=%d \n", k);
        }
    }

    void checkCollateral(int currentColl){
        if(!lastcollateral) lastcollateral = currentColl;  // if this is first collateral we only initialyze lastcollateral value 
        else if(currentColl != lastcollateral) {
            lastcollateral = currentColl;
            this->reInitialyze();
        }
    }

    void vinit(string adr, string hash, int outputIndex){
        outInd.push_back( outputIndex ); 
        arr.push_back( Char35Adr(adr) ); 
        txhash.push_back( MnTxHash(hash) ); 
    }

    void eraseFirst(){
        if(!erasefirstisdone){
            outInd.erase(outInd.begin());
            arr.erase(arr.begin());
            txhash.erase(txhash.begin());
            erasefirstisdone = true;
        }
        else {
            if(fDebug) LogPrintf("   ___eraseFirst()___  HAS BEEN ERASED ALREADY \n");
        }

        return;
    }


    void erase(int k){
        outInd.erase(outInd.begin()+k);
        arr.erase(arr.begin()+k);
        txhash.erase(txhash.begin()+k);
        LogPrintf("   ___erase()___  done\n");
        return;
    }


    void print()
    {
        for(unsigned i = 0; i < arr.size(); ++i)
        {
            arr[i].f();
            txhash[i].f();
            LogPrintf("outInd = %d\n", outInd[i]);
        }
    }

    string getValueMn(int i)
    {
        return arr[i].toString();
    }

    int getValueOI(int i)
    {
        return outInd[i];
    }

    string getValueHash(int i)
    {
        return txhash[i].toString();
    }

    int sizeMn(){
        return arr.size()/* * sizeof(Char35Adr)*/;
    }

    int sizeHash(){
        return txhash.size()/* * sizeof(Char35Adr)*/;
    }
 /*
    void txtWrite(string path){
        ofstream fout;
        fout.open(path, ios::out | ios::trunc );  
        if(!fout.is_open()){
            cout << "txtWrite(): open out-file error" << endl;
        }
        else {
            if ( (fout.rdstate() & std::ofstream::failbit ) != 0 ) 
                cout << "txtWrite(): Error opening 'myfile.txt'\n";

            cout << "txtWrite(): out-file " << path << " was opened" << endl;
            //fout << "txtWrite(): Writing this to a file.\n";
            for(unsigned i=0; i<arr.size(); i++) fout << arr[i].toString() << "\n";
        }
        fout.close();
        return;
    }

    void binWrite(string path){
        ofstream fout;
        //    fout.open(path, ofstream::app);   //   ios::out | ios::app | ios::binary
        fout.open(path, ios::out | ios::trunc | ios::binary);  
        if(!fout.is_open()){
            cout << "binWrite(): open out-file error" << endl;
        }
        else {
            if ( (fout.rdstate() & std::ofstream::failbit ) != 0 ) cout << "binWrite(): Error opening 'myfile.bin'\n";

            cout << "binWrite(): out-file " << path << " was opened" << endl;
            fout.write((char*)&this->arr, this->size());
            cout << "binWrite(): " << this->size() << " bytes were written down" << endl;
        }
        fout.close();
        return;
    }


    void binRead(string path){
        ifstream fin;
        fin.open(path, ios::binary);
        if(!fin.is_open()){
            cout << "binRead(): open in-file error" << endl;
        }
        else {
            cout << "binRead(): in-file " << path << " was opened" << endl;
            cout << "binRead(): inadr.size is " << this->size() << endl;
            fin.read( (char*)&this->arr, this->size() );
        }
        fin.close();
        return;
    }
 */
};
 


/*
int main()
{
    // make vector supposedMnList  and fill the data in vector supposedMnList
    FindMnList supposedMnList;

    supposedMnList.vinit("BYJpT4Xv3zUCkL1E4bc1SYty99GBx5EoNR");
    supposedMnList.vinit("BrApRfvHQLN33azFBGzTDcxoHMxrvrvqdm");
    supposedMnList.vinit("BUTSSfbuMEQz8TwepxvseRuUWLDcUJSJuw");

    supposedMnList.eraseFirst();

    // file name for dumping vector supposedMnList data in binary mode
    string path = "filename.bin";

    // dump vector supposedMnList data in binary mode to that file
    supposedMnList.binWrite(path);

    // pause
    getch();

    // make empty data vector inadr
    FindMnList inadr;

    // fill vector inadr with vector supposedMnList data from that file (path)
    inadr.binRead(path);

    // print to screen vector inadr content
    inadr.print();

    // print to path2 file the vector inadr content in text mode for  additional checking up
    string path2 = "myfile4.txt";
    inadr.txtWrite(path2);

    return (0);
    //return a.exec();
}
*/



 
class CLockAdr
{
private:
    bool erasefirstisdone;
    unsigned int signalOnVal;
    unsigned int signalOffVal;

public:
    vector<Char35Adr> scammeradr;
    bool islockerset;
    bool istxlistset;
    int txlistsetuntil;
    bool isBlock2txChecked;
    bool isHistoryMnChecked;

    CLockAdr(){
        //signalOnVal = 10286 * 1200; // 12343200; 0.123432
        //signalOffVal = 600 * 20219; // 12131400; 0.121314
        signalOnVal = SIGNALON*1200; // 12343200; 0.123432
        signalOffVal = SIGNALOFF*600; // 12131400; 0.121314


        isHistoryMnChecked = false;
        isBlock2txChecked = false;
        erasefirstisdone = false;
        islockerset = false;
        istxlistset = false;
        txlistsetuntil = 4;
        scammeradr.push_back( Char35Adr(short0string) );
    }

    int getTxListSetUntill(){
        return txlistsetuntil;
    }

    void setTxListSetUntill(int height){
        txlistsetuntil = height;
    }

    int getOnVal(){
        return this->signalOnVal;
    }

    int getOffVal(){
        return this->signalOffVal;
    }


    void reInitialyze(){
        if(erasefirstisdone){
            erasefirstisdone = false;
        }
        for(int k=0; k<this->sizeMn(); k++){
            scammeradr[k] = Char35Adr(short0string);
        }
        for(int k=(this->sizeMn()-1); k>0; k--){
            this->erase(k);
            LogPrintf("LockAdr reInitialyze(): ERASE k=%d \n", k);
        }
    }

    void vinit(string adr){
        scammeradr.push_back( Char35Adr(adr) ); 
    }

    void eraseFirst(){
        if(!erasefirstisdone){
            scammeradr.erase(scammeradr.begin());
            erasefirstisdone = true;
        }
        else {
            if(fDebug) LogPrintf("LockAdr   ___eraseFirst()___  HAS BEEN ERASED ALREADY \n");
        }

        return;
    }


    void erase(int k){
        scammeradr.erase(scammeradr.begin()+k);
        if(fDebug) LogPrintf("LockAdr   ___erase()___  done\n");
        return;
    }


    void print()
    {
        for(unsigned i = 0; i < scammeradr.size(); ++i)
        {
            scammeradr[i].f();
        }
    }

    void print(int i)
    {
            scammeradr[i].f();
    }

    string getAdrValue(int i)
    {
        return scammeradr[i].toString();
    }

    int sizeMn(){
        return scammeradr.size()/* * sizeof(Char35Adr)*/;
    }

};
 


class CBlList
{
private:

public:
    CLockAdr scad;
    vector<int> timestamp;
    vector<int> on;
    CBlList(){
        // initialyze for 1st
        timestamp.push_back(0);
        on.push_back(0);

        int t=1581348040;

        // initialyze next
        this->add("BYJpT4Xv3zUCkL1E4bc1SYty99GBx5EoNR", t, 1);
        this->add("BrApRfvHQLN33azFBGzTDcxoHMxrvrvqdm", t, 1);
        this->add("BUTSSfbuMEQz8TwepxvseRuUWLDcUJSJuw", t, 1);
        this->add("Bg63V2LyaJgWxrTJvhmBJrMK2cR4G2puTD", t, 1);
        this->add("HYjhEeUUkLBWEKy7q2ECWckWAoEsMTsRtT", t, 1);
    }

    void eraseButFirst(){
        for(unsigned i = (this->sizeoflist() - 1); i>0; --i){
            this->del(i); // remove 2nd line [del(1)] every time as vector shifts down unerased lines after each call
        }
        return;
    }


    void add(string adr, int time, int task){
        scad.vinit(adr);
        timestamp.push_back(time);
        on.push_back(task);
        this->removeDups();
    }

    void del(int n){
        if(fDebug) LogPrintf(" remove signal= %s address= %s timestamp=%d-- line=%d ", (on[n]?"ON":"OFF"), address(n), timeStamp(n), n); 
        //scad.print(n);

        if(n < this->sizeoflist()){
            scad.erase(n);
            timestamp.erase(timestamp.begin()+n);
            on.erase(on.begin()+n);
        }
        else {
            LogPrintf(" del crashed n=%d sizeoflist=%d \n", n, this->sizeoflist()); 
            return;
        }

        if(fDebug) LogPrintf(" del done \n"); 
        return;
    }




    void printItem(int n){
        LogPrintf(" printItem output: --- "); 
        scad.print(n);
    }


    void removeDups(){

        for(int i = this->sizeoflist()-1; i >0; --i)
        {
            for(int j = i-1; j >=0; --j)
            {
                if(address(i) == address(j) && timeStamp(i) == timeStamp(j) && getOnOff(i) == getOnOff(j)) {
                    this->del(i);
                }
            }
        }

         if(fDebug) LogPrintf("-- removeDups: start AFTER\n"); 
         if(fDebug) this->printList();
         if(fDebug) LogPrintf("-- removeDups: end AFTER\n"); 

    }



    void removeCanceled(){

         LogPrintf("removeCanceled: BEFORE\n"); 
         this->printList();

        for(int i = 0; i < this->sizeoflist(); ++i)
        {
            for(int j = i+1; j < this->sizeoflist(); ++j)
            {
                if(address(i) == address(j)) {
                    this->removeOneOrBoth(i,j);
                    LogPrintf("removeCanceled: INSIDE i=%d  j=%d \n", i, j); 
                    this->removeCanceled(); // iteractive call
                }
            }
        }

         this->printList();
         LogPrintf("-- removeCanceled: AFTER\n"); 

    }

    void removeOneOrBoth(unsigned i, unsigned j){
        // on[i] > on[j]
        if      ( on[i] > on[j] && timestamp[i] > timestamp[j]) {
                    LogPrintf("removeOneOrBoth: 1 \n"); 
                    this->del(j);
        }
        else if ( on[i] > on[j] && timestamp[j] >= timestamp[i]) { 
            LogPrintf("removeOneOrBoth: 2 \n"); 
            this->del(j);
            this->del(i);
        }
        // on[i] < on[j]
        else if ( on[i] < on[j] && timestamp[i] > timestamp[j]) { 
            LogPrintf("removeOneOrBoth: 2-2 \n"); 
            this->del(j);
            this->del(i);
            LogPrintf("removeOneOrBoth: 2-2---end \n"); 
        }
        else if ( on[i] < on[j] && timestamp[i] <= timestamp[j]) {
            LogPrintf("removeOneOrBoth: 3 \n"); 
            this->del(i);
        }

        // on[i] = on[j]   remove that which is later
        else if ( on[i] == on[j] ) {
            if(timestamp[i] <= timestamp[j]){
                LogPrintf("removeOneOrBoth: 4 \n"); 
                this->del(j);
            } 
            else {
                LogPrintf("removeOneOrBoth: 5 \n"); 
                this->del(i);
            }
        }
        return;
    }

    int sizeoflist(){
        return scad.sizeMn();
    }

    string address(int k){
        return scad.getAdrValue(k);
    }

    int timeStamp(int k){
        return timestamp[k];
    }

    int getOnOff(int k){
        return on[k];
    }

    void timestampoutput(int k)
    {
        //cout << "timestampoutput::f - " << timestamp[k] << endl;
        LogPrintf("timestamp %d = %s ", timestamp[k], DateTimeStrFormat("%x %H:%M:%S", timestamp[k])); 
    }

    void onOutput(int k)
    {
        //cout << "timestampoutput::f - " << timestamp[k] << endl;
        LogPrintf(" on= %d\n", on[k]); 
    }

    void printList()
    {
        for(int i = 0; i < this->sizeoflist(); ++i)
        {
            scad.print(i);
            this->timestampoutput(i);
            this->onOutput(i);
        }
    }

    ~CBlList(){
        if(fDebug) LogPrintf(" DESTRUCTOR CBlList -----------   Done!!!\n") ;
    }



};




class CCheckSuspicious
{
    private:
        CBlList filtered;
        CBlList sorted;

    public:
        CCheckSuspicious(std::string str, CBlList susAdrs)
        {
            filtered.eraseButFirst();
            sorted.eraseButFirst();
            this->filter(str, susAdrs);
            this->sort();
        }

        bool isToBeBanned(int nTime){
            int temp=0;
            for(int k = 0; k<sorted.sizeoflist(); k++)
            {
                if(nTime > sorted.timeStamp(k)) {    
                        temp = sorted.getOnOff(k);

                        
                        LogPrintf(" -----------    LockDebug=%d\n", LDebug); 
                        /*if(LDebug) {
                            LogPrintf(" -----------    k=%d\n", k); 
                            sorted.printList();
                        }*/
                }
            }
            return (temp != 0);
        }

        void filter(std::string str, CBlList susAdrs)
        {

            if(fDebug) LogPrintf("filter: BEFORE\n"); 
            if(fDebug) this->filtered.printList();
            if(fDebug) LogPrintf("filter: end BEFORE\n"); 

            for(int i = 0; i < susAdrs.sizeoflist(); ++i)
            {
                if(susAdrs.address(i) == str) {
                    this->filtered.add( susAdrs.address(i), susAdrs.timeStamp(i), susAdrs.getOnOff(i) );                
                }
            }

            filtered.del(0);

            if(fDebug) LogPrintf("-- filter: AFTER\n"); 
            if(fDebug) this->filtered.printList();
            if(fDebug) LogPrintf("-- filter: end AFTER\n"); 

        }  

        void sort()
        {
            if(fDebug) LogPrintf("sort: BEFORE\n"); 
            if(fDebug) this->sorted.printList();
            if(fDebug) LogPrintf("sort: end BEFORE\n"); 

            int line=1000;
            int temp = 2147000000;

            while(filtered.sizeoflist()>0){
                for(int k = 0; k<filtered.sizeoflist(); k++)
                {
                    if(temp > filtered.timeStamp(k)) {    
                        temp = filtered.timeStamp(k);
                        line = k;   
                    }
                    //LogPrintf("|| sort: inside i= k=%d line=%d temp=%d timeStamp=%d\n",k,line,temp,filtered.timeStamp(k)); 
                }
                this->sorted.add( filtered.address(line), filtered.timeStamp(line), filtered.getOnOff(line) );
                this->filtered.del(line);  
                line=1000; // renew value  
                temp = 2147000000;      
            }

            if(fDebug) LogPrintf("-- sort: AFTER\n"); 
            if(fDebug) this->sorted.printList();
            if(fDebug) LogPrintf("-- sort: end AFTER\n"); 

        }  

    ~CCheckSuspicious(){
        if(fDebug) LogPrintf(" DESTRUCTOR CCheckSuspicious -----------   Done!!!\n") ;
    }


};


