
countword = 0
filecount = 0
with open('雅思标准词汇3800（第二版）.csv', newline='') as file:



    while countword<3803:
        if countword % 400 == 0:
            filecount = filecount+1
        with open('3800_anki_wordlists/3800_anki_wordlist{}.csv'.format(filecount), 'w', newline='') as write_file:
            for line in file:
                write_file.write(line)
                countword = countword+1
                if countword % 400 == 0:
                    break 