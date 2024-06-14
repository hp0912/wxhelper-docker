# pip intall pymem  
from pymem import Pymem  
import sys  
  
version3_9_2_23 = "3.9.2.23"  
version3_9_5_81 = "3.9.5.81"  
  
version3_9_2_23_hex = 0x63090217  
version3_9_5_81_hex = 0x63090551  
version3_9_10_27_hex = 0x63090a1b  
  
  
# 修复微信版本号  
def fix_version(pm: Pymem, version: str):  
    WeChatWindll_base = 0  
    for m in list(pm.list_modules()):  
       path = m.filename  
       if path.endswith("WeChatWin.dll"):  
          WeChatWindll_base = m.lpBaseOfDll  
          break  
  
    # 这些是CE找到的内存地址偏移量  
    ADDRS = [0x2FFEAF8, 0x3020E1C, 0x3021AEC, 0x303C4D8, 0x303FEF4, 0x30416EC]  # 3.9.2.23  
    version_hex = version3_9_2_23_hex  
    if version == version3_9_5_81:  
       ADDRS = [0x3A70FD4, 0x3A878DC, 0x3AA0508, 0x3AC85F0, 0x3ACF3D8, 0x3AD1908]  # 3.9.5.81  
       version_hex = version3_9_5_81_hex  
  
    for offset in ADDRS:  
       addr = WeChatWindll_base + offset  
       v = pm.read_uint(addr)  
       print(v)  
       if v == version3_9_10_27_hex:  # 是3.9.10.27，已经修复过了  
          continue  
       elif v != version_hex:  # 不是,修复也没用，代码是hardcode的，只适配这一个版本  
          raise Exception("别修了，版本不对，修了也没啥用。")  
  
       pm.write_uint(addr, version3_9_10_27_hex)  # 改成要伪装的版本3.9.10.27，转换逻辑看链接  
  
    print("好了，可以扫码登录了")  
  
  
if __name__ == "__main__":  
    try:  
       # 用户输入第一个参数是版本号，默认版本号是3.9.2.23  
       if len(sys.argv) > 1:  
          current_version = sys.argv[1]  
       else:  
          current_version = "3.9.2.23"  
       pm = Pymem("WeChat.exe")  
       fix_version(pm, current_version)  
    except Exception as e:  
       print(f"{e}，请确认微信程序已经打开！")