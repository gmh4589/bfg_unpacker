@echo off
if [%1]==[] goto help
if [%2]==[] goto help
if [%3]==[] goto help
if [%4]==[] goto help

    quickbms -a "\"des\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"3des2\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"3des\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"desx\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"arc4\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"idea\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc2\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"blowfish\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"cast5\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"aes_128_ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"seed\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tea\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"xtea\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"xxtea\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"swap\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"reverseshort\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"reverselong\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"math ARG\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"xmath ARG\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"random\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"xor\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rot\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rotate\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"reverse\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"incremental\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"charset\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"charset2\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"ebcdic\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"twofish\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"serpent\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"icecrypt\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"ice\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rotor\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"ssc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"wincrypt\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"cryptunprotect\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"zipcrypto\" \"%4\" \"%5\"" %1 %2 %3

    rem mcrypt
    quickbms -a "\"mcrypt blowfish_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt blowfish_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt blowfish_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt blowfish_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt blowfish_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt blowfish_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt des_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt des_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt des_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt des_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt des_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt des_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt tripledes_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt tripledes_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt tripledes_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt tripledes_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt tripledes_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt tripledes_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt threeway_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt threeway_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt threeway_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt threeway_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt threeway_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt threeway_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt gost_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt gost_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt gost_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt gost_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt gost_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt gost_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk64_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk64_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk64_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk64_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk64_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk64_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk128_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk128_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk128_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk128_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk128_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt safer-sk128_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-128_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-128_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-128_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-128_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-128_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-128_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt xtea_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt xtea_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt xtea_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt xtea_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt xtea_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt xtea_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rc2_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rc2_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rc2_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rc2_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rc2_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rc2_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt twofish_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt twofish_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt twofish_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt twofish_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt twofish_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt twofish_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-256_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-256_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-256_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-256_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-256_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt cast-256_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt saferplus_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt saferplus_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt saferplus_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt saferplus_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt saferplus_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt saferplus_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt loki97_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt loki97_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt loki97_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt loki97_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt loki97_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt loki97_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt serpent_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt serpent_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt serpent_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt serpent_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt serpent_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt serpent_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-128_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-128_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-128_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-128_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-128_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-128_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-192_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-192_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-192_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-192_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-192_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-192_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-256_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-256_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-256_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-256_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-256_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt rijndael-256_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt enigma_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt enigma_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt enigma_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt enigma_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt enigma_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt enigma_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt arcfour_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt arcfour_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt arcfour_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt arcfour_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt arcfour_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt arcfour_stream\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt wake_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt wake_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt wake_cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt wake_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt wake_nofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mcrypt wake_stream\" \"%4\" \"%5\"" %1 %2 %3

    rem tomcrypt
    quickbms -a "\"tomcrypt blowfish ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt blowfish f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc5 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc6 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rc2 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt saferp f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k64 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-k128 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk64 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt safer-sk128 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt rijndael f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt xtea f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt twofish f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt des f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt 3des f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt cast5 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt noekeon f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt skipjack f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt khazad f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt anubis f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt seed f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt kasumi f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt multi2 f9\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia cfb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia lrw\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia f8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia hmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia omac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia pmac\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia eax\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia ocb3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia ocb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia pelican\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia xcbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tomcrypt camellia f9\" \"%4\" \"%5\"" %1 %2 %3

    rem openssl
    quickbms -a "\"des_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"desx_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"des_ede3_wrap\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"dev_crypto_des_ede3_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"dev_crypto_rc4\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc4\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc4_40\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc4_hmac_md5\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"idea_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"idea_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"idea_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"idea_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc2_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc2_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc2_40_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc2_64_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc2_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc2_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"bf_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"bf_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"bf_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"bf_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"cast5_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"cast5_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"cast5_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"cast5_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc5_32_12_16_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc5_32_12_16_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc5_32_12_16_cfb64\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_cfb128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_wrap\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_cfb128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_192_wrap\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_cfb128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_ctr\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_ccm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_gcm\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_xts\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_wrap\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_cbc_hmac_sha1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_cbc_hmac_sha1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_128_cbc_hmac_sha256\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aes_256_cbc_hmac_sha256\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_128_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_128_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_128_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_128_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_128_cfb128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_128_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_192_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_192_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_192_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_192_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_192_cfb128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_192_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_256_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_256_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_256_cfb1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_256_cfb8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_256_cfb128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"camellia_256_ofb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"seed_ecb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"seed_cbc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"seed_cfb128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"seed_ofb\" \"%4\" \"%5\"" %1 %2 %3

    rem others
    rem quickbms -a "\"crc\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"execute\" \"%4\" \"%5\"" %1 %2 %3
    rem quickbms -a "\"calldll\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"3way\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"skipjack\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"anubis\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"aria\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"crypton\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"frog\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"gost\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"lucifer\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"kirk\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"pc1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mars\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"misty1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"noekeon\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"seal\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"safer\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mpq\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rc6\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"xor_prev\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"xor_prev2\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"xor_next\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"xor_next2\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rsa\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rsa tomcrypt\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"PKCS5_PBKDF2_HMAC\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"BytesToKey\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"ZIP_AES\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"modpow\" \"%4\" \"%5\"" %1 %2 %3

    rem ecrypt
    quickbms -a "\"abc\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"achterbahn\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"achterbahn128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"cryptmt\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"decim\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"dicing\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"dragon\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"edon80\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"ffcsr8\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"frogbit\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"fubuki\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"grain\" \"%4\" \"%5\"" %1 %2 %3
    rem freezing: quickbms -a "\"grain128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"hc128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"hc256\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"hermes128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"hermes80\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"lex\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mag\" \"%4\" \"%5\"" %1 %2 %3
    rem freezing: quickbms -a "\"mickey\" \"%4\" \"%5\"" %1 %2 %3
    rem freezing: quickbms -a "\"mickey128\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mir1\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"mosquito\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"moustique\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"nls\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"phelix\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"polarbear\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"pomaranch\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"py\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"rabbit\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"salsa20\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"sfinks\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"sosemanuk\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"sss\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"trivium\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tsc3\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"tsc4\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"vest\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"wg\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"yamb\" \"%4\" \"%5\"" %1 %2 %3
    quickbms -a "\"zkcrypt\" \"%4\" \"%5\"" %1 %2 %3

    rem others

    goto end

:help
    echo .
    echo QuickBMS encryption scanner 0.2
    echo by Luigi Auriemma
    echo e-mail: aluigi@autistici.org
    echo web:    aluigi.org
    echo .
    echo You must specify:
    echo - the path of encryption_scan.bms
    echo - the input file encrypted with the unknown algorithm
    echo - the output folder where placing the output files
    echo - the key, supported C format like "\x11\x22\x33" or "hello\r\n"
    echo - optional ivec, if you don't specify it the tool will use no
    echo   ivec and then an ivec set to zeroes producing 2 files
    echo .
    echo Example:
    echo   encryption_scan c:\encryption_scan.bms c:\dump.dat c:\out_folder "key" [ivec]
    echo .
    echo If an algorithm doesn't return immediately press CTRL-C
    echo and answer 'n' [no] when will be asked to "terminate batch job"
    echo .
:end
