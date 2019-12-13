1.免费渠道
快贷里、ip3366
2.代理池说明
    基于redis存储构建免费代理池。以redis无序set作为代理池载体，建立name:tianshu_proxyip_[domain_name] 的无序set代理池
    例如：快手代理池的name为: tianshu_proxyip_kuaishou
2.结构说明
    例如: {'HTTP': '222.89.32.174:9999'}
    即为一个字典，key为类型，value为host和port组成

