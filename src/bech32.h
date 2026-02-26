// Copyright (c) 2017 Pieter Wuille
// Distributed under the MIT software license

#ifndef HEXLAN_BECH32_H
#define HEXLAN_BECH32_H

#include <stdint.h>
#include <string>
#include <vector>

namespace bech32
{

/** Encode a Bech32 string. If hrp contains uppercase characters, this will cause an assertion error. Encoding must occur using one case only. */
std::string Encode(const std::string& hrp, const std::vector<uint8_t>& values);

/** Decode a Bech32 string. Returns (hrp, data). Empty hrp means failure. */
std::pair<std::string, std::vector<uint8_t> > Decode(const std::string& str);

} // namespace bech32

#endif // HEXLAN_BECH32_H
