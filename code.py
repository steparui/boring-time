#-*-coding:utf-8-*-
import requests,lxml, os, json, re
import xlrd, xlwt

def get_content(var):
    target = 'https://leetcode.com/graphql'
    
    payload = {'operationName':'getQuestionDetail',
            "query":"query getQuestionDetail($titleSlug: String!) {\nisCurrentUserAuthenticated\nquestion(titleSlug: $titleSlug) {\nquestionId\nquestionTitle\nquestionTitleSlug\ncontent\ndifficulty\nstats\ncontributors\ncompanyTags\ntopicTags\nsimilarQuestions\ndiscussUrl\nmysqlSchemas\nrandomQuestionUrl\nsessionId\ncategoryTitle\nsubmitUrl\ninterpretUrl\ncodeDefinition\nsampleTestCase\nenableTestMode\nmetaData\nenableRunCode\nenableSubmit\njudgerAvailable\nemailVerified\nenvInfo\nurlManager\narticle\nquestionDetailUrl\ndiscussCategoryId\ndiscussSolutionCategoryId\n__typename\n}\ninterviewed {\ninterviewedUrl\ncompanies {\nid\nname\n__typename\n}\ntimeOptions {\nid\nname\n__typename\n}\nstageOptions {\nid\nname\n__typename\n}\n__typename\n}\nsubscribeUrl\nisPremium\nloginUrl\n}",
            "variables":{'titleSlug':var}}
    headers = {'Referer':'https://leetcode.com/problems/two-sum/description/',
            'Content-type':'application/json',
            'Cookie' : '__cfduid=d4d7cfb2804bbcdc632d735934ea531cd1514725642; LEETCODE_SESSION=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfcGFzc3dvcmRfcmVzZXRfa2V5IjoiNHNqLTE0MmVmNTEyNDU5NTgwNmE2NGI2In0.1bRBUWQdsTXpxA6WVd6pEY60qFFOZ4eJF_eTlIQiUa4; _gat=1; csrftoken=EpKgZKIpWh15WI367vjdzifIJ7LzHdQPHjYb9RgxxQRZl0bG86XUquOA0dLsRjsj; _ga=GA1.2.967718918.1514725643; _gid=GA1.2.165379645.1514906025',
            'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko)'
            'Chrome/61.0.3163.100 Safari/537.36',
            'Origin':'https://leetcode.com',
            'X-csrftoken':'EpKgZKIpWh15WI367vjdzifIJ7LzHdQPHjYb9RgxxQRZl0bG86XUquOA0dLsRjsj'}
    req = requests.post(url = target, data = json.dumps(payload), headers = headers)

    html = req.text
    data = json.loads(html)
    print('var%s'%var)
    print('data%s'%data['data'])
    #print('question%s'%data['data']['question'])
    
    if data['data']['question'] == None:
        return
    content = data['data']['question']['content']
    
    temp = re.compile(r'<[^>]+>',re.S)
    result = temp.sub('',content)
    return result

if(__name__ == '__main__'):
    #数据
    url = 'https://leetcode.com/api/problems/all/'
    wbdata = requests.get(url).text
    data = json.loads(wbdata)
    stat = data['stat_status_pairs']
    
    #创建excel和sheet
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok = True)
    
    #写入数据
    sheet1.write(0, 0, 'level')
    sheet1.write(0, 1, 'title')
    sheet1.write(0, 2, 'content')
    
    i = 1
    for var in stat:
        level = var['difficulty']['level']
        title = var['stat']['question__title_slug']
        sheet1.write(i, 0, level)
        sheet1.write(i, 1, title)
        
        
        # 内容
        content = get_content(title)
        sheet1.write(i, 2, content)
        i = i + 1
    # 保存文件
    dir_url = os.path.abspath('.')
    #print('dir_url%s'%dir_url)
    url = os.path.join(dir_url,'workbook.xls')
    #print('url%s'%url)
    workbook.save(url)