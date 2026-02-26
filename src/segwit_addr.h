// Copyright (c) 2026 Hexlan Developers
// Distributed under the MIT software license

#ifndef HEXLAN_SEGWIT_ADDR_H
#define HEXLAN_SEGWIT_ADDR_H

#include "script.h"
#include <string>

// HRP (Human Readable Part) для сети Hexlan
extern const std::string SEGWIT_HRP;

std::string EncodeDestination(const CTxDestination& dest);
CTxDestination DecodeDestination(const std::string& str);
bool IsValidDestinationString(const std::string& str);

#endif // HEXLAN_SEGWIT_ADDR_H
