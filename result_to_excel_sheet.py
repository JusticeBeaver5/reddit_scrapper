import xlsxwriter
import reddit_scrapper as rs


posts = rs.request_subreddit_posts('funny', 'hot', 25, 'day')

info = rs.get_post_info(posts)

# print(info)

titles = ['date', 'ups', 'link', 'title', 'id']




def save_data_sheet(titles, data):
    workbook  = xlsxwriter.Workbook('data_sheet.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold':True})
    worksheet.set_column('A:C', 100)
    
    for col in range(len(titles)):
        # create titles
        worksheet.write(0, col, titles[col], bold)
        # fill the sheet
        for row in range(len(data[col])):
            worksheet.write(row+1, col, data[col][row])
    workbook.close()


save_data_sheet(titles, info)