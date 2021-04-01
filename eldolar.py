import scrapy


class EldolarSpider(scrapy.Spider):
    name = 'eldolar'
    allowed_domains = ['https://www.eldolar.info/es-MX/mexico/dia/hoy']
    start_urls = ['https://www.eldolar.info/es-MX/mexico/dia/hoy']

    def parse(self, response):
        result = []
        data = response.xpath('.//table[@id="dllsTable"]/tbody/tr')
        # data_headers = response.xpath('.//table[@id="dllsTable"]/thead//th')
        # visible_data_headers = data_headers.css('display')
        # print(data_headers)
        # print("=="*50)
        # print("=="*100,'\n',data)
        for row in data:
            # ok = row.xpath('.//td/a/@href').extract()
            # ['compra','venta']
            row_data = row.xpath('.//td//text()').extract()
            row_data = row_data[::-1]
            name_index = 1
            is_number_second_result = False

            try:
                value_temp = float(row_data[1])
                if value_temp:
                    is_number_second_result = True
            except:
                pass

            # print('=='*50)
            # print(row_data)
            dict_temp = {}
            if len(row_data) < 3 and not is_number_second_result:
                dict_temp = {
                    'compra': row_data[0],
                    'venta': row_data[0],
                }
            elif is_number_second_result:
                dict_temp = {
                    'compra': row_data[1],
                    'venta': row_data[0],
                }
                name_index += 1
            else:
                dict_temp = {
                    'compra': row_data[0],
                    'venta': row_data[0],
                }
            dict_temp['banco'] = ''
            banco_data_array = row_data[name_index:]
            banco_data_array = banco_data_array[::-1]
            # print("banco data",banco_data_array)
            dict_temp['banco'] = dict_temp['banco'].join(banco_data_array)

            # print(dict)
            # print('=='*50)
            result.append(dict)
        return result
