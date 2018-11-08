# BJUT Network ipv4&ipv6 Autologin
北工大校园网有线自动登录Python3脚本，`IPV4与IPV6统一认证`模式。

![screenshot](https://i.imgur.com/4FfrqPt.png)

## 简介
北工大的校园网登录非常奇葩，如果你仅需要单一的ipv4登录或者ipv6登录，简单的使用`curl`发送一个POST请求就可以了，但这样无法同时使用ipv4和ipv6。若有此需求，只能通过`IPV4与IPV6统一认证`模式。在这个模式中，会先向跳转网址`https://lgn6.bjut.edu.cn/V6?https://lgn.bjut.edu.cn`发送POST请求，再向`https://lgn.bjut.edu.cn`发送第二个POST请求，跳转回来。过程中必须分别包含在页面中给出的v4和v6两个地址，才可正常的登录使用。

所以本Python脚本通过正则表达式获取两个页面中的地址，完全模拟使用浏览器`IPV4与IPV6统一认证`登录时的各步骤，以达到可以同时使用ipv4和ipv6的效果。

此脚本在本部宿舍有线网络上测试通过，暂不支持无线网络使用。

## 使用
```
Usage:  gateway-login.py <user> <password>     #登录网关
        gateway-login.py --status              #查看账号信息
        gateway-login.py --logout              #注销账号
```
如果报错无法登陆，请先尝试注销一遍。
