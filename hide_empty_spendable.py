import os

fpath = "src/qt/overviewpage.cpp"
try:
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read()

    s_find = """    // only show immature (newly mined) balance if it's non-zero, so as not to complicate things
    // for the non-mining users
    bool showImmature = immatureBalance != 0;
    bool showWatchOnlyImmature = watchImmatureBalance != 0;

    // for symmetry reasons also show immature label when the watch-only one is shown
    ui->labelImmature->setVisible(showImmature || showWatchOnlyImmature);
    ui->labelImmatureText->setVisible(showImmature || showWatchOnlyImmature);
    ui->labelWatchImmature->setVisible(showWatchOnlyImmature); // show watch-only immature balance"""

    s_replace = """    // HEXLAN: Скрываем колонку обычного баланса, если он нулевой, а Watch-Only имеет средства
    bool hasNormalBalance = (balance > 0 || stake > 0 || unconfirmedBalance > 0 || immatureBalance > 0 || anonymizedBalance > 0);
    bool hasWatchOnlyBalance = (watchOnlyBalance > 0 || watchOnlyStake > 0 || watchUnconfBalance > 0 || watchImmatureBalance > 0);
    bool showNormal = hasNormalBalance || !hasWatchOnlyBalance;

    ui->labelSpendable->setVisible(showNormal);
    ui->labelBalance->setVisible(showNormal);
    ui->labelStake->setVisible(showNormal);
    ui->labelUnconfirmed->setVisible(showNormal);
    ui->labelAnonymized->setVisible(showNormal);
    ui->labelAnonymizedText->setVisible(showNormal);
    ui->labelTotal->setVisible(showNormal);
    ui->lineSpendableBalance->setVisible(showNormal);

    // only show immature (newly mined) balance if it's non-zero, so as not to complicate things
    // for the non-mining users
    bool showImmature = immatureBalance != 0;
    bool showWatchOnlyImmature = watchImmatureBalance != 0;

    // for symmetry reasons also show immature label when the watch-only one is shown
    ui->labelImmature->setVisible((showImmature || showWatchOnlyImmature) && showNormal);
    ui->labelImmatureText->setVisible(showImmature || showWatchOnlyImmature);
    ui->labelWatchImmature->setVisible(showWatchOnlyImmature); // show watch-only immature balance"""

    if s_find in code:
        code = code.replace(s_find, s_replace)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(code)
        print("Success: overviewpage.cpp patched to hide empty spendable balance.")
    elif "HEXLAN: Скрываем колонку" in code:
        print("Already patched.")
    else:
        print("Error: Target code block not found. Cannot patch.")

except Exception as e:
    print("Error: " + str(e))
