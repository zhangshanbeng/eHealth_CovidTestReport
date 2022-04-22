# eHealth_CovidTestReport

通过苏康码核酸查询接口获取个人省内核酸记录

### 0. 写在前面

某人因太懒，傍晚才去做核酸，成功掉进焦虑陷阱，姑且称之为“核酸焦虑”

本着有焦虑就有缓解焦虑的焦虑，该项目成功入选我的《缓解焦虑》专题的第二期

### 1. 项目准备

前往[https://scm.szgaj.cn/wjw/health_skm.html](https://scm.szgaj.cn/wjw/health_skm.html)申领网页版苏康码（该网站为苏州公安局，可放心使用）

申领后可以发现健康码的url格式如下：

https://jsstm.jszwfw.gov.cn/jkmIndex.html?token=XXX&uuid=XXX

记住这个token和uuid，它们相当于你的凭证

*可选项：配置好你的通知设置，如：邮件，Server酱，企业微信BOT

### 2. 项目运行

需要配置的有以下三处：

`get_abc()中的data`: 配置好苏康码的token和uuid

`judge_report()中的send_email`: 这里你可以选择配置好邮箱，也可以调用Sever酱

`my_dateFlag`: 该值大小在 (上一次核酸时间, 本次核酸时间] 区间内，例如我2022年1月1日做了一次核酸，那么my_dateFlag可以设置为20220101

配置好以上信息，运行脚本即可

### 3. 项目说明

启动后，每隔60s将会查询一次省内核酸记录，如果有新记录出现，且其dateFlag >= 我们设置的my_dateFlag（例如：my_dateFlag = 20220421，这时候有一条新的核酸记录，该记录采集时间是20220421，满足>=的关系），那么将会通过邮件提醒你，同时循环结束

### 4. 致谢

[dsus4wang](https://github.com/dsus4wang)：[oneclickreport](https://github.com/dsus4wang/oneclickreport)

今年年初的时候偶然间看见这位大佬的仓库，直接打开了苏康码的新的大门，通过苏州苏城码入口申领苏康码，随后跳转的url里就会有token+uuid，而且这个token的有效期似乎非常长

### 5. 写在最后

在编写这篇说明的时候，我偶然间看见一篇帖子，在[一秒钟内打开苏康码](https://anduin.aiursoft.com/post/2021/12/7/open-suzhou-health-code-in-1-second)，可以作为补充阅读

苏康码的迭代优化其实还是挺快的，网页版苏康码可能过不了多久就会被淘汰，因此本项目的时效性需要读者自行判断

最后的最后，本项目不会对苏康码信息安全造成破坏，没有触碰法律红线，本项目仅可用于查询自己的核酸状态，禁止商用
