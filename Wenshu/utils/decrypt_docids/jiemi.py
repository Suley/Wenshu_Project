# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  jiemi.py
@time:  2018/12/11
"""
import re
import threading
import time

import execjs


text = 'w61aS8KOwoMwDD0LwqjCi0TCjMOmAsKowqseYcKWVsKEKsO6YzFlwpQywqvCqncfwqDCiMOySQMdAk3DqcKTwpArEsObw49+ThwidXHCiDbDm1MowqPCn2TDucKVw4jDqMK4w7/DnMOJw7h7dVjDi1XCvMOZMsOPw7FIQFgtPkACw4R7wqzCkDkkw7Imw5sVXQnCtcKFAMOvYBYCw5UDYyguEgYnYAd0IHXDpA8Sw4AEwohBw5bDoAnDiSElVAACC8OBQsOBfT9YwrphfDwlw7I3TGLDqcO6AQUifRjDs8OOwpdMwq18w44XTldLSsKFEB5zw7IJTnXCn8OZRMO3TMO+wrrCuMO9O8KBWDbCnGrCkMKTw43CkMKgw7TCpwFYV3cKwoPDu2DCjcK4wpXCusOawpjCqsOew5TDoyVUHnXCm8KiVgjDihw0wr7DiyDDuzFaecOtDMK7wqfDhiNqD8Orw77Dj2DCgMOVUFMjw7bCncO7w4TCgHvDg8KeXsOAXcK5F8KLwo5FeQcZFW1cw4cTeMKfCmLCshXCrwXCp1rCp8Kkw47Crm8ew5lswrLDtw/CnnkXFMOew63DgTEHw7bChMOWwq3CjWXDnMKdNcOOw6Fnw4F3wo1hw5gnw4U0PcK2wqE9NCsnL1M8TRTDjcODwr/Dl33Dk0rCvhTDl8OLVnJUw6vDoMOqw5HCqkMacEHCtsKIPMOEU8KBw6XCjMO7fw==,DcOOwrcBw4AwCADCsMKXw6jCmMKRw7rDv0nDicKsRU/CqWrCmsOYwrlww7gYwpEGwoN6KcOfKj51LDrDisOxw6EUw4lbO8Kqw6s+BsOxGMOoworDm8KXUWxOwpzCl8Klw6LDiMOWR8OvbB4aEGTCuCLCi8Oawo8qw6g7wrfDoGAJwoZOwrDCiGEAw5pNw4VAWcK9RsKaXcO7JsOKAQrCl8KlSsOrw49UwqjDt8K1w68fw6DDhjPDvhs5wpMVTDLDpTfDjcOCwo8WBD4=,HcKOw4cRBDEMw4NaUsKyLD5lwoXDvkvCusKde8KDQ8KgQsKoUMOhw6RPT8OhbcOoE8KwYcOFET3ClBvDuXJrwoYkOcKPfhNqaj/DmsKSaioXw4PCsVbDpm5qVxbCt2EMPQ7CjcKhfh9MwrIgwqbCkMKBHHZRAsOvDcOMPFzDr8K4wpnDj8OvZcKbw5vDkcONw6nDi0HCsxbDhcK6ecKOOcKJw5XDmcKZw5LDr8O+w4vDngnDvcK4T3cZw7DDr8KFw5V8UsOkJlvDs8O7AQ==,DcKOSQ4AMQjDg8K+FCjClHJkw73Dv8KTZsKOwpFsOcOswprCuMK1w4RHGsKww6Maw5rDjcOeZwzCgyvCqMOdQQXClCLCl8Kjw6Qywr/CsVzDj8KpPHPCjXBODcKLw695wpbCoggafxvCh8O8wpoTJktWwpZiw53Di8OeL8OLwrpawqfDjmTDi8KzScOGw7PDhS7DnmBEVcKNNsOeM8OFUULDvRTDuy3CvzLDqMOsU8O/L8OzDMKHV8ODwrPCl1LDo8K1w7zCrX/Di1zCnsKBwrJ/,DcKPwrkNADEMw4NWSsOkwr/DtBPDrz/Dkl0rwpAEdMKqwqXDhTbDusK8JsK6w4UdEsKqwpXDog5uwoZOw5fClMKiwo5Hc2nCpHcvw43CmzbDl2VRw6PDtsOjCS3CgsO0UcKpwpvCoMOmV8KewpnChkzDh8KSwr/Di3xgwpzCq8O7RDp2w77CnB3DssKZUUHCs2fDqXXCnkRnwrlgwqFxw6RSwqBkVMKtfyDDgx/Co8OoWsO8wrXDuy5Gw7/CvU0cGcK0wot0wo5fRcONf8OpAw==,DcKOwrcBADAIw4NeInRGQsO5w7/CpGTDsmLDicOmOn0JwqLCp2PCvcOVw5DCssKgegIPHEBUw5bCiBrCrcKKVcKaFBvDugBuEGHCi0LCqsKUJybDgVfCjDjCusKJG8O5ZcOow4zClBJXLBnCoVLCpsO2wrMIWj7DjD3CuyzCl8OSwrDDqcK3woPDrAozO8KMbGTDssKkLWMqw7XDlnbDmsO9wqTCtMKpwpcewoofwqwacMO7wq/DhsO/w6DCoiIGJDtzDCE2w68D,DcOLwrcNw4BADMOAw4DClcKUwqUvFcO3H8OJw64IHMKoL01uwo5TwrXClULDmMOSw7jDhV3Cr8ObwoUywofDthtDNsOJYMKEZCoKQMONVFYdwqgiwo8Yw7HCmgTCrm3DqsK/RmTClgvCisOGDWZjMAsew5XDukMiSsOcOj5Uw7tpVXLClWPDmHbCnCI8w53Cl0XDlEfCr8O6wonDpsOtUzM9woDDvwPDn0towoHDolvCv8KoPsKZXsK4wp51wowlTsOhNzIf,DcOOw4kBRFEEBMOAwpTDsD3Di8KRRsO+IcONVARVecKPOip4JsKfwp4ow7LCm8OFwoTDrsKzShTCjcOIR0bDsVEowqTDjMORK8OBSMK/Yjo5S8KxGXDDoCvCglYfTi3DisKLwp7CtsOQwqzCkSk1dk12w53CujhtwopaMsKlwo3DhsO8wq1zMsOgwrQvwrXCrMKCPsOzw7sPWMK/w5xzwrBhwr9rwrVtwoY8ecKmwqvDmg5hRcO1wqs2wpHChsKzXHXDq8K5JEfDvgA=,DcOMwrkBADEIw4TDgMKWw7jDjBMuBsO3X8OSXcKoQMOjwpDDqMK8wofDnDTDmlbCqMKgWEbDssO2NkfDicKywrMpwpnDjRPCq8KYwoDCpsOLFMKaw5HCnsOtD3IMN8KLw7fCnhLDq8KZw4XDrSLDqsOAw5/CucK8w4nCtEF8MMKPw4nChSDDrBozRX1CKyzCjcKSw6JZw6fDqsOGw7thw6TDj3QIw4YewqvDnsK6w4bClcKGw7F5wppzwo7DlMKyw61LXMOGP8K1w7MtD30ZD04kYcKiHw==,DcKOw4ERw4AwCMODVjIBYnhCSMO2H8KpfUsnwrvDpsOowp5cL2jDisKzNMKCwoLDhcOdw6o6w7XCiCEcwpV7N8K2w5p5wpTDvsKBw5HCqsKEHX4GCsOiwrBiw7xGwqnCn2xKw6rCvMKuw63DoiHCqm/CmAPDlsKiwqxrw4RvHMKeOm/DucOuf1tWW3LCvcOMTsKkw681fS0PIMKNJsOUwqtfdsOkw5/DomzDvHLCtVjDhMO/w7dNDS5uw6cKwrsqwrBiw6fCrcObG8OwDw==,DcKOw4kNADEIw4RaYsKABHhywoTDvkvDmsO9WsKybEZEwp1jw6EbMcKTwpHDvVhqw7UHcgPDtMOew6QkwqlnwptbacKccGPChA1swpFKRcK1w5sHwo1QGQXCgsKuwqpKw53CkhdKw7NUWE5kJsKMT2tbwq7Dq2IfwrVUwoHDtSnDncOuwp3ChsKKw53DtElGw6UtwqNjcBBkwqLCriTDrUPDj8Kjw5fDpMO4wpvDvnvCu8KawqXDsMOlw6JWwrvDjsOaLTnCuMO3f8OZDw==,DcKOw4kNADEIw4RawoLChXA8CTDDvcKXwrTCkcK/wpZlw47CjMOge1Msw4s9w47DsiYawrcowo8beV3DuUZhOQE9AiEyZWfCgynCvkkTN8OewqnCjSPChcOLwqd3ZMKHHxIsa8Kgw5DDkBYZUktMwq9zQsO6VsKMwojDo8K6wpAiKkDCmn3CuAHCrxTCoDlew4XCi8OrI8KmwqsHfGppD3MWw5rCnmESTcOzZcOQwqROwrNFwr8ZfMOSwr5PwpjDjR8=,DcOOw5sVADEEBcOAwpY8woLDuCTCl8O+S8OabWDDjjzDiD7CksOgDsKpw4fClcKdwrZcRUchLlJaR8K9w5MbV8OawphkwqHDpQvDh8KZwqfDl8KBPnjDm8K3SMKYwpNCw41AwoTDlcORwrBTRMKCW8ODS1PDtsOSwpTDisOsOFsKwpHCjsKdwrdhwrlxYyDCgMKbNivCncK5wrURw5XCh8KCNiZdw59fwpPDiXHCmhvCmWXCjmpew4nCvcOufSU1VX56wpDCssOnAcKMP8O8AQ==,FcKOw4sRRDEIw4Naw6Ibw4LDkUDDqMK/wqR9e8KURzMWw5dqw7VrwojDuVUnWWcyw4RYw7ALw5hDacK+HVoYwrM8wo5rwpY5McK5w6/DtMOZMF3DtsK2wozClMKswrrCl8Krw6V+wpZAfBPCpxMOGMO1wpZ4IzEiwp7DqxnDh1LDgMKfw6F9YQHCosOZLcK1PGoiwovDl8OzZcONZBbDlsO/wqQlw4PDn8KEw6tkF8K6SWNzOhLDu8Kqw73DksKKHlI4w7l8wr/Ckj8=,DcONwrcBw4BACMOAw4DClcOIPCVxw7/CkcOsUsONw4nCn8KswqhswpPDj3XDjgHDsjMHw4XDi8KEasOWeCXCk3R3ShfCs0XCk8KcbAseFDvDtmY3ABhNJMOEw4VICQLDoinCocOcw5bCkFMYw7AVwpAhw69eUcKVw444w41RQ8K/QBHDrSfDv8KREMOpd8KNwpNswpgkwoBNw5vCphzDpSXCgsKCcUnDi8Kgw4LDqW/DjkjCsgjCosO3w4XDjSLDmsO+w50qwp5Fw7gB,DcOOw4kNADEIQ8ORwpYwYQlHCMOQf0kzV39ZekLCosODHMKHwpLDoVXDrCrDmSzCpMOeN8O+cTfDv8KSw559wrXDn8KWw5ZUwrvCryTCn1fCoiluYcKZYxYlRi9PwpTDhTPDs8KTOnnDucKcwpnDpsOhK8KUcsOTPMKCATBMw6zConZsw5cUw7pAw7piZyjCvEnDucOQw7/CgMO+FsK0w55rwoLDvsKVUiVMLWnCtcKkAcOnHlDCosKAwoPCmMKHwrTChsOIwq9dw6rDjQ8=,FcKOwrkRBEEIw4RSw6Idw4DDpMONP8Kkw5tTwrUhwqMNLcOYZWNKwoTDpiZoGsKySzlsw44pwrwKwqhWw7wmw7jClhwGwqUuwr7DlyXDmizCv1Q+w40aw4l3TMKywo4Fw5lwwrTDnMKnIj7ChjXDkWjDosKlSMO4WsOcwqwyKyJXwoM/FsKWwqzDpMOtYRcyXSzCrsOvAxrDiEpww57Ctkg5w5/Clgw2wqLDs8O6w7fDhkU7U8OnUn9xGMOzLGR5w7jCk8O5AQ==,FcKNwrkRA0EIw4BaAsKWN8Okw63CvyTCn2NpJCbDq1UCwoQNRcK1wq3DkMK+bWtITHIqw6TDkcK3w6LCm1cfLcK7dhBjwrVQw4rCiUXChSzDt8KSEMOkwqrCvmsmwpzCgzbDl8K5bCHCoMOkYcK5w5Zcw5hrW8O2SsKvBcKJUMKzMkIae1/DssOdwozDs8KUw4XDq8O7S8KswpsZGUR1w7kSwqJvXsOUwozCrE4gRzh/S1UPecKDw50lwq40RCjCjsO1Aw==,FcKOw4kVRDEIw4NaAhPCtiMkw5B/ScOzw6dsw6nDicKtRsKAwrMyFE/DqsKiwoBKQARZMzoDwovCp0IOw5hKD3RTZcOBZmzDhcKYPcO8Z8K7w4/Dp8KYBUnChcKDwo7DgsKmw4LCsmPDn8Oxb8K6wqTCjz4SfsKSwrIfwqfCnkfDhREeK8KTY0XDpcK5w63CphFRw6rCvcKDc8KXU27Dn3pHwocHwpfCpMOxw78VwpnCusOiwqvDhMOxwq59WsOHV8OTPSbCpcKXIUk/,DcOLw4cNw4BACADCsMKVwqgHPMKpw7vCj8KUfC3DucKewqTDmHrDn0wFPlPCjT5pwrjDmgrDqMOQw5VZJcO0w4whwrzCvHjClR3CuHt/HMK/wrtoRcOvMRzChGlswowjKT8twq5Jwr4wETw6wqbCljIwNsOQW8K7dAwVAgHDnsOCPH/CssKzw7jDpGoWwoDDvmbCknMJAcO0Q1kww60GJMKrGG5JwoRww4VzLEAsfUZuw5bDrA3DpcO2w4ghPg==,FcOPw4sRBDEIA8ORwpQQw4Z8wo7CgCHDv8KQdsO2wq7DqldaS8OYw5RpwqrClBvCtsKYw4deT8OcMC7Cl8KEwoHDoMOEwprDqXHCiwwnKX1DAsK/Z3kaw7tgBMOYw5rDo8OkY8K4B8O9IMKBw4PCgsKgwpzDmEVWWi5twpxvw746wr9cwpfCr2Qqw6bCqgU6dmBGw7x2WMOSwqPDpMO+WcO1w5XCliHDv8KswoHDuMKwKUfCqcKeworCvlcjwoRmwr8bcMKpchs3w7vDvMKHwp4f'


class GetDocId(object):

    def __init__(self):
        with open('../spiders/docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_2 = execjs.compile(jsdata_2)

    def decrypt_id(self, runeval, cids):
        """
        docid解密
        :param runeval: 运行参数
        :param cids: 待解密id列表
        :return: docid
        """
        print(runeval)
        js = self.js_2.call("GetJs", runeval)
        js_objs = js.split(";;")  # 使用 ;; 分割字符串,返回一个list
        js1 = js_objs[0] + ';'    # 分割的字符串的第0项尾部加上 ;
        js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]  # 根据正则搜索
        key = self.js_2.call("EvalKey", js1, js2)
        key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]

        print(key)
        s = self.js_2.call("DecryptDocID", key, 'HcKOw4cRBDEMw4NaUsKyLD5lwoXDvkvCusKde8KDQ8KgQsKoUMOhw6RPT8OhbcOoE8KwYcOFET3ClBvDuXJrwoYkOcKPfhNqaj/DmsKSaioXw4PCsVbDpm5qVxbCt2EMPQ7CjcKhfh9MwrIgwqbCkMKBHHZRAsOvDcOMPFzDr8K4wpnDj8OvZcKbw5vDkcONw6nDi0HCsxbDhcK6ecKOOcKJw5XDmcKZw5LDr8O+w4vDngnDvcK4T3cZw7DDr8KFw5V8UsOkJlvDs8O7AQ==')
        print(s)

num = 0
c = GetDocId()

def run():
    global num
    global text
    lis = text.split(',')
    r = lis[0]
    cids = lis[1:]
    while True:
        for i in c.decrypt_id(r, cids):
            num += 1


def run2():
    global num
    while True:
        time.sleep(1)
        print(num)

def multy():
    th1 = threading.Thread(target=run)
    th2 = threading.Thread(target=run2)
    th1.start()
    th2.start()

# while True:
#     pass

multy()
