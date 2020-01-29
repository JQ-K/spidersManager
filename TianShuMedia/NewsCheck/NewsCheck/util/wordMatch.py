srcFilePath = '/Users/macbookpro/PycharmProjects/spidersManager/TianShuMedia/NewsCheck/wechat.txt'
dstFilePath = '/Users/macbookpro/PycharmProjects/spidersManager/TianShuMedia/NewsCheck/wechat_result_1.txt'

wordList = ['冠状病毒', '隔离', '感染', '传染', '肺炎', '疫情', '确诊', '病例',
            '突发公共卫生事件', '重大卫生事件', '口罩', '驰援', '雷神山', '火神山',
            '小汤山', '野味', '武汉', 'N95', '封城', '钟南山', '卫健委', 'SARS',
            '消毒', '蝙蝠', '果子狸', '2019-nCov']

def isYiQingNews(cont):
    for word in wordList:
        if cont.find(word) >= 0:
            return True
    return False

def run():
    f_src = open(srcFilePath, encoding='utf-8')
    f_dst = open(dstFilePath, 'w+', encoding='utf-8')

    for line in f_src:
        cont = line.strip('\n')
        rlt = isYiQingNews(cont)
        print(cont)
        print(rlt)
        if rlt:
            isYiQing = '是'
        else:
            isYiQing = '否'
        #msg = cont + '\t' + isYiQing
        msg = isYiQing
        f_dst.write(msg + '\n')

    f_src.close()
    f_dst.close()


run()