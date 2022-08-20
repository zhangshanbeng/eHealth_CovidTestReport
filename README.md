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

配置`config.json`

`token`: 苏康码的token

`uuid`: 苏康码的uuid

`time`: 查询时间，格式为`YYYY-MM-DD HH:MM`，如`2022-07-07 07:07`

`interval`: 查询间隔，单位为秒，如`60`

`need_mail`: 是否需要邮件通知，如`false`, `true`

`receiver`: 你的邮箱，如`YOUR_MAIL`

*如果需要邮件通知，请在`sendmail.py`中配置好邮件服务器，如果不需要邮件通知，请忽略此项

配置好以上信息，运行脚本`CovidTestReport`即可

### 3. 项目说明

启动后，每隔`interval`秒将会查询一次省内核酸记录，如果有新记录出现，其采样时间时间戳 >= 我们设置的日期的时间戳，则可以发送邮件通知并结束程序

*更详细的说明:

例如:
我在2022-07-07 07:07做了一次核酸

现在是2022-07-07 08:08，显然核酸结果还没出来

而我现在很焦虑，想在核酸结果出来的时候提醒我

所以此处日期可以设置为2022-07-07 00:00

此日期的取值范围是: 上一次核酸时间 - 本次核酸采样时间

日期格式为: '%Y-%m-%d %H:%M'

### 4. 致谢

[dsus4wang](https://github.com/dsus4wang)：[oneclickreport](https://github.com/dsus4wang/oneclickreport)

今年年初的时候偶然间看见这位大佬的仓库，直接打开了苏康码的新的大门，通过苏州苏城码入口申领苏康码，随后跳转的url里就会有token+uuid，而且这个token的有效期似乎非常长

### 5. 写在最后

在编写这篇说明的时候，我偶然间看见一篇帖子，在[一秒钟内打开苏康码](https://anduin.aiursoft.com/post/2021/12/7/open-suzhou-health-code-in-1-second)，可以作为补充阅读

苏康码的迭代优化其实还是挺快的，网页版苏康码可能过不了多久就会被淘汰，因此本项目的时效性需要读者自行判断

最后的最后，本项目不会对苏康码信息安全造成破坏，没有触碰法律红线，本项目仅可用于查询自己的核酸状态，禁止商用

### 6. 一些新的发现

谨言慎行

### 7. 更新记录

`2022/5/13` 今天自己在使用的过程中，运行之后立刻就收到了邮件，但是并不是报告出来了，观察返回的数据后发现，发现是苏康码对timeFlag字段进行了更新，以前的timeFlag格式为YYYYMMDD，现在是YYYYMMDDHHMM，12位数肯定比8为数大啦，这就是问题所在，因此，my_timeFlag在设置的时候加上0000(0时0分)即可

`2022/8/18` 苏康码提供了核酸查询接口，免得换令牌去卫健委查询，以前是使用timeFlag字段进行日期比较，现在使用collectTime字段，转换为时间戳后比较
