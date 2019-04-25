import urllib.request
import re
import wget
import sys

def download_from_url(url_adr):
    try:
        with urllib.request.urlopen(url_adr) as response:
            read_data = response.read().decode('utf-8')
    except:
        print("Error during loading URL : " + url_adr)
        return

    streams = re.findall('<source data-src="(.+)" type="video\/mp4" data-quality="(.+)">', read_data)
    file_name = re.findall('<div class="article-title vod-title">(.+)<\/div>', read_data)

    if len(streams) == 0 or len(file_name) == 0:
        print('Wrong website structure : ' + url_adr)
        return

    file_name_list = list(file_name[0])

    for i in range(len(file_name_list)):
        if file_name_list[i] == ':':
            file_name_list[i] = '-'

    file_name_normalized = "".join(x for x in file_name_list if (x.isalnum() or x in ['-', ' ']))

    fhd_url = ''
    hd_url = ''
    sd_url = ''
    download_url = ''

    for i in streams:
        if i[1] == '1080p':
            fhd_url = i[0]
        elif i[1] == '720p':
            hd_url = i[0]
        elif i[1] == '480p':
            sd_url = i[0]

    if fhd_url != '':
        download_url = fhd_url
    elif hd_url != '':
        download_url = hd_url
    elif sd_url != '':
        download_url = sd_url
    else:
        print('Error during choosing quality of file')
        return

    print('\nDownloading file : ' + file_name_normalized)
    wget.download(download_url, file_name_normalized +'.mp4')

if len(sys.argv) != 2:
    print('Usage : ps_downloader.py <text_file_with_urls>')
    sys.exit()
else:
    filename = sys.argv[1]
    try:
        with open(filename) as f:
            urls = []
            for line in f:
                urls.append(line.rstrip())
            
    except FileNotFoundError:
        print('No ' + filename + ' file in directory')
        sys.exit()

    for i in urls:
        download_from_url(i)