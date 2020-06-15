# coding:utf-8
import pygame,os,time
#文字转图片
def get_txt_image(file_name):
    #pygame初始化
    pygame.init()
    #输入文字
    text = u"%s" % file_name
    font = pygame.font.Font(os.path.join("C:\Windows\Fonts", "simsun.ttc"), 66)
    #渲染图片，设置背景颜色和字体样式，
    rtext = font.render(text, True, (255,255,255), (8,46,84))
    #获取当前时间，设置为image图片名字
    image = get_now_time()
    #保存图片
    pygame.image.save(rtext, "chengyu_image\%s.jpg" % image)
    return image
    print('>>>>%s：文字生成图片执行成功！' % image)

#获取当前时间
import datetime,time
def get_now_time():
    a = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    return a

#图片插入原先文章中
def image_into_content(file_name,image):
    file_title = file_name + '的成语故事带译文.txt'
    file_alt = file_name + '的成语故事带译文'
    file_content =  open('chengyu/%s' % file_title,'r',encoding='utf-8').read()
    content_add = '\n'+'<p style="text-align: center;"><img src="http://127.0.0.2/zb_users/upload/2020/06/%s.jpg" alt="%s" title="%s"></p> ' % (image,file_alt,file_alt)+'\n'
    pos = file_content.find('\n')
    if pos != -1:
        content = file_content[:pos] + content_add + file_content[pos:]
        file_content = open('chengyu/%s' % file_title,'w',encoding='utf-8')
        file_content.write(content)
        file_content.close()
        print('>>>>%s加入图片代码成功！' % file_alt)




#批量读取文件夹中的TXT
def read_txt_title():
    files = os.listdir('chengyu')
    for file_name in files:
        file_name = file_name.split('的')[0]
        image = get_txt_image(file_name)
        # file_name = file_name + '的成语故事.txt'
        time.sleep(3)
        image_into_content(file_name,image)



read_txt_title()

